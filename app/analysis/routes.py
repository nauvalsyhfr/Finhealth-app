"""
Analysis API Routes
Handles financial health analysis using Expert System
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from app import db
from app.models import AnalysisHistory, SystemLog
from app.analysis.expert_system import analyze_financial_health

analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/analyze', methods=['POST'])
@login_required
def analyze():
    """
    Analyze financial health using Expert System
    
    Expected JSON:
    {
        "pemasukan": float,
        "pengeluaran": float,
        "jumlah_transaksi": int,
        "cashflow": float,
        "notes": str (optional)
    }
    """
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['pemasukan', 'pengeluaran', 'jumlah_transaksi', 'cashflow']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Data tidak lengkap: {", ".join(missing_fields)}'
            }), 400
        
        # Convert to appropriate types
        try:
            pemasukan = float(data['pemasukan'])
            pengeluaran = float(data['pengeluaran'])
            jumlah_transaksi = int(data['jumlah_transaksi'])
            cashflow = float(data['cashflow'])
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'error': 'Format data tidak valid. Pastikan angka dalam format yang benar.'
            }), 400
        
        # Validate positive values
        if pemasukan < 0 or pengeluaran < 0 or jumlah_transaksi < 0:
            return jsonify({
                'success': False,
                'error': 'Pemasukan, pengeluaran, dan jumlah transaksi harus bernilai positif.'
            }), 400
        
        # Run expert system analysis
        analysis_result = analyze_financial_health(
            pemasukan=pemasukan,
            pengeluaran=pengeluaran,
            jumlah_transaksi=jumlah_transaksi,
            cashflow=cashflow
        )
        
        # Save to database
        analysis_record = AnalysisHistory(
            user_id=current_user.id,
            pemasukan=pemasukan,
            pengeluaran=pengeluaran,
            jumlah_transaksi=jumlah_transaksi,
            cashflow=cashflow,
            profit_margin=analysis_result['profit_margin'],
            expense_ratio=analysis_result['expense_ratio'],
            cashflow_ratio=analysis_result['cashflow_ratio'],
            status_kesehatan=analysis_result['status_kesehatan'],
            skor_kesehatan=analysis_result['skor_kesehatan'],
            rekomendasi=analysis_result['rekomendasi'],
            notes=data.get('notes')
        )
        
        db.session.add(analysis_record)
        
        # Log activity
        log = SystemLog(
            user_id=current_user.id,
            action_type='analysis',
            action_description=f'Financial analysis performed - Status: {analysis_result["status_kesehatan"]}',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(log)
        
        db.session.commit()
        
        # Return results
        return jsonify({
            'success': True,
            'message': 'Analisis berhasil dilakukan',
            'analysis_id': analysis_record.id,
            'results': {
                'status_kesehatan': analysis_result['status_kesehatan'],
                'skor_kesehatan': float(analysis_result['skor_kesehatan']),
                'ratios': {
                    'profit_margin': float(analysis_result['profit_margin']),
                    'expense_ratio': float(analysis_result['expense_ratio']),
                    'cashflow_ratio': float(analysis_result['cashflow_ratio'])
                },
                'detail_analisis': analysis_result['detail_analisis'],
                'analysis_date': analysis_record.analysis_date.isoformat()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500


@analysis_bp.route('/history', methods=['GET'])
@login_required
def get_history():
    """
    Get user's analysis history
    
    Query params:
    - limit: number of records (default: 10)
    - offset: pagination offset (default: 0)
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Query analyses
        analyses = AnalysisHistory.query.filter_by(user_id=current_user.id)\
            .order_by(AnalysisHistory.analysis_date.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
        
        total = AnalysisHistory.query.filter_by(user_id=current_user.id).count()
        
        return jsonify({
            'success': True,
            'total': total,
            'limit': limit,
            'offset': offset,
            'analyses': [analysis.to_dict() for analysis in analyses]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500


@analysis_bp.route('/latest', methods=['GET'])
@login_required
def get_latest():
    """Get user's most recent analysis"""
    try:
        latest = AnalysisHistory.query.filter_by(user_id=current_user.id)\
            .order_by(AnalysisHistory.analysis_date.desc())\
            .first()
        
        if not latest:
            return jsonify({
                'success': True,
                'analysis': None,
                'message': 'Belum ada analisis yang dilakukan'
            }), 200
        
        return jsonify({
            'success': True,
            'analysis': latest.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500


@analysis_bp.route('/<int:analysis_id>', methods=['GET'])
@login_required
def get_analysis(analysis_id):
    """Get specific analysis by ID"""
    try:
        analysis = AnalysisHistory.query.filter_by(
            id=analysis_id,
            user_id=current_user.id
        ).first()
        
        if not analysis:
            return jsonify({
                'success': False,
                'error': 'Analisis tidak ditemukan'
            }), 404
        
        return jsonify({
            'success': True,
            'analysis': analysis.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500


@analysis_bp.route('/<int:analysis_id>', methods=['DELETE'])
@login_required
def delete_analysis(analysis_id):
    """Delete specific analysis"""
    try:
        analysis = AnalysisHistory.query.filter_by(
            id=analysis_id,
            user_id=current_user.id
        ).first()
        
        if not analysis:
            return jsonify({
                'success': False,
                'error': 'Analisis tidak ditemukan'
            }), 404
        
        db.session.delete(analysis)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Analisis berhasil dihapus'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500


@analysis_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """Get statistical summary of user's analyses"""
    try:
        analyses = AnalysisHistory.query.filter_by(user_id=current_user.id).all()
        
        if not analyses:
            return jsonify({
                'success': True,
                'stats': None,
                'message': 'Belum ada data analisis'
            }), 200
        
        # Calculate statistics
        total = len(analyses)
        status_counts = {
            'Sehat': sum(1 for a in analyses if a.status_kesehatan == 'Sehat'),
            'Kurang Sehat': sum(1 for a in analyses if a.status_kesehatan == 'Kurang Sehat'),
            'Kritis': sum(1 for a in analyses if a.status_kesehatan == 'Kritis')
        }
        
        avg_score = sum(float(a.skor_kesehatan or 0) for a in analyses) / total
        
        return jsonify({
            'success': True,
            'stats': {
                'total_analyses': total,
                'status_distribution': status_counts,
                'average_score': round(avg_score, 2),
                'latest_status': analyses[0].status_kesehatan if analyses else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500