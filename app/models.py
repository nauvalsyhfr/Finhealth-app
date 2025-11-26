"""
FinHealth Database Models
SQLAlchemy ORM models for all database tables
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    """User model for UMKM accounts"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nama_umkm = db.Column(db.String(150), nullable=False)
    nama_pemilik = db.Column(db.String(150))
    produk = db.Column(db.String(255))
    tanggal_berdiri = db.Column(db.Date)
    alamat = db.Column(db.Text)
    nomor_telepon = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    analyses = db.relationship('AnalysisHistory', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    predictions = db.relationship('PredictionData', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'nama_umkm': self.nama_umkm,
            'nama_pemilik': self.nama_pemilik,
            'produk': self.produk,
            'tanggal_berdiri': self.tanggal_berdiri.isoformat() if self.tanggal_berdiri else None,
            'alamat': self.alamat,
            'nomor_telepon': self.nomor_telepon,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'


class AnalysisHistory(db.Model):
    """Model for storing expert system analysis results"""
    __tablename__ = 'analysis_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Input data
    pemasukan = db.Column(db.Numeric(15, 2), nullable=False)
    pengeluaran = db.Column(db.Numeric(15, 2), nullable=False)
    jumlah_transaksi = db.Column(db.Integer, nullable=False)
    cashflow = db.Column(db.Numeric(15, 2), nullable=False)
    
    # Calculated ratios
    profit_margin = db.Column(db.Numeric(5, 2))
    expense_ratio = db.Column(db.Numeric(5, 2))
    cashflow_ratio = db.Column(db.Numeric(5, 2))
    
    # Expert system output
    status_kesehatan = db.Column(db.Enum('Sehat', 'Kurang Sehat', 'Kritis', name='health_status'), nullable=False)
    skor_kesehatan = db.Column(db.Numeric(5, 2))
    rekomendasi = db.Column(db.Text)
    
    # Metadata
    analysis_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    notes = db.Column(db.Text)
    
    def to_dict(self):
        """Convert analysis to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pemasukan': float(self.pemasukan),
            'pengeluaran': float(self.pengeluaran),
            'jumlah_transaksi': self.jumlah_transaksi,
            'cashflow': float(self.cashflow),
            'profit_margin': float(self.profit_margin) if self.profit_margin else None,
            'expense_ratio': float(self.expense_ratio) if self.expense_ratio else None,
            'cashflow_ratio': float(self.cashflow_ratio) if self.cashflow_ratio else None,
            'status_kesehatan': self.status_kesehatan,
            'skor_kesehatan': float(self.skor_kesehatan) if self.skor_kesehatan else None,
            'rekomendasi': self.rekomendasi,
            'analysis_date': self.analysis_date.isoformat() if self.analysis_date else None,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f'<Analysis {self.id} - {self.status_kesehatan}>'


class PredictionData(db.Model):
    """Model for storing uploaded prediction data and metadata"""
    __tablename__ = 'prediction_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # File information
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    file_path = db.Column(db.String(500))
    
    # Data range
    data_start_date = db.Column(db.Date)
    data_end_date = db.Column(db.Date)
    total_records = db.Column(db.Integer)
    
    # ARIMA model parameters
    arima_order = db.Column(db.String(20))
    model_aic = db.Column(db.Numeric(10, 2))
    model_bic = db.Column(db.Numeric(10, 2))
    
    # Prediction settings
    forecast_months = db.Column(db.Integer, default=6)
    
    # Status
    processing_status = db.Column(
        db.Enum('uploaded', 'processing', 'completed', 'failed', name='processing_status'),
        default='uploaded'
    )
    error_message = db.Column(db.Text)
    
    # Relationships
    results = db.relationship('PredictionResult', backref='prediction', lazy='dynamic', cascade='all, delete-orphan')
    raw_data = db.relationship('UploadedDataRecord', backref='prediction', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, include_results=False):
        """Convert prediction to dictionary"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'data_start_date': self.data_start_date.isoformat() if self.data_start_date else None,
            'data_end_date': self.data_end_date.isoformat() if self.data_end_date else None,
            'total_records': self.total_records,
            'arima_order': self.arima_order,
            'model_aic': float(self.model_aic) if self.model_aic else None,
            'model_bic': float(self.model_bic) if self.model_bic else None,
            'forecast_months': self.forecast_months,
            'processing_status': self.processing_status,
            'error_message': self.error_message
        }
        
        if include_results:
            data['results'] = [r.to_dict() for r in self.results.order_by(PredictionResult.forecast_month)]
        
        return data
    
    def __repr__(self):
        return f'<Prediction {self.id} - {self.filename}>'


class PredictionResult(db.Model):
    """Model for storing ARIMA forecast results"""
    __tablename__ = 'prediction_results'
    
    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('prediction_data.id'), nullable=False)
    
    # Forecast data
    forecast_date = db.Column(db.Date, nullable=False)
    forecast_month = db.Column(db.Integer, nullable=False)
    
    # Predicted values
    predicted_pemasukan = db.Column(db.Numeric(15, 2))
    predicted_pengeluaran = db.Column(db.Numeric(15, 2))
    predicted_cashflow = db.Column(db.Numeric(15, 2))
    predicted_transaksi = db.Column(db.Integer)
    
    # Confidence intervals
    pemasukan_lower = db.Column(db.Numeric(15, 2))
    pemasukan_upper = db.Column(db.Numeric(15, 2))
    pengeluaran_lower = db.Column(db.Numeric(15, 2))
    pengeluaran_upper = db.Column(db.Numeric(15, 2))
    cashflow_lower = db.Column(db.Numeric(15, 2))
    cashflow_upper = db.Column(db.Numeric(15, 2))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert result to dictionary"""
        return {
            'id': self.id,
            'prediction_id': self.prediction_id,
            'forecast_date': self.forecast_date.isoformat() if self.forecast_date else None,
            'forecast_month': self.forecast_month,
            'predicted_pemasukan': float(self.predicted_pemasukan) if self.predicted_pemasukan else None,
            'predicted_pengeluaran': float(self.predicted_pengeluaran) if self.predicted_pengeluaran else None,
            'predicted_cashflow': float(self.predicted_cashflow) if self.predicted_cashflow else None,
            'predicted_transaksi': self.predicted_transaksi,
            'confidence_intervals': {
                'pemasukan': {
                    'lower': float(self.pemasukan_lower) if self.pemasukan_lower else None,
                    'upper': float(self.pemasukan_upper) if self.pemasukan_upper else None
                },
                'pengeluaran': {
                    'lower': float(self.pengeluaran_lower) if self.pengeluaran_lower else None,
                    'upper': float(self.pengeluaran_upper) if self.pengeluaran_upper else None
                },
                'cashflow': {
                    'lower': float(self.cashflow_lower) if self.cashflow_lower else None,
                    'upper': float(self.cashflow_upper) if self.cashflow_upper else None
                }
            }
        }
    
    def __repr__(self):
        return f'<PredictionResult {self.id} - Month {self.forecast_month}>'


class UploadedDataRecord(db.Model):
    """Model for storing raw uploaded financial data"""
    __tablename__ = 'uploaded_data_records'
    
    id = db.Column(db.Integer, primary_key=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey('prediction_data.id'), nullable=False)
    
    # Raw data
    record_date = db.Column(db.Date, nullable=False)
    pemasukan = db.Column(db.Numeric(15, 2))
    pengeluaran = db.Column(db.Numeric(15, 2))
    jumlah_transaksi = db.Column(db.Integer)
    cashflow = db.Column(db.Numeric(15, 2))
    
    row_number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert record to dictionary"""
        return {
            'record_date': self.record_date.isoformat() if self.record_date else None,
            'pemasukan': float(self.pemasukan) if self.pemasukan else None,
            'pengeluaran': float(self.pengeluaran) if self.pengeluaran else None,
            'jumlah_transaksi': self.jumlah_transaksi,
            'cashflow': float(self.cashflow) if self.cashflow else None
        }
    
    def __repr__(self):
        return f'<DataRecord {self.id} - {self.record_date}>'


class SystemLog(db.Model):
    """Model for system activity logging"""
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    action_type = db.Column(db.String(50), nullable=False)
    action_description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Log {self.action_type} - {self.created_at}>'