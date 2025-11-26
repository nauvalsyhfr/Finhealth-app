import os
from app import create_app, db
from app.models import User, AnalysisHistory, PredictionData, PredictionResult

# Create application instance
app = create_app(os.getenv('FLASK_ENV') or 'default')


@app.shell_context_processor
def make_shell_context():
    """Make database and models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'AnalysisHistory': AnalysisHistory,
        'PredictionData': PredictionData,
        'PredictionResult': PredictionResult
    }


@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("✅ Database tables created successfully!")


@app.cli.command()
def drop_db():
    """Drop all database tables"""
    if input("⚠️  Are you sure you want to drop all tables? (yes/no): ").lower() == 'yes':
        db.drop_all()
        print("✅ All tables dropped!")
    else:
        print("❌ Operation cancelled.")


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8080,  # ← UBAH DARI 5000 KE 8080
        debug=True
    )