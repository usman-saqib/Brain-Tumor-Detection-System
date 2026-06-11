# routes/auth.py
from flask import Blueprint, render_template, request, jsonify, session, redirect
from database import signup_user, login_user, get_user_by_id

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def landing():
    return render_template('landing.html')

@auth_bp.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@auth_bp.route('/api/signup', methods=['POST'])
def api_signup():
    """API endpoint for signup"""
    data = request.json
    result = signup_user(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        password=data.get('password'),
        role=data.get('role', 'other')
    )
    return jsonify(result)

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    """API endpoint for login"""
    data = request.json
    result = login_user(
        email=data.get('email'),
        password=data.get('password')
    )
    
    if result['success']:
        session['user_id'] = result['user']['id']
        session['user_email'] = result['user']['email']
        session['user_name'] = f"{result['user']['first_name']} {result['user']['last_name']}"
        return jsonify({'success': True, 'redirect': '/dashboard'})
    return jsonify({'success': False, 'message': result['message']})

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')