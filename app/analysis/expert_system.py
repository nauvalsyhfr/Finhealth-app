"""
FinHealth Expert System
Rule-based financial health diagnosis system for UMKM
"""
import json


class FinancialExpertSystem:
    """
    Expert System for analyzing UMKM financial health
    Uses rule-based inference to diagnose and recommend
    """
    
    def __init__(self):
        self.rules = self._initialize_rules()
    
    def analyze(self, pemasukan, pengeluaran, jumlah_transaksi, cashflow):
        """
        Main analysis method
        
        Args:
            pemasukan (float): Total income
            pengeluaran (float): Total expenses
            jumlah_transaksi (int): Number of transactions
            cashflow (float): Net cashflow
        
        Returns:
            dict: Analysis results with status, score, ratios, and recommendations
        """
        # Calculate financial ratios
        ratios = self._calculate_ratios(pemasukan, pengeluaran, jumlah_transaksi, cashflow)
        
        # Apply expert rules to determine health status
        diagnosis = self._diagnose_health(ratios)
        
        # Generate specific recommendations
        recommendations = self._generate_recommendations(ratios, diagnosis)
        
        return {
            'status_kesehatan': diagnosis['status'],
            'skor_kesehatan': diagnosis['score'],
            'profit_margin': ratios['profit_margin'],
            'expense_ratio': ratios['expense_ratio'],
            'cashflow_ratio': ratios['cashflow_ratio'],
            'rekomendasi': json.dumps(recommendations, ensure_ascii=False),
            'detail_analisis': {
                'ratios': ratios,
                'diagnosis': diagnosis,
                'recommendations': recommendations
            }
        }
    
    def _calculate_ratios(self, pemasukan, pengeluaran, jumlah_transaksi, cashflow):
        """Calculate key financial ratios"""
        
        # Profit Margin (%)
        profit_margin = 0
        if pemasukan > 0:
            profit_margin = ((pemasukan - pengeluaran) / pemasukan) * 100
        
        # Expense Ratio (%)
        expense_ratio = 0
        if pemasukan > 0:
            expense_ratio = (pengeluaran / pemasukan) * 100
        
        # Cashflow Ratio
        cashflow_ratio = 0
        if pengeluaran > 0:
            cashflow_ratio = cashflow / pengeluaran
        
        # Average transaction value
        avg_transaction = 0
        if jumlah_transaksi > 0:
            avg_transaction = pemasukan / jumlah_transaksi
        
        # Net profit
        net_profit = pemasukan - pengeluaran
        
        return {
            'profit_margin': round(profit_margin, 2),
            'expense_ratio': round(expense_ratio, 2),
            'cashflow_ratio': round(cashflow_ratio, 2),
            'avg_transaction': round(avg_transaction, 2),
            'net_profit': round(net_profit, 2),
            'pemasukan': pemasukan,
            'pengeluaran': pengeluaran,
            'jumlah_transaksi': jumlah_transaksi,
            'cashflow': cashflow
        }
    
    def _diagnose_health(self, ratios):
        """
        Apply rule-based diagnosis
        Uses weighted scoring system
        """
        score = 0
        max_score = 100
        flags = []
        
        # Rule 1: Profit Margin Assessment (Weight: 35%)
        profit_margin = ratios['profit_margin']
        if profit_margin >= 20:
            score += 35
            flags.append('profit_excellent')
        elif profit_margin >= 10:
            score += 25
            flags.append('profit_good')
        elif profit_margin >= 5:
            score += 15
            flags.append('profit_moderate')
        elif profit_margin > 0:
            score += 5
            flags.append('profit_low')
        else:
            score += 0
            flags.append('profit_negative')
        
        # Rule 2: Expense Ratio Assessment (Weight: 25%)
        expense_ratio = ratios['expense_ratio']
        if expense_ratio <= 60:
            score += 25
            flags.append('expense_excellent')
        elif expense_ratio <= 75:
            score += 20
            flags.append('expense_good')
        elif expense_ratio <= 90:
            score += 10
            flags.append('expense_moderate')
        elif expense_ratio < 100:
            score += 5
            flags.append('expense_high')
        else:
            score += 0
            flags.append('expense_critical')
        
        # Rule 3: Cashflow Assessment (Weight: 25%)
        cashflow_ratio = ratios['cashflow_ratio']
        if cashflow_ratio >= 0.5:
            score += 25
            flags.append('cashflow_excellent')
        elif cashflow_ratio >= 0.2:
            score += 20
            flags.append('cashflow_good')
        elif cashflow_ratio >= 0:
            score += 10
            flags.append('cashflow_moderate')
        else:
            score += 0
            flags.append('cashflow_negative')
        
        # Rule 4: Transaction Volume Assessment (Weight: 15%)
        jumlah_transaksi = ratios['jumlah_transaksi']
        if jumlah_transaksi >= 100:
            score += 15
            flags.append('transaction_high')
        elif jumlah_transaksi >= 50:
            score += 12
            flags.append('transaction_moderate')
        elif jumlah_transaksi >= 20:
            score += 8
            flags.append('transaction_low')
        else:
            score += 5
            flags.append('transaction_very_low')
        
        # Determine final status
        if score >= 75:
            status = 'Sehat'
            status_desc = 'Kondisi keuangan usaha Anda sangat baik dan stabil'
        elif score >= 50:
            status = 'Kurang Sehat'
            status_desc = 'Kondisi keuangan usaha Anda perlu perbaikan'
        else:
            status = 'Kritis'
            status_desc = 'Kondisi keuangan usaha Anda memerlukan perhatian serius'
        
        return {
            'status': status,
            'score': round(score, 2),
            'description': status_desc,
            'flags': flags
        }
    
    def _generate_recommendations(self, ratios, diagnosis):
        """Generate specific actionable recommendations"""
        recommendations = {
            'prioritas_tinggi': [],
            'prioritas_sedang': [],
            'tips_umum': []
        }
        
        flags = diagnosis['flags']
        
        # Critical recommendations based on flags
        if 'profit_negative' in flags or 'profit_low' in flags:
            recommendations['prioritas_tinggi'].append({
                'kategori': 'Profitabilitas',
                'masalah': 'Margin keuntungan terlalu rendah atau negatif',
                'solusi': 'Tingkatkan harga jual atau kurangi biaya produksi. Evaluasi struktur biaya dan cari supplier yang lebih murah.',
                'target': 'Capai profit margin minimal 10% dalam 3 bulan'
            })
        
        if 'expense_critical' in flags or 'expense_high' in flags:
            recommendations['prioritas_tinggi'].append({
                'kategori': 'Pengendalian Biaya',
                'masalah': 'Pengeluaran terlalu tinggi dibanding pemasukan',
                'solusi': 'Audit semua pengeluaran dan identifikasi biaya yang bisa dikurangi. Fokus pada efisiensi operasional.',
                'target': 'Turunkan expense ratio ke bawah 80% dalam 2 bulan'
            })
        
        if 'cashflow_negative' in flags:
            recommendations['prioritas_tinggi'].append({
                'kategori': 'Arus Kas',
                'masalah': 'Arus kas negatif - risiko likuiditas tinggi',
                'solusi': 'SEGERA: Percepat penagihan piutang, tunda pembayaran non-esensial, dan cari sumber dana darurat.',
                'target': 'Stabilkan cashflow positif dalam 1 bulan'
            })
        
        # Medium priority recommendations
        if 'profit_moderate' in flags:
            recommendations['prioritas_sedang'].append({
                'kategori': 'Optimasi Pendapatan',
                'masalah': 'Profit margin masih bisa ditingkatkan',
                'solusi': 'Lakukan upselling/cross-selling, diversifikasi produk, atau tambah value-added services.',
                'target': 'Tingkatkan profit margin ke 15-20%'
            })
        
        if 'transaction_low' in flags or 'transaction_very_low' in flags:
            recommendations['prioritas_sedang'].append({
                'kategori': 'Volume Penjualan',
                'masalah': 'Jumlah transaksi masih rendah',
                'solusi': 'Tingkatkan marketing, promosi di media sosial, program loyalitas pelanggan, atau kolaborasi bisnis.',
                'target': 'Naikkan jumlah transaksi minimal 30% per bulan'
            })
        
        if 'expense_moderate' in flags:
            recommendations['prioritas_sedang'].append({
                'kategori': 'Efisiensi Operasional',
                'masalah': 'Biaya operasional bisa lebih efisien',
                'solusi': 'Review kontrak supplier, negosiasi harga bulk, dan otomasi proses yang repetitif.',
                'target': 'Turunkan biaya operasional 10-15%'
            })
        
        # General tips based on overall health
        if diagnosis['status'] == 'Sehat':
            recommendations['tips_umum'] = [
                'Pertahankan cash reserve minimal 3 bulan biaya operasional',
                'Mulai investasi untuk pengembangan bisnis (ekspansi, equipment baru)',
                'Dokumentasikan laporan keuangan secara teratur untuk akses modal',
                'Pertimbangkan diversifikasi produk atau pasar'
            ]
        elif diagnosis['status'] == 'Kurang Sehat':
            recommendations['tips_umum'] = [
                'Buat budget bulanan dan tracking pengeluaran ketat',
                'Pisahkan keuangan pribadi dan bisnis',
                'Fokus pada produk/layanan dengan margin tertinggi',
                'Cari mentor atau konsultan bisnis untuk guidance'
            ]
        else:  # Kritis
            recommendations['tips_umum'] = [
                'PRIORITAS: Stabilkan cashflow - ini masalah darurat',
                'Evaluasi apakah bisnis model sustainable atau perlu pivot',
                'Kurangi semua biaya non-esensial segera',
                'Pertimbangkan pinjaman modal kerja jika diperlukan',
                'Konsultasi dengan ahli keuangan atau business advisor'
            ]
        
        # Add specific metrics-based tips
        avg_transaction = ratios.get('avg_transaction', 0)
        if avg_transaction > 0 and avg_transaction < 100000:
            recommendations['tips_umum'].append(
                f'Nilai rata-rata transaksi Anda Rp {avg_transaction:,.0f}. '
                'Pertimbangkan strategi untuk meningkatkan nilai per transaksi.'
            )
        
        return recommendations
    
    def _initialize_rules(self):
        """Initialize expert system rules (for future expansion)"""
        return {
            'profit_threshold': {
                'excellent': 20,
                'good': 10,
                'moderate': 5,
                'low': 0
            },
            'expense_threshold': {
                'excellent': 60,
                'good': 75,
                'moderate': 90,
                'high': 100
            },
            'cashflow_threshold': {
                'excellent': 0.5,
                'good': 0.2,
                'moderate': 0
            }
        }


# Helper function for API use
def analyze_financial_health(pemasukan, pengeluaran, jumlah_transaksi, cashflow):
    """
    Wrapper function for easy API integration
    
    Returns:
        dict: Complete analysis results
    """
    expert = FinancialExpertSystem()
    return expert.analyze(pemasukan, pengeluaran, jumlah_transaksi, cashflow)
