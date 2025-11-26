"""
History Routes - Combines analysis and prediction history
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import AnalysisHistory, PredictionData

history_bp = Blueprint('history', __name__)

@history_bp.route('/all', methods=['GET'])
@login_required
def get_all_history():
    """Get combined history of analyses and predictions"""
    try:
        limit = request.args.get('limit', 20, type=int)
        
        # Get analyses
        analyses = AnalysisHistory.query.filter_by(user_id=current_user.id)\
            .order_by(AnalysisHistory.analysis_date.desc())\
            .limit(limit // 2)\
            .all()
        
        # Get predictions
        predictions = PredictionData.query.filter_by(user_id=current_user.id)\
            .order_by(PredictionData.upload_date.desc())\
            .limit(limit // 2)\
            .all()
        
        # Combine and format
        history = []
        
        for analysis in analyses:
            history.append({
                'type': 'analysis',
                'id': analysis.id,
                'date': analysis.analysis_date.isoformat(),
                'status': analysis.status_kesehatan,
                'score': float(analysis.skor_kesehatan) if analysis.skor_kesehatan else None,
                'data': analysis.to_dict()
            })
        
        for prediction in predictions:
            history.append({
                'type': 'prediction',
                'id': prediction.id,
                'date': prediction.upload_date.isoformat(),
                'status': prediction.processing_status,
                'filename': prediction.filename,
                'data': prediction.to_dict()
            })
        
        # Sort by date
        history.sort(key=lambda x: x['date'], reverse=True)
        
        return jsonify({
            'success': True,
            'total': len(history),
            'history': history[:limit]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500