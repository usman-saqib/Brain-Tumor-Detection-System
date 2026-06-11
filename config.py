# config.py
import os

class Config:
    SECRET_KEY = 'your-secret-key-here'
    UPLOAD_FOLDER = 'uploads'
    REPORT_FOLDER = 'reports'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'jfif', 'bmp', 'tiff', 'tif', 'webp', 'gif'}
    TEMPLATES_AUTO_RELOAD = False
    DB_PATH = 'neurascan.db'

    @staticmethod
    def init_folders():
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.REPORT_FOLDER, exist_ok=True)