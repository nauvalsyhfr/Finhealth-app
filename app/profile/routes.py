from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import SystemLog

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/', methods=['GET'])
@login_required
def get_profile():
    """Get current user profile"""
    return jsonify({
        'success': True,
        'profile': current_user.to_dict()
    }), 200


@profile_bp.route('/update', methods=['PUT', 'POST'])
@login_required
def update_profile():
    """Update user profile"""
    try:
        data = request.get_json()
        
        # Update allowed fields
        allowed_fields = ['nama_umkm', 'nama_pemilik', 'produk', 'alamat', 'nomor_telepon', 'tanggal_berdiri']
        
        for field in allowed_fields:
            if field in data:
                if field == 'tanggal_berdiri' and data[field]:
                    try:
                        current_user.tanggal_berdiri = datetime.strptime(data[field], '%Y-%m-%d').date()
                    except:
                        pass
                else:
                    setattr(current_user, field, data[field])
        
        current_user.updated_at = datetime.utcnow()
        
        # Log activity
        log = SystemLog(
            user_id=current_user.id,
            action_type='profile_update',
            action_description='Profile updated',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(log)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Profil berhasil diperbarui',
            'profile': current_user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500


@profile_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Change user password"""
    try:
        data = request.get_json()
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        if not all([current_password, new_password, confirm_password]):
            return jsonify({
                'success': False,
                'error': 'Semua field password harus diisi'
            }), 400
        
        # Verify current password
        if not current_user.check_password(current_password):
            return jsonify({
                'success': False,
                'error': 'Password lama tidak sesuai'
            }), 401
        
        # Check password match
        if new_password != confirm_password:
            return jsonify({
                'success': False,
                'error': 'Password baru tidak cocok'
            }), 400
        
        # Validate password strength
        if len(new_password) < 6:
            return jsonify({
                'success': False,
                'error': 'Password minimal 6 karakter'
            }), 400
        
        # Update password
        current_user.set_password(new_password)
        
        # Log activity
        log = SystemLog(
            user_id=current_user.id,
            action_type='password_change',
            action_description='Password changed',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(log)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Password berhasil diubah'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500


@profile_bp.route('/statistics', methods=['GET'])
@login_required
def get_statistics():
    """Get user's overall statistics"""
    try:
        from app.models import AnalysisHistory, PredictionData
        
        total_analyses = AnalysisHistory.query.filter_by(user_id=current_user.id).count()
        total_predictions = PredictionData.query.filter_by(user_id=current_user.id).count()
        
        # Get latest analysis
        latest_analysis = AnalysisHistory.query.filter_by(user_id=current_user.id)\
            .order_by(AnalysisHistory.analysis_date.desc())\
            .first()
        
        # Get latest prediction
        latest_prediction = PredictionData.query.filter_by(user_id=current_user.id)\
            .order_by(PredictionData.upload_date.desc())\
            .first()
        
        stats = {
            'total_analyses': total_analyses,
            'total_predictions': total_predictions,
            'member_since': current_user.created_at.isoformat(),
            'last_login': current_user.last_login.isoformat() if current_user.last_login else None,
            'latest_analysis': latest_analysis.to_dict() if latest_analysis else None,
            'latest_prediction': latest_prediction.to_dict() if latest_prediction else None
        }
        
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500
