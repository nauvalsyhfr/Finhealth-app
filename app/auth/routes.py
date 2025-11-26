"""
Authentication Routes
Handles user registration, login, and logout
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app import db
from app.models import User, SystemLog

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'GET':
        return render_template('auth/register.html')
    
    # POST request - handle registration
    data = request.get_json() if request.is_json else request.form
    
    # Validation
    required_fields = ['email', 'password', 'nama_umkm']
    missing_fields = [field for field in required_fields if not data.get(field)]
    
    if missing_fields:
        if request.is_json:
            return jsonify({
                'success': False,
                'error': f'Field yang wajib diisi: {", ".join(missing_fields)}'
            }), 400
        flash(f'Field yang wajib diisi: {", ".join(missing_fields)}', 'danger')
        return redirect(url_for('auth.register'))
    
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        if request.is_json:
            return jsonify({
                'success': False,
                'error': 'Email sudah terdaftar'
            }), 400
        flash('Email sudah terdaftar', 'danger')
        return redirect(url_for('auth.register'))
    
    # Create new user
    try:
        user = User(
            email=data['email'],
            nama_umkm=data['nama_umkm'],
            nama_pemilik=data.get('nama_pemilik'),
            produk=data.get('produk'),
            nomor_telepon=data.get('nomor_telepon'),
            alamat=data.get('alamat')
        )
        user.set_password(data['password'])
        
        # Parse tanggal_berdiri if provided
        if data.get('tanggal_berdiri'):
            try:
                user.tanggal_berdiri = datetime.strptime(data['tanggal_berdiri'], '%Y-%m-%d').date()
            except:
                pass
        
        db.session.add(user)
        db.session.commit()
        
        # Log registration
        log = SystemLog(
            user_id=user.id,
            action_type='register',
            action_description=f'New user registered: {user.email}',
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(log)
        db.session.commit()
        
        if request.is_json:
            return jsonify({
                'success': True,
                'message': 'Registrasi berhasil! Silakan login.',
                'user': user.to_dict()
            }), 201
        
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('auth.login'))
        
    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({
                'success': False,
                'error': f'Terjadi kesalahan: {str(e)}'
            }), 500
        flash('Terjadi kesalahan saat registrasi', 'danger')
        return redirect(url_for('auth.register'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    # POST request - handle login
    data = request.get_json() if request.is_json else request.form
    
    email = data.get('email')
    password = data.get('password')
    remember = data.get('remember', False)
    
    if not email or not password:
        if request.is_json:
            return jsonify({
                'success': False,
                'error': 'Email dan password harus diisi'
            }), 400
        flash('Email dan password harus diisi', 'danger')
        return redirect(url_for('auth.login'))
    
    # Find user
    user = User.query.filter_by(email=email).first()
    
    if user is None or not user.check_password(password):
        if request.is_json:
            return jsonify({
                'success': False,
                'error': 'Email atau password salah'
            }), 401
        flash('Email atau password salah', 'danger')
        return redirect(url_for('auth.login'))
    
    if not user.is_active:
        if request.is_json:
            return jsonify({
                'success': False,
                'error': 'Akun Anda tidak aktif'
            }), 403
        flash('Akun Anda tidak aktif', 'danger')
        return redirect(url_for('auth.login'))
    
    # Login user
    login_user(user, remember=remember)
    user.last_login = datetime.utcnow()
    
    # Log login
    log = SystemLog(
        user_id=user.id,
        action_type='login',
        action_description=f'User logged in: {user.email}',
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(log)
    db.session.commit()
    
    if request.is_json:
        return jsonify({
            'success': True,
            'message': 'Login berhasil',
            'user': user.to_dict(),
            'redirect': url_for('dashboard.index')
        }), 200
    
    flash(f'Selamat datang, {user.nama_umkm}!', 'success')
    
    # Redirect to next page or dashboard
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    # Log logout
    log = SystemLog(
        user_id=current_user.id,
        action_type='logout',
        action_description=f'User logged out: {current_user.email}',
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent')
    )
    db.session.add(log)
    db.session.commit()
    
    logout_user()
    flash('Anda telah keluar', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    """Check if user is authenticated (API endpoint)"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': current_user.to_dict()
        }), 200
    
    return jsonify({'authenticated': False}), 200
