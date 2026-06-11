# routes/__init__.py
from .dashboard import dashboard_bp
from .detection import detection_bp
from .history import history_bp
from .profile import profile_bp
from .reports import reports_bp
from .analytics import analytics_bp
from .auth import auth_bp

__all__ = [
    'dashboard_bp',
    'detection_bp', 
    'history_bp',
    'profile_bp',
    'reports_bp',
    'analytics_bp',
    'auth_bp'
]