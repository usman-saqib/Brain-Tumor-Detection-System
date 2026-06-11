# app.py - Main Entry Point
from flask import Flask
from config import Config
from routes.dashboard import dashboard_bp
from routes.detection import detection_bp
from routes.history import history_bp
from routes.profile import profile_bp
from routes.reports import reports_bp
from routes.analytics import analytics_bp
from routes.auth import auth_bp
from models.model_loader import get_model

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

# Initialize folders
Config.init_folders()

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(detection_bp)
app.register_blueprint(history_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(reports_bp)
app.register_blueprint(analytics_bp)

if __name__ == '__main__':
    try:
        # Load model before starting server
        get_model()
        print("\n" + "="*50)
        print("✓ NEUROSCAN AI IS READY!")
        print("="*50)
        print(f"✓ Server: http://localhost:5000")
        print(f"✓ Dashboard: http://localhost:5000/dashboard")
        print(f"✓ Detection: http://localhost:5000/detection")
        print(f"✓ History: http://localhost:5000/history")
        print(f"✓ Profile: http://localhost:5000/profile")
        print(f"✓ Reports: http://localhost:5000/reports")
        print(f"✓ Analytics: http://localhost:5000/analytics")
        print("="*50)
        print("Press CTRL+C to stop\n")
        app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
    except Exception as e:
        print(f"\n✗ Failed to start: {str(e)}")