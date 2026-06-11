# routes/reports.py
from flask import Blueprint, render_template, session, redirect, request, jsonify, send_file
import base64
from datetime import datetime
from config import Config
import sqlite3
import json

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports')
def reports_page():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('reports.html')

@reports_bp.route('/api/user-history', methods=['GET'])
def get_user_history():
    """Get user's analysis history"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, image_filename, prediction, confidence, analysis_time, created_at
            FROM analysis_history 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 100
        ''', (session['user_id'],))
        
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e), 'history': []})

@reports_bp.route('/api/download-report', methods=['POST'])
def download_report():
    try:
        data = request.json
        result = data['result']
        
        # Decode images from base64
        original_image = base64.b64decode(result['original_image'])
        overlay_image = base64.b64decode(result['overlay_image'])
        heatmap_image = base64.b64decode(result['heatmap_image'])
        comparison_image = base64.b64decode(result['comparison_image'])
        
        from utils.image_utils import decode_to_array
        from utils.pdf_generator import generate_pdf_report
        
        original_arr = decode_to_array(original_image)
        overlay_arr = decode_to_array(overlay_image)
        heatmap_arr = decode_to_array(heatmap_image)
        comparison_arr = decode_to_array(comparison_image)
        
        pdf_path = generate_pdf_report(
            result, original_arr, overlay_arr, heatmap_arr, comparison_arr,
            result['probability_chart'], result['detailed_metrics'],
            Config.UPLOAD_FOLDER, Config.REPORT_FOLDER
        )
        
        return send_file(
            pdf_path, 
            as_attachment=True, 
            download_name=f"neuroscan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mimetype='application/pdf'
        )
    
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/api/analysis/<int:analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """Get analysis details by ID"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM analysis_history 
            WHERE id = ? AND user_id = ?
        ''', (analysis_id, session['user_id']))
        
        analysis = cursor.fetchone()
        conn.close()
        
        if analysis:
            # Parse probabilities JSON
            analysis_dict = dict(analysis)
            if analysis_dict.get('probabilities'):
                analysis_dict['probabilities'] = json.loads(analysis_dict['probabilities'])
            return jsonify({'success': True, 'analysis': analysis_dict})
        return jsonify({'success': False, 'message': 'Analysis not found'}), 404
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500