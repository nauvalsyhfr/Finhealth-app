// Analysis Tab Content and Logic

function loadAnalysisTab() {
    const tabContent = document.getElementById('tab-analisis');
    
    tabContent.innerHTML = `
        <div style="margin-bottom: 2rem;">
            <h2 style="color: var(--primary-color);">Analisis Kesehatan Finansial</h2>
            <p style="color: var(--text-secondary);">Masukkan data keuangan UMKM Anda untuk mendapatkan analisis dan rekomendasi</p>
        </div>

        <div class="row">
            <!-- Input Form -->
            <div class="col-6">
                <div class="card" style="background: var(--dark-card); border-color: var(--dark-border);">
                    <div class="card-header" style="background: var(--dark-bg-secondary); border-bottom-color: var(--dark-border);">
                        <h3 class="card-title">Input Data Keuangan</h3>
                    </div>
                    <div class="card-body">
                        <form id="analysisForm">
                            <div class="form-group">
                                <label for="pemasukan" class="form-label">Pemasukan (Rp)</label>
                                <input type="number" id="pemasukan" name="pemasukan" class="form-control" placeholder="0" required min="0" step="0.01" style="background: var(--dark-bg); color: var(--text-primary); border-color: var(--dark-border);">
                                <small class="text-muted">Total pendapatan dalam periode</small>
                            </div>

                            <div class="form-group">
                                <label for="pengeluaran" class="form-label">Pengeluaran (Rp)</label>
                                <input type="number" id="pengeluaran" name="pengeluaran" class="form-control" placeholder="0" required min="0" step="0.01" style="background: var(--dark-bg); color: var(--text-primary); border-color: var(--dark-border);">
                                <small class="text-muted">Total biaya operasional</small>
                            </div>

                            <div class="form-group">
                                <label for="jumlah_transaksi" class="form-label">Jumlah Transaksi</label>
                                <input type="number" id="jumlah_transaksi" name="jumlah_transaksi" class="form-control" placeholder="0" required min="0" style="background: var(--dark-bg); color: var(--text-primary); border-color: var(--dark-border);">
                                <small class="text-muted">Jumlah transaksi penjualan</small>
                            </div>

                            <div class="form-group">
                                <label for="cashflow" class="form-label">Cashflow (Rp)</label>
                                <input type="number" id="cashflow" name="cashflow" class="form-control" placeholder="0" required step="0.01" style="background: var(--dark-bg); color: var(--text-primary); border-color: var(--dark-border);">
                                <small class="text-muted">Arus kas bersih (bisa negatif)</small>
                            </div>

                            <div class="form-group">
                                <label for="notes" class="form-label">Catatan (Opsional)</label>
                                <textarea id="notes" name="notes" class="form-control" rows="3" placeholder="Tambahkan catatan jika diperlukan" style="background: var(--dark-bg); color: var(--text-primary); border-color: var(--dark-border);"></textarea>
                            </div>

                            <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;" id="analyzeBtn">
                                <span id="analyzeBtnText">Analisis Sekarang</span>
                                <span id="analyzeBtnSpinner" class="d-none">
                                    <div class="spinner" style="width: 20px; height: 20px; border-width: 2px;"></div>
                                </span>
                            </button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Results -->
            <div class="col-6">
                <div class="card" id="resultsCard" style="background: var(--dark-card); border-color: var(--dark-border);">
                    <div class="card-header" style="background: var(--dark-bg-secondary); border-bottom-color: var(--dark-border);">
                        <h3 class="card-title">Hasil Analisis</h3>
                    </div>
                    <div class="card-body">
                        <div id="analysisResults">
                            <div style="text-align: center; padding: 3rem; color: var(--text-muted);">
                                <svg style="width: 80px; height: 80px; margin-bottom: 1rem; opacity: 0.3;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                                </svg>
                                <p>Masukkan data keuangan dan klik "Analisis Sekarang"</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Recommendations Card (initially hidden) -->
                <div class="card" id="recommendationsCard" style="margin-top: 1rem; display: none; background: var(--dark-card); border-color: var(--dark-border);">
                    <div class="card-header" style="background: var(--dark-bg-secondary); border-bottom-color: var(--dark-border);">
                        <h3 class="card-title">Rekomendasi</h3>
                    </div>
                    <div class="card-body" id="recommendationsContent">
                    </div>
                </div>
            </div>
        </div>

        <!-- Analysis History -->
        <div class="card" style="margin-top: 2rem; background: var(--dark-card); border-color: var(--dark-border);">
            <div class="card-header" style="background: var(--dark-bg-secondary); border-bottom-color: var(--dark-border);">
                <h3 class="card-title">Riwayat Analisis</h3>
            </div>
            <div class="card-body">
                <div id="analysisHistory">
                    <p class="text-muted text-center">Memuat riwayat...</p>
                </div>
            </div>
        </div>
    `;

    // Initialize form handler
    initAnalysisForm();
    loadAnalysisHistory();
}

function initAnalysisForm() {
    const form = document.getElementById('analysisForm');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const btn = document.getElementById('analyzeBtn');
        const btnText = document.getElementById('analyzeBtnText');
        const btnSpinner = document.getElementById('analyzeBtnSpinner');
        
        // Disable button and show spinner
        btn.disabled = true;
        btnText.classList.add('d-none');
        btnSpinner.classList.remove('d-none');
        
        const formData = {
            pemasukan: parseFloat(document.getElementById('pemasukan').value),
            pengeluaran: parseFloat(document.getElementById('pengeluaran').value),
            jumlah_transaksi: parseInt(document.getElementById('jumlah_transaksi').value),
            cashflow: parseFloat(document.getElementById('cashflow').value),
            notes: document.getElementById('notes').value
        };
        
        try {
            const response = await fetch('/api/analysis/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const data = await response.json();
            
            if (data.success) {
                displayAnalysisResults(data.results);
                showAlert('success', 'Analisis berhasil dilakukan!');
                loadAnalysisHistory();
                loadDashboardStats(); // Refresh dashboard stats
            } else {
                showAlert('danger', data.error || 'Analisis gagal. Silakan coba lagi.');
            }
        } catch (error) {
            showAlert('danger', 'Terjadi kesalahan. Silakan coba lagi.');
        } finally {
            btn.disabled = false;
            btnText.classList.remove('d-none');
            btnSpinner.classList.add('d-none');
        }
    });
}

function displayAnalysisResults(results) {
    const statusColor = {
        'Sehat': 'success',
        'Kurang Sehat': 'warning',
        'Kritis': 'danger'
    }[results.status_kesehatan] || 'info';
    
    const statusIcon = {
        'Sehat': '✓',
        'Kurang Sehat': '⚠',
        'Kritis': '✕'
    }[results.status_kesehatan] || '?';
    
    const html = `
        <div style="text-align: center; padding: 2rem; background: var(--gray-50); border-radius: var(--radius); margin-bottom: 1.5rem;">
            <div style="font-size: 4rem; margin-bottom: 0.5rem;">${statusIcon}</div>
            <h2 style="color: var(--${statusColor}-color); margin-bottom: 0.5rem;">${results.status_kesehatan}</h2>
            <div style="font-size: var(--font-size-3xl); font-weight: 700; color: var(--primary-color); margin-bottom: 0.5rem;">
                ${results.skor_kesehatan} / 100
            </div>
            <p style="color: var(--gray-600); margin-bottom: 0;">${results.detail_analisis.diagnosis.description}</p>
        </div>

        <div style="margin-bottom: 1.5rem;">
            <h4 style="margin-bottom: 1rem; color: var(--gray-800);">Rasio Keuangan</h4>
            <div class="row">
                <div class="col-4">
                    <div style="text-align: center; padding: 1rem; background: white; border: 2px solid var(--gray-200); border-radius: var(--radius);">
                        <div style="font-size: var(--font-size-sm); color: var(--gray-600); margin-bottom: 0.5rem;">Profit Margin</div>
                        <div style="font-size: var(--font-size-2xl); font-weight: 700; color: var(--success-color);">${results.ratios.profit_margin}%</div>
                    </div>
                </div>
                <div class="col-4">
                    <div style="text-align: center; padding: 1rem; background: white; border: 2px solid var(--gray-200); border-radius: var(--radius);">
                        <div style="font-size: var(--font-size-sm); color: var(--gray-600); margin-bottom: 0.5rem;">Expense Ratio</div>
                        <div style="font-size: var(--font-size-2xl); font-weight: 700; color: var(--warning-color);">${results.ratios.expense_ratio}%</div>
                    </div>
                </div>
                <div class="col-4">
                    <div style="text-align: center; padding: 1rem; background: white; border: 2px solid var(--gray-200); border-radius: var(--radius);">
                        <div style="font-size: var(--font-size-sm); color: var(--gray-600); margin-bottom: 0.5rem;">Cashflow Ratio</div>
                        <div style="font-size: var(--font-size-2xl); font-weight: 700; color: var(--info-color);">${results.ratios.cashflow_ratio}</div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('analysisResults').innerHTML = html;
    
    // Display recommendations
    displayRecommendations(results.detail_analisis.recommendations);
}

function displayRecommendations(recommendations) {
    const card = document.getElementById('recommendationsCard');
    const content = document.getElementById('recommendationsContent');
    
    let html = '';
    
    // High Priority
    if (recommendations.prioritas_tinggi && recommendations.prioritas_tinggi.length > 0) {
        html += '<div style="margin-bottom: 1.5rem;"><h5 style="color: var(--danger-color); margin-bottom: 1rem;">🔴 Prioritas Tinggi</h5>';
        recommendations.prioritas_tinggi.forEach(rec => {
            html += `
                <div style="padding: 1rem; background: #fff5f5; border-left: 4px solid var(--danger-color); border-radius: var(--radius); margin-bottom: 0.75rem;">
                    <h6 style="margin-bottom: 0.5rem; color: var(--danger-color);">${rec.kategori}</h6>
                    <p style="margin-bottom: 0.5rem; font-weight: 600; color: var(--gray-800);">Masalah: ${rec.masalah}</p>
                    <p style="margin-bottom: 0.5rem; color: var(--gray-700);">Solusi: ${rec.solusi}</p>
                    <p style="margin-bottom: 0; font-size: var(--font-size-sm); color: var(--gray-600);">Target: ${rec.target}</p>
                </div>
            `;
        });
        html += '</div>';
    }
    
    // Medium Priority
    if (recommendations.prioritas_sedang && recommendations.prioritas_sedang.length > 0) {
        html += '<div style="margin-bottom: 1.5rem;"><h5 style="color: var(--warning-color); margin-bottom: 1rem;">🟡 Prioritas Sedang</h5>';
        recommendations.prioritas_sedang.forEach(rec => {
            html += `
                <div style="padding: 1rem; background: #fffbf0; border-left: 4px solid var(--warning-color); border-radius: var(--radius); margin-bottom: 0.75rem;">
                    <h6 style="margin-bottom: 0.5rem; color: var(--warning-color);">${rec.kategori}</h6>
                    <p style="margin-bottom: 0.5rem; font-weight: 600; color: var(--gray-800);">Masalah: ${rec.masalah}</p>
                    <p style="margin-bottom: 0.5rem; color: var(--gray-700);">Solusi: ${rec.solusi}</p>
                    <p style="margin-bottom: 0; font-size: var(--font-size-sm); color: var(--gray-600);">Target: ${rec.target}</p>
                </div>
            `;
        });
        html += '</div>';
    }
    
    // General Tips
    if (recommendations.tips_umum && recommendations.tips_umum.length > 0) {
        html += '<div><h5 style="color: var(--info-color); margin-bottom: 1rem;">💡 Tips Umum</h5>';
        html += '<ul style="padding-left: 1.5rem; color: var(--gray-700);">';
        recommendations.tips_umum.forEach(tip => {
            html += `<li style="margin-bottom: 0.5rem;">${tip}</li>`;
        });
        html += '</ul></div>';
    }
    
    content.innerHTML = html;
    card.style.display = 'block';
}

async function loadAnalysisHistory() {
    try {
        const response = await fetch('/api/analysis/history?limit=5');
        const data = await response.json();
        
        if (data.success && data.analyses.length > 0) {
            let html = '<table class="table"><thead><tr><th>Tanggal</th><th>Status</th><th>Skor</th><th>Profit Margin</th><th>Aksi</th></tr></thead><tbody>';
            
            data.analyses.forEach(analysis => {
                const date = new Date(analysis.analysis_date).toLocaleDateString('id-ID');
                const statusClass = {
                    'Sehat': 'success',
                    'Kurang Sehat': 'warning',
                    'Kritis': 'danger'
                }[analysis.status_kesehatan] || 'info';
                
                html += `
                    <tr>
                        <td>${date}</td>
                        <td><span class="badge badge-${statusClass}">${analysis.status_kesehatan}</span></td>
                        <td>${analysis.skor_kesehatan}/100</td>
                        <td>${analysis.profit_margin}%</td>
                        <td>
                            <button class="btn btn-sm btn-outline" onclick="viewAnalysisDetail(${analysis.id})">Detail</button>
                        </td>
                    </tr>
                `;
            });
            
            html += '</tbody></table>';
            document.getElementById('analysisHistory').innerHTML = html;
        } else {
            document.getElementById('analysisHistory').innerHTML = '<p class="text-muted text-center">Belum ada riwayat analisis</p>';
        }
    } catch (error) {
        console.error('Error loading analysis history:', error);
    }
}

async function viewAnalysisDetail(id) {
    // TODO: Implement detail view modal
    showAlert('info', 'Fitur detail akan segera hadir!');
}