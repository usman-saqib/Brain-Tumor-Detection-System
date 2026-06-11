# routes/analytics.py
from flask import Blueprint, render_template, session, redirect, jsonify, request
import sqlite3
from config import Config
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
def analytics_page():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('analytics.html')

@analytics_bp.route('/api/analytics-data', methods=['GET'])
def get_analytics_data():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
    
    try:
        time_filter = request.args.get('filter', '30')
        
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = '''
            SELECT id, prediction, confidence, created_at, analysis_time
            FROM analysis_history 
            WHERE user_id = ?
        '''
        params = [session['user_id']]
        
        if time_filter != 'all':
            days = int(time_filter)
            cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
            query += ' AND created_at >= ?'
            params.append(cutoff_date)
        
        query += ' ORDER BY created_at DESC'
        
        cursor.execute(query, params)
        history = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        total = len(history)
        if total > 0:
            avg_confidence = sum(h['confidence'] for h in history) / total * 100
            best_accuracy = max(h['confidence'] for h in history) * 100
            tumor_count = sum(1 for h in history if h['prediction'] != 'no_tumor')
            tumor_rate = (tumor_count / total) * 100
        else:
            avg_confidence = 0
            best_accuracy = 0
            tumor_count = 0
            tumor_rate = 0
        
        # Class distribution
        glioma_count = sum(1 for h in history if h['prediction'] == 'glioma_tumor')
        meningioma_count = sum(1 for h in history if h['prediction'] == 'meningioma_tumor')
        pituitary_count = sum(1 for h in history if h['prediction'] == 'pituitary_tumor')
        no_tumor_count = sum(1 for h in history if h['prediction'] == 'no_tumor')
        
        # Confidence distribution
        confidence_bins = [0, 0, 0, 0, 0]
        for h in history:
            conf = h['confidence'] * 100
            if conf < 20: confidence_bins[0] += 1
            elif conf < 40: confidence_bins[1] += 1
            elif conf < 60: confidence_bins[2] += 1
            elif conf < 80: confidence_bins[3] += 1
            else: confidence_bins[4] += 1
        
        # Weekly activity
        weekly_activity = []
        for i in range(29, -1, -1):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            count = sum(1 for h in history if h['created_at'].split()[0] == date_str)
            weekly_activity.append({
                'date': date.strftime('%d/%m'),
                'count': count
            })
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_analyses': total,
                'avg_confidence': round(avg_confidence, 1),
                'best_accuracy': round(best_accuracy, 1),
                'tumor_rate': round(tumor_rate, 1),
                'tumor_count': tumor_count,
                'healthy_count': total - tumor_count
            },
            'class_distribution': {
                'glioma': glioma_count,
                'meningioma': meningioma_count,
                'pituitary': pituitary_count,
                'no_tumor': no_tumor_count
            },
            'confidence_distribution': confidence_bins,
            'weekly_activity': weekly_activity,
            'model_performance': {
                'accuracy': 95.7,
                'precision': 94.2,
                'recall': 93.8,
                'f1_score': 94.0,
                'specificity': 96.1
            }
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500