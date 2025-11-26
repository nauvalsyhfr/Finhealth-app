"""
FinHealth Application Factory
Creates and configures the Flask application
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from app.config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name='default'):
    """
    Application factory pattern
    Creates and configures the Flask application
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    CORS(app)
    
    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'
    login_manager.login_message_category = 'warning'
    
    # User loader for Flask-Login
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.landing.routes import landing_bp  
    from app.auth.routes import auth_bp
    from app.dashboard.routes import dashboard_bp
    from app.analysis.routes import analysis_bp
    from app.prediction.routes import prediction_bp
    from app.history.routes import history_bp
    from app.profile.routes import profile_bp
    
    app.register_blueprint(landing_bp)  
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    app.register_blueprint(prediction_bp, url_prefix='/api/prediction')
    app.register_blueprint(history_bp, url_prefix='/api/history')
    app.register_blueprint(profile_bp, url_prefix='/api/profile')
    
    # Root route
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import jsonify, render_template, request
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Endpoint tidak ditemukan'}), 404
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import jsonify, render_template, request
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Terjadi kesalahan server'}), 500
        return render_template('errors/500.html'), 500
    
    return app