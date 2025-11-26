"""
Prediction API Routes
Handles file upload and ARIMA forecasting
"""
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import pandas as pd
import os
from datetime import datetime
from app import db
from app.models import PredictionData, PredictionResult, UploadedDataRecord, SystemLog
from app.prediction.arima_model import FinancialForecaster, forecast_financial_data

prediction_bp = Blueprint('prediction', __name__)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


@prediction_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """
    Upload CSV/Excel file for prediction
    
    Form data:
    - file: CSV or Excel file
    - forecast_months: number of months to forecast (optional, default: 6)
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Tidak ada file yang diupload'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nama file kosong'
            }), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Format file tidak didukung. Gunakan CSV atau Excel (.xlsx, .xls)'
            }), 400
        
        # Get forecast months
        forecast_months = request.form.get('forecast_months', 6, type=int)
        if forecast_months < 1 or forecast_months > current_app.config['MAX_FORECAST_MONTHS']:
            return jsonify({
                'success': False,
                'error': f'Forecast months harus antara 1 dan {current_app.config["MAX_FORECAST_MONTHS"]}'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{current_user.id}_{timestamp}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Read file
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(filepath)
            else:  # Excel
                df = pd.read_excel(filepath)
        except Exception as e:
            os.remove(filepath)
            return jsonify({
                'success': False,
                'error': f'Gagal membaca file: {str(e)}'
            }), 400
        
        # Validate format
        forecaster = FinancialForecaster()
        validation = forecaster.validate_csv_format(df)
        
        if not validation['valid']:
            os.remove(filepath)
            return jsonify({
                'success': False,
                'error': validation['error'],
                'required_columns': validation.get('required_columns', [])
            }), 400
        
        # Create prediction record
        prediction = PredictionData(
            user_id=current_user.id,
            filename=filename,
            file_path=filepath,
            total_records=len(df),
            forecast_months=forecast_months,
            processing_status='processing'
        )
        
        db.session.add(prediction)
        db.session.commit()
        
        # Process data and run ARIMA
        try:
            # Load and prepare data
            clean_df = forecaster.load_data(df)
            
            # Update date range
            prediction.data_start_date = clean_df.index.min().date()
            prediction.data_end_date = clean_df.index.max().date()
            
            # Save raw data
            for idx, row in clean_df.iterrows():
                record = UploadedDataRecord(
                    prediction_id=prediction.id,
                    record_date=idx.date(),
                    pemasukan=row.get('Pemasukan'),
                    pengeluaran=row.get('Pengeluaran'),
                    jumlah_transaksi=row.get('Jumlah Transaksi'),
                    cashflow=row.get('Cashflow'),
                    row_number=clean_df.index.get_loc(idx) + 1
                )
                db.session.add(record)
            
            # Run forecast
            forecast_result = forecast_financial_data(df, forecast_months)
            
            if not forecast_result['success']:
                prediction.processing_status = 'failed'
                prediction.error_message = forecast_result['error']
                db.session.commit()
                
                return jsonify({
                    'success': False,
                    'error': forecast_result['error'],
                    'prediction_id': prediction.id
                }), 400
            
            # Save model info
            if 'pemasukan' in forecast_result['models']:
                model_info = forecast_result['models']['pemasukan']
                prediction.arima_order = model_info['order']
                prediction.model_aic = model_info['aic']
                prediction.model_bic = model_info['bic']
            
            # Save forecast results
            for forecast in forecast_result['forecasts']:
                result = PredictionResult(
                    prediction_id=prediction.id,
                    forecast_date=datetime.strptime(forecast['forecast_date'], '%Y-%m-%d').date(),
                    forecast_month=forecast['forecast_month'],
                    predicted_pemasukan=forecast.get('predicted_pemasukan'),
                    predicted_pengeluaran=forecast.get('predicted_pengeluaran'),
                    predicted_cashflow=forecast.get('predicted_cashflow'),
                    predicted_transaksi=int(forecast.get('predicted_transaksi', 0)),
                    pemasukan_lower=forecast.get('pemasukan_lower'),
                    pemasukan_upper=forecast.get('pemasukan_upper'),
                    pengeluaran_lower=forecast.get('pengeluaran_lower'),
                    pengeluaran_upper=forecast.get('pengeluaran_upper'),
                    cashflow_lower=forecast.get('cashflow_lower'),
                    cashflow_upper=forecast.get('cashflow_upper')
                )
                db.session.add(result)
            
            prediction.processing_status = 'completed'
            
            # Log activity
            log = SystemLog(
                user_id=current_user.id,
                action_type='prediction',
                action_description=f'ARIMA prediction completed - {forecast_months} months forecast',
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent')
            )
            db.session.add(log)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Prediksi berhasil dilakukan',
                'prediction_id': prediction.id,
                'results': forecast_result
            }), 200
            
        except Exception as e:
            db.session.rollback()
            prediction.processing_status = 'failed'
            prediction.error_message = str(e)
            db.session.commit()
            
            return jsonify({
                'success': False,
                'error': f'Gagal melakukan prediksi: {str(e)}',
                'prediction_id': prediction.id
            }), 500
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500


@prediction_bp.route('/history', methods=['GET'])
@login_required
def get_history():
    """Get user's prediction history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        predictions = PredictionData.query.filter_by(user_id=current_user.id)\
            .order_by(PredictionData.upload_date.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
        
        total = PredictionData.query.filter_by(user_id=current_user.id).count()
        
        return jsonify({
            'success': True,
            'total': total,
            'limit': limit,
            'offset': offset,
            'predictions': [p.to_dict() for p in predictions]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500


@prediction_bp.route('/<int:prediction_id>', methods=['GET'])
@login_required
def get_prediction(prediction_id):
    """Get specific prediction with results"""
    try:
        prediction = PredictionData.query.filter_by(
            id=prediction_id,
            user_id=current_user.id
        ).first()
        
        if not prediction:
            return jsonify({
                'success': False,
                'error': 'Prediksi tidak ditemukan'
            }), 404
        
        return jsonify({
            'success': True,
            'prediction': prediction.to_dict(include_results=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500


@prediction_bp.route('/<int:prediction_id>', methods=['DELETE'])
@login_required
def delete_prediction(prediction_id):
    """Delete prediction and its results"""
    try:
        prediction = PredictionData.query.filter_by(
            id=prediction_id,
            user_id=current_user.id
        ).first()
        
        if not prediction:
            return jsonify({
                'success': False,
                'error': 'Prediksi tidak ditemukan'
            }), 404
        
        # Delete file
        if prediction.file_path and os.path.exists(prediction.file_path):
            os.remove(prediction.file_path)
        
        db.session.delete(prediction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Prediksi berhasil dihapus'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500


@prediction_bp.route('/latest', methods=['GET'])
@login_required
def get_latest():
    """Get user's most recent prediction"""
    try:
        latest = PredictionData.query.filter_by(user_id=current_user.id)\
            .order_by(PredictionData.upload_date.desc())\
            .first()
        
        if not latest:
            return jsonify({
                'success': True,
                'prediction': None,
                'message': 'Belum ada prediksi yang dilakukan'
            }), 200
        
        return jsonify({
            'success': True,
            'prediction': latest.to_dict(include_results=True)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500