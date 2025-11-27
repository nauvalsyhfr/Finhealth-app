// Prediction Tab Content and Logic

function loadPredictionTab() {
    const tabContent = document.getElementById('tab-prediksi');
    
    tabContent.innerHTML = `
        <div style="margin-bottom: 2rem;">
            <h2 style="color: var(--primary-color);">Prediksi Keuangan (ARIMA)</h2>
            <p style="color: var(--gray-600);">Upload data historis untuk mendapatkan prediksi keuangan 6-12 bulan ke depan</p>
        </div>

        <div class="row">
            <!-- Upload Form -->
            <div class="col-6">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Upload Data Historis</h3>
                    </div>
                    <div class="card-body">
                        <div class="alert alert-info" style="margin-bottom: 1.5rem;">
                            <strong>Format File:</strong> CSV atau Excel (.xlsx, .xls)<br>
                            <strong>Kolom Required:</strong> Hari/Tanggal, Pemasukan, Pengeluaran, Jumlah Transaksi, Cashflow<br>
                            <strong>Minimal Data:</strong> 10 baris data
                        </div>

                        <form id="predictionForm">
                            <div class="form-group">
                                <label for="dataFile" class="form-label">Pilih File Data</label>
                                <input type="file" id="dataFile" name="file" class="form-control" accept=".csv,.xlsx,.xls" required>
                                <small class="text-muted">Format: CSV atau Excel</small>
                            </div>

                            <div class="form-group">
                                <label for="forecast_months" class="form-label">Periode Prediksi (Bulan)</label>
                                <select id="forecast_months" name="forecast_months" class="form-control">
                                    <option value="3">3 Bulan</option>
                                    <option value="6" selected>6 Bulan</option>
                                    <option value="9">9 Bulan</option>
                                    <option value="12">12 Bulan</option>
                                </select>
                            </div>

                            <button type="submit" class="btn btn-success btn-lg" style="width: 100%;" id="predictBtn">
                                <span id="predictBtnText">
                                    <svg style="width: 20px; height: 20px; display: inline-block; margin-right: 0.5rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
                                    </svg>
                                    Upload & Prediksi
                                </span>
                                <span id="predictBtnSpinner" class="d-none">
                                    <div class="spinner" style="width: 20px; height: 20px; border-width: 2px;"></div>
                                    Memproses...
                                </span>
                            </button>
                        </form>

                        <div id="uploadStatus" style="margin-top: 1rem; display: none;"></div>
                    </div>
                </div>

                <!-- Sample Template -->
                <div class="card" style="margin-top: 1rem;">
                    <div class="card-body">
                        <h5 style="margin-bottom: 1rem;">📥 Download Template</h5>
                        <p style="color: var(--gray-600); font-size: var(--font-size-sm); margin-bottom: 1rem;">
                            Belum punya file data? Download template berikut:
                        </p>
                        <button class="btn btn-outline btn-sm" onclick="downloadTemplate()">
                            Download Template CSV
                        </button>
                    </div>
                </div>
            </div>

            <!-- Results -->
            <div class="col-6">
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">Hasil Prediksi</h3>
                    </div>
                    <div class="card-body">
                        <div id="predictionResults">
                            <div style="text-align: center; padding: 3rem; color: var(--gray-400);">
                                <svg style="width: 80px; height: 80px; margin-bottom: 1rem; opacity: 0.3;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                                </svg>
                                <p>Upload file data untuk melihat hasil prediksi</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Prediction Chart -->
        <div class="card" id="predictionChartCard" style="margin-top: 2rem; display: none;">
            <div class="card-header">
                <h3 class="card-title">Grafik Prediksi</h3>
            </div>
            <div class="card-body">
                <canvas id="predictionChart" style="max-height: 400px;"></canvas>
            </div>
        </div>

        <!-- Prediction History -->
        <div class="card" style="margin-top: 2rem;">
            <div class="card-header">
                <h3 class="card-title">Riwayat Prediksi</h3>
            </div>
            <div class="card-body">
                <div id="predictionHistory">
                    <p class="text-muted text-center">Memuat riwayat...</p>
                </div>
            </div>
        </div>
    `;

    // Initialize form handler
    initPredictionForm();
    loadPredictionHistory();
}

function initPredictionForm() {
    const form = document.getElementById('predictionForm');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const btn = document.getElementById('predictBtn');
        const btnText = document.getElementById('predictBtnText');
        const btnSpinner = document.getElementById('predictBtnSpinner');
        const statusDiv = document.getElementById('uploadStatus');
        
        // Disable button and show spinner
        btn.disabled = true;
        btnText.classList.add('d-none');
        btnSpinner.classList.remove('d-none');
        
        const formData = new FormData();
        const fileInput = document.getElementById('dataFile');
        const file = fileInput.files[0];
        
        if (!file) {
            showAlert('danger', 'Silakan pilih file terlebih dahulu');
            btn.disabled = false;
            btnText.classList.remove('d-none');
            btnSpinner.classList.add('d-none');
            return;
        }
        
        formData.append('file', file);
        formData.append('forecast_months', document.getElementById('forecast_months').value);
        
        // Show upload status
        statusDiv.style.display = 'block';
        statusDiv.innerHTML = '<div class="alert alert-info">Mengupload dan memproses data...</div>';
        
        try {
            const response = await fetch('/api/prediction/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                statusDiv.innerHTML = '<div class="alert alert-success">✓ Prediksi berhasil dilakukan!</div>';
                displayPredictionResults(data.results);
                showAlert('success', 'Prediksi berhasil dilakukan!');
                loadPredictionHistory();
                loadDashboardStats(); // Refresh dashboard stats
                
                // Reset form
                form.reset();
            } else {
                statusDiv.innerHTML = `<div class="alert alert-danger">✕ ${data.error}</div>`;
                showAlert('danger', data.error || 'Prediksi gagal. Silakan coba lagi.');
            }
        } catch (error) {
            statusDiv.innerHTML = '<div class="alert alert-danger">✕ Terjadi kesalahan saat mengupload file</div>';
            showAlert('danger', 'Terjadi kesalahan. Silakan coba lagi.');
        } finally {
            btn.disabled = false;
            btnText.classList.remove('d-none');
            btnSpinner.classList.add('d-none');
        }
    });
}

function displayPredictionResults(results) {
    if (!results.forecasts || results.forecasts.length === 0) {
        document.getElementById('predictionResults').innerHTML = '<p class="text-muted text-center">Tidak ada hasil prediksi</p>';
        return;
    }
    
    // Display summary
    const summary = results.data_summary;
    let html = `
        <div style="margin-bottom: 1.5rem; padding: 1rem; background: var(--gray-50); border-radius: var(--radius);">
            <h5 style="margin-bottom: 1rem;">📊 Informasi Data</h5>
            <div class="row">
                <div class="col-6">
                    <p style="margin-bottom: 0.5rem;"><strong>Periode Data:</strong></p>
                    <p style="color: var(--gray-600);">${summary.start_date} s/d ${summary.end_date}</p>
                </div>
                <div class="col-6">
                    <p style="margin-bottom: 0.5rem;"><strong>Total Records:</strong></p>
                    <p style="color: var(--gray-600);">${summary.total_records} data point</p>
                </div>
            </div>
        </div>

        <h5 style="margin-bottom: 1rem;">🔮 Hasil Prediksi</h5>
        <div style="max-height: 400px; overflow-y: auto;">
            <table class="table">
                <thead>
                    <tr>
                        <th>Bulan</th>
                        <th>Pemasukan</th>
                        <th>Pengeluaran</th>
                        <th>Cashflow</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    results.forecasts.forEach(forecast => {
        const date = new Date(forecast.forecast_date).toLocaleDateString('id-ID', { month: 'short', year: 'numeric' });
        html += `
            <tr>
                <td>${date}</td>
                <td style="color: var(--success-color);">Rp ${formatNumber(forecast.predicted_pemasukan)}</td>
                <td style="color: var(--danger-color);">Rp ${formatNumber(forecast.predicted_pengeluaran)}</td>
                <td style="color: ${forecast.predicted_cashflow >= 0 ? 'var(--success-color)' : 'var(--danger-color)'};">
                    Rp ${formatNumber(forecast.predicted_cashflow)}
                </td>
            </tr>
        `;
    });
    
    html += `
                </tbody>
            </table>
        </div>
    `;
    
    document.getElementById('predictionResults').innerHTML = html;
    
    // Display chart
    displayPredictionChart(results.forecasts);
}

let predictionChartInstance = null;

function displayPredictionChart(forecasts) {
    const card = document.getElementById('predictionChartCard');
    card.style.display = 'block';
    
    const ctx = document.getElementById('predictionChart').getContext('2d');
    
    // Destroy existing chart
    if (predictionChartInstance) {
        predictionChartInstance.destroy();
    }
    
    const labels = forecasts.map(f => new Date(f.forecast_date).toLocaleDateString('id-ID', { month: 'short', year: 'numeric' }));
    const pemasukan = forecasts.map(f => f.predicted_pemasukan);
    const pengeluaran = forecasts.map(f => f.predicted_pengeluaran);
    const cashflow = forecasts.map(f => f.predicted_cashflow);
    
    predictionChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Pemasukan',
                    data: pemasukan,
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'Pengeluaran',
                    data: pengeluaran,
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    tension: 0.4
                },
                {
                    label: 'Cashflow',
                    data: cashflow,
                    borderColor: '#17a2b8',
                    backgroundColor: 'rgba(23, 162, 184, 0.1)',
                    tension: 0.4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Prediksi Keuangan UMKM'
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return 'Rp ' + formatNumber(value);
                        }
                    }
                }
            }
        }
    });
}

async function loadPredictionHistory() {
    try {
        const response = await fetch('/api/prediction/history?limit=5');
        const data = await response.json();
        
        if (data.success && data.predictions.length > 0) {
            let html = '<table class="table"><thead><tr><th>Tanggal Upload</th><th>Filename</th><th>Status</th><th>Periode</th><th>Aksi</th></tr></thead><tbody>';
            
            data.predictions.forEach(prediction => {
                const date = new Date(prediction.upload_date).toLocaleDateString('id-ID');
                const statusClass = {
                    'completed': 'success',
                    'processing': 'warning',
                    'failed': 'danger',
                    'uploaded': 'info'
                }[prediction.processing_status] || 'info';
                
                const statusText = {
                    'completed': 'Selesai',
                    'processing': 'Diproses',
                    'failed': 'Gagal',
                    'uploaded': 'Diupload'
                }[prediction.processing_status] || prediction.processing_status;
                
                html += `
                    <tr>
                        <td>${date}</td>
                        <td>${prediction.filename}</td>
                        <td><span class="badge badge-${statusClass}">${statusText}</span></td>
                        <td>${prediction.forecast_months} bulan</td>
                        <td>
                            ${prediction.processing_status === 'completed' 
                                ? `<button class="btn btn-sm btn-outline" onclick="viewPredictionDetail(${prediction.id})">Lihat</button>`
                                : '<span class="text-muted">-</span>'
                            }
                        </td>
                    </tr>
                `;
            });
            
            html += '</tbody></table>';
            document.getElementById('predictionHistory').innerHTML = html;
        } else {
            document.getElementById('predictionHistory').innerHTML = '<p class="text-muted text-center">Belum ada riwayat prediksi</p>';
        }
    } catch (error) {
        console.error('Error loading prediction history:', error);
    }
}

async function viewPredictionDetail(id) {
    try {
        const response = await fetch(`/api/prediction/${id}`);
        const data = await response.json();
        
        if (data.success) {
            displayPredictionResults({
                data_summary: {
                    start_date: data.prediction.data_start_date,
                    end_date: data.prediction.data_end_date,
                    total_records: data.prediction.total_records
                },
                forecasts: data.prediction.results
            });
            
            // Scroll to results
            document.getElementById('predictionResults').scrollIntoView({ behavior: 'smooth' });
        }
    } catch (error) {
        showAlert('danger', 'Gagal memuat detail prediksi');
    }
}

function downloadTemplate() {
    const csv = `Hari/Tanggal,Pemasukan,Pengeluaran,Jumlah Transaksi,Cashflow
2024-01-01,5000000,3500000,45,1500000
2024-02-01,5500000,3800000,50,1700000
2024-03-01,6000000,4000000,55,2000000
2024-04-01,5800000,3900000,52,1900000
2024-05-01,6200000,4100000,58,2100000
2024-06-01,6500000,4200000,60,2300000
2024-07-01,6800000,4400000,62,2400000
2024-08-01,7000000,4500000,65,2500000
2024-09-01,7200000,4600000,68,2600000
2024-10-01,7500000,4800000,70,2700000`;
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'template_data_keuangan.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    
    showAlert('success', 'Template berhasil didownload!');
}

function formatNumber(num) {
    return new Intl.NumberFormat('id-ID').format(Math.round(num));
}