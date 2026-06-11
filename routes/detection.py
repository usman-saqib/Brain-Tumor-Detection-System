# routes/detection.py - Update the predict function
from flask import Blueprint, render_template, request, jsonify, session, redirect
from werkzeug.utils import secure_filename
import os
import torch
import torch.nn.functional as F
from PIL import Image
import numpy as np
import cv2
from torchvision import transforms
from datetime import datetime
from models.model_loader import get_model, get_config, get_class_names
from utils.gradcam import GradCAM
from utils.chart_utils import *
from utils.image_utils import image_to_base64
from config import Config
import json
import sqlite3

detection_bp = Blueprint('detection', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def load_image(file_path):
    try:
        image = Image.open(file_path)
        return image
    except Exception as e:
        print(f"Error loading image: {str(e)}")
        return None

def preprocess_image(image, img_size=160):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = image.resize((img_size, img_size))
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                           std=[0.229, 0.224, 0.225])
    ])
    img_tensor = transform(image).unsqueeze(0)
    return img_tensor, np.array(image)

def predict_and_visualize(model, img_tensor, original_image, class_names):
    target_layer = model.features[-1]
    grad_cam = GradCAM(model, target_layer)
    
    img_tensor.requires_grad_()
    outputs = model(img_tensor)
    probabilities = F.softmax(outputs, dim=1)
    pred_class = torch.argmax(probabilities, dim=1).item()
    confidence = probabilities[0][pred_class].item()
    all_probs = probabilities[0].detach().numpy()
    
    model.zero_grad()
    class_score = outputs[0][pred_class]
    class_score.backward()
    
    heatmap = grad_cam.generate_heatmap()
    heatmap_resized = cv2.resize(heatmap, (original_image.shape[1], original_image.shape[0]))
    heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
    overlay = cv2.addWeighted(original_image, 0.6, heatmap_colored, 0.4, 0)
    
    return pred_class, confidence, all_probs, heatmap_resized, overlay

def save_analysis_to_db(user_id, prediction, confidence, probabilities, analysis_time):
    """Save analysis automatically to database"""
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        cursor = conn.cursor()
        
        # Create table if not exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                image_filename TEXT,
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL,
                probabilities TEXT,
                analysis_time REAL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        probabilities_json = json.dumps(probabilities)
        
        cursor.execute('''
            INSERT INTO analysis_history (user_id, image_filename, prediction, confidence, probabilities, analysis_time, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, 'MRI_Scan', prediction, confidence, probabilities_json, analysis_time, created_at))
        
        conn.commit()
        analysis_id = cursor.lastrowid
        conn.close()
        
        return {'success': True, 'analysis_id': analysis_id}
    except Exception as e:
        print(f"Error saving analysis: {str(e)}")
        return {'success': False, 'message': str(e)}

@detection_bp.route('/detection')
def detection_page():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('detection.html')

@detection_bp.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed'}), 400
        
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            start_time = datetime.now()
            
            image = load_image(filepath)
            if image is None:
                return jsonify({'error': 'Could not load image'}), 400
            
            model = get_model()
            config = get_config()
            class_names = get_class_names()
            
            img_tensor, original_image = preprocess_image(image, img_size=config['img_size'])
            pred_class, confidence, all_probs, heatmap, overlay = predict_and_visualize(
                model, img_tensor, original_image, class_names
            )
            
            analysis_time = (datetime.now() - start_time).total_seconds()
            
            # Prepare probabilities dictionary
            probabilities_dict = {class_names[i]: float(all_probs[i]) for i in range(len(class_names))}
            
            # Auto-save to database if user is logged in
            analysis_id = None
            if 'user_id' in session:
                save_result = save_analysis_to_db(
                    user_id=session['user_id'],
                    prediction=class_names[pred_class],
                    confidence=float(confidence),
                    probabilities=probabilities_dict,
                    analysis_time=analysis_time
                )
                if save_result['success']:
                    analysis_id = save_result['analysis_id']
            
            result = {
                'success': True,
                'prediction': class_names[pred_class],
                'confidence': float(confidence),
                'all_probabilities': probabilities_dict,
                'original_image': image_to_base64(original_image),
                'overlay_image': image_to_base64(overlay),
                'heatmap_image': create_heatmap_image(heatmap),
                'comparison_image': create_comparison_image(original_image, heatmap),
                'probability_chart': create_probability_chart(all_probs, class_names),
                'detailed_metrics': create_detailed_metrics_chart(all_probs, class_names, confidence),
                'analysis_time': analysis_time,
                'analysis_id': analysis_id,
                'model_info': {
                    'architecture': config.get('architecture', 'MobileNetV2'),
                    'input_size': config.get('img_size', 160),
                    'validation_accuracy': config.get('best_val_accuracy', 0.957),
                    'dataset': config.get('dataset', 'Brain Tumor MRI Dataset')
                }
            }
            
            return jsonify(result)
            
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500