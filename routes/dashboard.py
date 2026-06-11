# routes/dashboard.py
from flask import Blueprint, render_template, session, redirect, jsonify
import sqlite3
from config import Config

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html')

@dashboard_bp.route('/api/user-history')
def api_user_history():
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