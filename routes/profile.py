# routes/profile.py
from flask import Blueprint, render_template, session, redirect, request, jsonify
import sqlite3
from config import Config
from database import hash_password, verify_password, get_user_by_id

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
def profile_page():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('profile.html')

@profile_bp.route('/api/current-user', methods=['GET'])
def api_current_user():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    user = get_user_by_id(session['user_id'])
    if user:
        return jsonify({'success': True, 'user': user})
    return jsonify({'success': False, 'message': 'User not found'}), 404

@profile_bp.route('/api/update-profile', methods=['POST'])
def api_update_profile():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET first_name = ?, last_name = ? WHERE id = ?',
                      (first_name, last_name, session['user_id']))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@profile_bp.route('/api/change-password', methods=['POST'])
def api_change_password():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    data = request.json
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if len(new_password) < 8:
        return jsonify({'success': False, 'message': 'Password must be at least 8 characters'})
    
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE id = ?', (session['user_id'],))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return jsonify({'success': False, 'message': 'User not found'})
        
        if not verify_password(old_password, row[0]):
            conn.close()
            return jsonify({'success': False, 'message': 'Current password is incorrect'})
        
        new_hash = hash_password(new_password)
        cursor.execute('UPDATE users SET password = ? WHERE id = ?', (new_hash, session['user_id']))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Password changed successfully'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})