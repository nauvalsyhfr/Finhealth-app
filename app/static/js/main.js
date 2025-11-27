// Main JavaScript - Utilities, History, and Profile

// Utility function for showing alerts
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} fade-in`;
    alertDiv.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px; box-shadow: var(--shadow-lg);';
    alertDiv.innerHTML = `
        ${message}
        <button onclick="this.parentElement.remove()" style="float: right; background: none; border: none; font-size: 1.5rem; cursor: pointer; line-height: 1; color: inherit; opacity: 0.7;">&times;</button>
    `;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.style.transition = 'opacity 0.5s';
        alertDiv.style.opacity = '0';
        setTimeout(() => alertDiv.remove(), 500);
    }, 5000);
}

// History Tab
function loadHistoryTab() {
    const tabContent = document.getElementById('tab-riwayat');
    
    tabContent.innerHTML = `
        <div style="margin-bottom: 2rem;">
            <h2 style="color: var(--primary-color);">Riwayat Aktivitas</h2>
            <p style="color: var(--gray-600);">Semua analisis dan prediksi yang pernah dilakukan</p>
        </div>

        <div class="card">
            <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
                <h3 class="card-title" style="margin-bottom: 0;">Riwayat Lengkap</h3>
                <div>
                    <button class="btn btn-sm btn-outline" onclick="filterHistory('all')" id="filterAll">Semua</button>
                    <button class="btn btn-sm btn-outline" onclick="filterHistory('analysis')" id="filterAnalysis">Analisis</button>
                    <button class="btn btn-sm btn-outline" onclick="filterHistory('prediction')" id="filterPrediction">Prediksi</button>
                </div>
            </div>
            <div class="card-body">
                <div id="historyContent">
                    <p class="text-muted text-center">Memuat riwayat...</p>
                </div>
            </div>
        </div>
    `;

    loadAllHistory();
}

let currentHistoryFilter = 'all';
let allHistoryData = [];

async function loadAllHistory() {
    try {
        const response = await fetch('/api/history/all?limit=50');
        const data = await response.json();
        
        if (data.success) {
            allHistoryData = data.history;
            displayHistory(allHistoryData);
        } else {
            document.getElementById('historyContent').innerHTML = '<p class="text-muted text-center">Gagal memuat riwayat</p>';
        }
    } catch (error) {
        console.error('Error loading history:', error);
        document.getElementById('historyContent').innerHTML = '<p class="text-muted text-center">Terjadi kesalahan saat memuat riwayat</p>';
    }
}

function filterHistory(type) {
    currentHistoryFilter = type;
    
    // Update button states
    document.querySelectorAll('#filterAll, #filterAnalysis, #filterPrediction').forEach(btn => {
        btn.style.backgroundColor = 'transparent';
        btn.style.color = 'var(--primary-color)';
    });
    
    const activeBtn = document.getElementById(`filter${type.charAt(0).toUpperCase() + type.slice(1)}`);
    if (activeBtn) {
        activeBtn.style.backgroundColor = 'var(--primary-color)';
        activeBtn.style.color = 'white';
    }
    
    // Filter and display
    const filtered = type === 'all' 
        ? allHistoryData 
        : allHistoryData.filter(item => item.type === type);
    
    displayHistory(filtered);
}

function displayHistory(historyData) {
    if (!historyData || historyData.length === 0) {
        document.getElementById('historyContent').innerHTML = '<p class="text-muted text-center">Belum ada riwayat</p>';
        return;
    }
    
    let html = '<div class="timeline">';
    
    historyData.forEach(item => {
        const date = new Date(item.date);
        const dateStr = date.toLocaleDateString('id-ID', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        if (item.type === 'analysis') {
            const statusClass = {
                'Sehat': 'success',
                'Kurang Sehat': 'warning',
                'Kritis': 'danger'
            }[item.status] || 'info';
            
            html += `
                <div style="padding: 1.5rem; border-left: 4px solid var(--primary-color); background: white; margin-bottom: 1rem; border-radius: var(--radius); box-shadow: var(--shadow-sm);">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                        <div>
                            <span class="badge badge-info" style="margin-bottom: 0.5rem;">Analisis</span>
                            <h5 style="margin-bottom: 0.5rem;">Analisis Kesehatan Finansial</h5>
                            <p style="color: var(--gray-600); font-size: var(--font-size-sm); margin-bottom: 0;">${dateStr}</p>
                        </div>
                        <span class="badge badge-${statusClass}" style="font-size: var(--font-size-base);">${item.status}</span>
                    </div>
                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--gray-200);">
                        <div class="row">
                            <div class="col-4">
                                <small style="color: var(--gray-600);">Skor:</small>
                                <p style="font-weight: 600; margin-bottom: 0;">${item.score}/100</p>
                            </div>
                            <div class="col-4">
                                <small style="color: var(--gray-600);">Profit Margin:</small>
                                <p style="font-weight: 600; margin-bottom: 0;">${item.data.profit_margin}%</p>
                            </div>
                            <div class="col-4" style="text-align: right;">
                                <button class="btn btn-sm btn-outline" onclick="viewAnalysisDetail(${item.id})">Detail</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        } else if (item.type === 'prediction') {
            const statusClass = {
                'completed': 'success',
                'processing': 'warning',
                'failed': 'danger',
                'uploaded': 'info'
            }[item.status] || 'info';
            
            const statusText = {
                'completed': 'Selesai',
                'processing': 'Diproses',
                'failed': 'Gagal',
                'uploaded': 'Diupload'
            }[item.status] || item.status;
            
            html += `
                <div style="padding: 1.5rem; border-left: 4px solid var(--success-color); background: white; margin-bottom: 1rem; border-radius: var(--radius); box-shadow: var(--shadow-sm);">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                        <div>
                            <span class="badge badge-success" style="margin-bottom: 0.5rem;">Prediksi</span>
                            <h5 style="margin-bottom: 0.5rem;">Prediksi ARIMA - ${item.filename}</h5>
                            <p style="color: var(--gray-600); font-size: var(--font-size-sm); margin-bottom: 0;">${dateStr}</p>
                        </div>
                        <span class="badge badge-${statusClass}">${statusText}</span>
                    </div>
                    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--gray-200);">
                        <div class="row">
                            <div class="col-4">
                                <small style="color: var(--gray-600);">Periode:</small>
                                <p style="font-weight: 600; margin-bottom: 0;">${item.data.forecast_months} bulan</p>
                            </div>
                            <div class="col-4">
                                <small style="color: var(--gray-600);">Total Data:</small>
                                <p style="font-weight: 600; margin-bottom: 0;">${item.data.total_records || '-'} records</p>
                            </div>
                            <div class="col-4" style="text-align: right;">
                                ${item.status === 'completed' 
                                    ? `<button class="btn btn-sm btn-outline" onclick="viewPredictionDetail(${item.id})">Lihat</button>`
                                    : '<span class="text-muted">-</span>'
                                }
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
    });
    
    html += '</div>';
    
    document.getElementById('historyContent').innerHTML = html;
}

// Profile Tab
function loadProfileTab() {
    const tabContent = document.getElementById('tab-profil');
    
    tabContent.innerHTML = `
        <div style="margin-bottom: 2rem;">
            <h2 style="color: var(--primary-color);">Profil UMKM</h2>
            <p style="color: var(--gray-600);">Kelola informasi akun dan pengaturan Anda</p>
        </div>

        <div class="row">
            <!-- Profile Information -->
            <div class="col-8">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Informasi Profil</h3>
                    </div>
                    <div class="card-body">
                        <form id="profileForm">
                            <div class="row">
                                <div class="col-6">
                                    <div class="form-group">
                                        <label for="profile_nama_umkm" class="form-label">Nama UMKM</label>
                                        <input type="text" id="profile_nama_umkm" name="nama_umkm" class="form-control" required>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="form-group">
                                        <label for="profile_email" class="form-label">Email</label>
                                        <input type="email" id="profile_email" class="form-control" disabled style="background-color: var(--gray-100);">
                                        <small class="text-muted">Email tidak dapat diubah</small>
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="form-group">
                                        <label for="profile_nama_pemilik" class="form-label">Nama Pemilik</label>
                                        <input type="text" id="profile_nama_pemilik" name="nama_pemilik" class="form-control">
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="form-group">
                                        <label for="profile_nomor_telepon" class="form-label">Nomor Telepon</label>
                                        <input type="tel" id="profile_nomor_telepon" name="nomor_telepon" class="form-control">
                                    </div>
                                </div>
                                <div class="col-12">
                                    <div class="form-group">
                                        <label for="profile_produk" class="form-label">Jenis Produk/Layanan</label>
                                        <input type="text" id="profile_produk" name="produk" class="form-control">
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="form-group">
                                        <label for="profile_tanggal_berdiri" class="form-label">Tanggal Berdiri</label>
                                        <input type="date" id="profile_tanggal_berdiri" name="tanggal_berdiri" class="form-control">
                                    </div>
                                </div>
                                <div class="col-12">
                                    <div class="form-group">
                                        <label for="profile_alamat" class="form-label">Alamat</label>
                                        <textarea id="profile_alamat" name="alamat" class="form-control" rows="3"></textarea>
                                    </div>
                                </div>
                            </div>

                            <button type="submit" class="btn btn-primary" id="updateProfileBtn">
                                <span id="updateProfileBtnText">Simpan Perubahan</span>
                                <span id="updateProfileBtnSpinner" class="d-none">
                                    <div class="spinner" style="width: 20px; height: 20px; border-width: 2px;"></div>
                                </span>
                            </button>
                        </form>
                    </div>
                </div>

                <!-- Change Password -->
                <div class="card" style="margin-top: 1rem;">
                    <div class="card-header">
                        <h3 class="card-title">Ubah Password</h3>
                    </div>
                    <div class="card-body">
                        <form id="passwordForm">
                            <div class="form-group">
                                <label for="current_password" class="form-label">Password Lama</label>
                                <input type="password" id="current_password" name="current_password" class="form-control" required>
                            </div>
                            <div class="row">
                                <div class="col-6">
                                    <div class="form-group">
                                        <label for="new_password" class="form-label">Password Baru</label>
                                        <input type="password" id="new_password" name="new_password" class="form-control" required minlength="6">
                                    </div>
                                </div>
                                <div class="col-6">
                                    <div class="form-group">
                                        <label for="confirm_new_password" class="form-label">Konfirmasi Password Baru</label>
                                        <input type="password" id="confirm_new_password" name="confirm_password" class="form-control" required>
                                    </div>
                                </div>
                            </div>

                            <button type="submit" class="btn btn-danger" id="changePasswordBtn">
                                <span id="changePasswordBtnText">Ubah Password</span>
                                <span id="changePasswordBtnSpinner" class="d-none">
                                    <div class="spinner" style="width: 20px; height: 20px; border-width: 2px;"></div>
                                </span>
                            </button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Statistics -->
            <div class="col-4">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Statistik</h3>
                    </div>
                    <div class="card-body">
                        <div id="profileStats">
                            <p class="text-muted text-center">Memuat statistik...</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    loadProfileData();
    initProfileForms();
}

async function loadProfileData() {
    try {
        // Load profile
        const profileResponse = await fetch('/api/profile/');
        const profileData = await profileResponse.json();
        
        if (profileData.success) {
            const profile = profileData.profile;
            document.getElementById('profile_nama_umkm').value = profile.nama_umkm || '';
            document.getElementById('profile_email').value = profile.email || '';
            document.getElementById('profile_nama_pemilik').value = profile.nama_pemilik || '';
            document.getElementById('profile_nomor_telepon').value = profile.nomor_telepon || '';
            document.getElementById('profile_produk').value = profile.produk || '';
            document.getElementById('profile_tanggal_berdiri').value = profile.tanggal_berdiri || '';
            document.getElementById('profile_alamat').value = profile.alamat || '';
        }
        
        // Load statistics
        const statsResponse = await fetch('/api/profile/statistics');
        const statsData = await statsResponse.json();
        
        if (statsData.success) {
            displayProfileStats(statsData.statistics);
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

function displayProfileStats(stats) {
    const memberSince = new Date(stats.member_since).toLocaleDateString('id-ID', { year: 'numeric', month: 'long' });
    
    const html = `
        <div style="text-align: center; padding: 1rem; background: var(--gray-50); border-radius: var(--radius); margin-bottom: 1rem;">
            <div style="font-size: var(--font-size-3xl); font-weight: 700; color: var(--primary-color); margin-bottom: 0.5rem;">
                ${stats.total_analyses + stats.total_predictions}
            </div>
            <div style="color: var(--gray-600);">Total Aktivitas</div>
        </div>
        
        <div style="margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: var(--gray-600);">Analisis:</span>
                <span style="font-weight: 600;">${stats.total_analyses}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                <span style="color: var(--gray-600);">Prediksi:</span>
                <span style="font-weight: 600;">${stats.total_predictions}</span>
            </div>
        </div>
        
        <div style="padding-top: 1rem; border-top: 1px solid var(--gray-200);">
            <p style="color: var(--gray-600); font-size: var(--font-size-sm); margin-bottom: 0.5rem;">Bergabung sejak:</p>
            <p style="font-weight: 600; margin-bottom: 0;">${memberSince}</p>
        </div>
    `;
    
    document.getElementById('profileStats').innerHTML = html;
}

function initProfileForms() {
    // Profile update form
    document.getElementById('profileForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const btn = document.getElementById('updateProfileBtn');
        const btnText = document.getElementById('updateProfileBtnText');
        const btnSpinner = document.getElementById('updateProfileBtnSpinner');
        
        btn.disabled = true;
        btnText.classList.add('d-none');
        btnSpinner.classList.remove('d-none');
        
        const formData = {
            nama_umkm: document.getElementById('profile_nama_umkm').value,
            nama_pemilik: document.getElementById('profile_nama_pemilik').value,
            nomor_telepon: document.getElementById('profile_nomor_telepon').value,
            produk: document.getElementById('profile_produk').value,
            tanggal_berdiri: document.getElementById('profile_tanggal_berdiri').value,
            alamat: document.getElementById('profile_alamat').value
        };
        
        try {
            const response = await fetch('/api/profile/update', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                showAlert('success', 'Profil berhasil diperbarui!');
            } else {
                showAlert('danger', data.error || 'Gagal memperbarui profil');
            }
        } catch (error) {
            showAlert('danger', 'Terjadi kesalahan');
        } finally {
            btn.disabled = false;
            btnText.classList.remove('d-none');
            btnSpinner.classList.add('d-none');
        }
    });
    
    // Password change form
    document.getElementById('passwordForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const newPassword = document.getElementById('new_password').value;
        const confirmPassword = document.getElementById('confirm_new_password').value;
        
        if (newPassword !== confirmPassword) {
            showAlert('danger', 'Password baru tidak cocok!');
            return;
        }
        
        const btn = document.getElementById('changePasswordBtn');
        const btnText = document.getElementById('changePasswordBtnText');
        const btnSpinner = document.getElementById('changePasswordBtnSpinner');
        
        btn.disabled = true;
        btnText.classList.add('d-none');
        btnSpinner.classList.remove('d-none');
        
        const formData = {
            current_password: document.getElementById('current_password').value,
            new_password: newPassword,
            confirm_password: confirmPassword
        };
        
        try {
            const response = await fetch('/api/profile/change-password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                showAlert('success', 'Password berhasil diubah!');
                document.getElementById('passwordForm').reset();
            } else {
                showAlert('danger', data.error || 'Gagal mengubah password');
            }
        } catch (error) {
            showAlert('danger', 'Terjadi kesalahan');
        } finally {
            btn.disabled = false;
            btnText.classList.remove('d-none');
            btnSpinner.classList.add('d-none');
        }
    });
}