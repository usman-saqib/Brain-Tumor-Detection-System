# models/model_loader.py
import torch
import torch.nn as nn
from torchvision import models
import json
from utils.gradcam import GradCAM
from utils.chart_utils import *
from utils.image_utils import image_to_base64
import cv2
import numpy as np

class ModelLoader:
    _instance = None
    _model = None
    _config = None
    _class_names = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
            cls._load_model()
        return cls._instance
    
    @classmethod
    def _load_model(cls):
        try:
            with open('config.json', 'r') as f:
                cls._config = json.load(f)
            
            checkpoint = torch.load('best_model.pth', map_location=torch.device('cpu'))
            cls._model = models.mobilenet_v2(weights=None)
            num_classes = cls._config['num_classes']
            cls._model.classifier = nn.Sequential(
                nn.Dropout(0.2),
                nn.Linear(cls._model.last_channel, num_classes)
            )
            
            if 'model_state_dict' in checkpoint:
                cls._model.load_state_dict(checkpoint['model_state_dict'])
            else:
                cls._model.load_state_dict(checkpoint)
            
            cls._model.eval()
            cls._class_names = cls._config['class_names']
            print("✓ Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise e

def get_model():
    return ModelLoader.get_instance()._model

def get_config():
    return ModelLoader.get_instance()._config

def get_class_names():
    return ModelLoader.get_instance()._class_names