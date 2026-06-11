# utils/image_utils.py
import cv2
import numpy as np
from PIL import Image
import base64
import io
import os
from datetime import datetime

def image_to_base64(image_array):
    img = Image.fromarray(image_array)
    img_io = io.BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return base64.b64encode(img_io.getvalue()).decode()

def save_image_temp(image_array, prefix, upload_folder):
    temp_path = os.path.join(upload_folder, f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
    img = Image.fromarray(image_array)
    img.save(temp_path)
    return temp_path

def decode_to_array(b64_data):
    img = Image.open(io.BytesIO(b64_data))
    return np.array(img)