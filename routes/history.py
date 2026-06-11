# routes/history.py
from flask import Blueprint, render_template, session, redirect, jsonify
import sqlite3
from config import Config

history_bp = Blueprint('history', __name__)

@history_bp.route('/history')
def history_page():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('history.html')

@history_bp.route('/api/delete-analysis/<int:analysis_id>', methods=['DELETE'])
def delete_analysis(analysis_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        conn = sqlite3.connect(Config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM analysis_history WHERE id = ? AND user_id = ?', 
                      (analysis_id, session['user_id']))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Analysis deleted'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})