-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Waktu pembuatan: 26 Nov 2025 pada 04.59
-- Versi server: 10.4.28-MariaDB
-- Versi PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `finhealth_db`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `analysis_history`
--

CREATE TABLE `analysis_history` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `pemasukan` decimal(15,2) NOT NULL,
  `pengeluaran` decimal(15,2) NOT NULL,
  `jumlah_transaksi` int(11) NOT NULL,
  `cashflow` decimal(15,2) NOT NULL,
  `profit_margin` decimal(5,2) DEFAULT NULL,
  `expense_ratio` decimal(5,2) DEFAULT NULL,
  `cashflow_ratio` decimal(5,2) DEFAULT NULL,
  `status_kesehatan` enum('Sehat','Kurang Sehat','Kritis') NOT NULL,
  `skor_kesehatan` decimal(5,2) DEFAULT NULL,
  `rekomendasi` text DEFAULT NULL,
  `analysis_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `notes` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data untuk tabel `analysis_history`
--

INSERT INTO `analysis_history` (`id`, `user_id`, `pemasukan`, `pengeluaran`, `jumlah_transaksi`, `cashflow`, `profit_margin`, `expense_ratio`, `cashflow_ratio`, `status_kesehatan`, `skor_kesehatan`, `rekomendasi`, `analysis_date`, `notes`) VALUES
(1, 2, 10000000.00, 7500000.00, 50, 2500000.00, 25.00, 75.00, 0.33, 'Sehat', 87.00, '{\"prioritas_tinggi\": [], \"prioritas_sedang\": [], \"tips_umum\": [\"Pertahankan cash reserve minimal 3 bulan biaya operasional\", \"Mulai investasi untuk pengembangan bisnis (ekspansi, equipment baru)\", \"Dokumentasikan laporan keuangan secara teratur untuk akses modal\", \"Pertimbangkan diversifikasi produk atau pasar\"]}', '2025-11-23 15:19:23', ''),
(2, 4, 50000000.00, 45000000.00, 500, -5000000.04, 10.00, 90.00, -0.11, 'Kurang Sehat', 50.00, '{\"prioritas_tinggi\": [{\"kategori\": \"Arus Kas\", \"masalah\": \"Arus kas negatif - risiko likuiditas tinggi\", \"solusi\": \"SEGERA: Percepat penagihan piutang, tunda pembayaran non-esensial, dan cari sumber dana darurat.\", \"target\": \"Stabilkan cashflow positif dalam 1 bulan\"}], \"prioritas_sedang\": [{\"kategori\": \"Efisiensi Operasional\", \"masalah\": \"Biaya operasional bisa lebih efisien\", \"solusi\": \"Review kontrak supplier, negosiasi harga bulk, dan otomasi proses yang repetitif.\", \"target\": \"Turunkan biaya operasional 10-15%\"}], \"tips_umum\": [\"Buat budget bulanan dan tracking pengeluaran ketat\", \"Pisahkan keuangan pribadi dan bisnis\", \"Fokus pada produk/layanan dengan margin tertinggi\", \"Cari mentor atau konsultan bisnis untuk guidance\"]}', '2025-11-24 20:16:48', 'Perlu peningkatan!'),
(3, 5, 100000000.00, 80000000.00, 1000, -10000000.00, 20.00, 80.00, -0.12, 'Kurang Sehat', 60.00, '{\"prioritas_tinggi\": [{\"kategori\": \"Arus Kas\", \"masalah\": \"Arus kas negatif - risiko likuiditas tinggi\", \"solusi\": \"SEGERA: Percepat penagihan piutang, tunda pembayaran non-esensial, dan cari sumber dana darurat.\", \"target\": \"Stabilkan cashflow positif dalam 1 bulan\"}], \"prioritas_sedang\": [{\"kategori\": \"Efisiensi Operasional\", \"masalah\": \"Biaya operasional bisa lebih efisien\", \"solusi\": \"Review kontrak supplier, negosiasi harga bulk, dan otomasi proses yang repetitif.\", \"target\": \"Turunkan biaya operasional 10-15%\"}], \"tips_umum\": [\"Buat budget bulanan dan tracking pengeluaran ketat\", \"Pisahkan keuangan pribadi dan bisnis\", \"Fokus pada produk/layanan dengan margin tertinggi\", \"Cari mentor atau konsultan bisnis untuk guidance\"]}', '2025-11-24 20:23:23', 'Perlu peningkatan!'),
(4, 2, 100000000.00, 90000000.00, 1000, -1000000.00, 10.00, 90.00, -0.01, 'Kurang Sehat', 50.00, '{\"prioritas_tinggi\": [{\"kategori\": \"Arus Kas\", \"masalah\": \"Arus kas negatif - risiko likuiditas tinggi\", \"solusi\": \"SEGERA: Percepat penagihan piutang, tunda pembayaran non-esensial, dan cari sumber dana darurat.\", \"target\": \"Stabilkan cashflow positif dalam 1 bulan\"}], \"prioritas_sedang\": [{\"kategori\": \"Efisiensi Operasional\", \"masalah\": \"Biaya operasional bisa lebih efisien\", \"solusi\": \"Review kontrak supplier, negosiasi harga bulk, dan otomasi proses yang repetitif.\", \"target\": \"Turunkan biaya operasional 10-15%\"}], \"tips_umum\": [\"Buat budget bulanan dan tracking pengeluaran ketat\", \"Pisahkan keuangan pribadi dan bisnis\", \"Fokus pada produk/layanan dengan margin tertinggi\", \"Cari mentor atau konsultan bisnis untuk guidance\"]}', '2025-11-25 20:50:26', 'Bagus');

-- --------------------------------------------------------

--
-- Struktur dari tabel `prediction_data`
--

CREATE TABLE `prediction_data` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `upload_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `file_path` varchar(500) DEFAULT NULL,
  `data_start_date` date DEFAULT NULL,
  `data_end_date` date DEFAULT NULL,
  `total_records` int(11) DEFAULT NULL,
  `arima_order` varchar(20) DEFAULT NULL,
  `model_aic` decimal(10,2) DEFAULT NULL,
  `model_bic` decimal(10,2) DEFAULT NULL,
  `forecast_months` int(11) DEFAULT 6,
  `processing_status` enum('uploaded','processing','completed','failed') DEFAULT 'uploaded',
  `error_message` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data untuk tabel `prediction_data`
--

INSERT INTO `prediction_data` (`id`, `user_id`, `filename`, `upload_date`, `file_path`, `data_start_date`, `data_end_date`, `total_records`, `arima_order`, `model_aic`, `model_bic`, `forecast_months`, `processing_status`, `error_message`) VALUES
(1, 2, 'template_data_keuangan.csv', '2025-11-23 15:20:57', '/Applications/XAMPP/xamppfiles/htdocs/Finhealth-app/app/static/uploads/2_20251124_052057_template_data_keuangan.csv', '2024-01-01', '2024-10-01', 10, '(2, 1, 3)', 248.71, 249.89, 3, 'completed', NULL),
(2, 4, 'template_data_keuangan_1.csv', '2025-11-24 20:17:32', '/Applications/XAMPP/xamppfiles/htdocs/Finhealth-app/app/static/uploads/4_20251125_101732_template_data_keuangan_1.csv', '2024-01-01', '2024-10-01', 10, '(2, 1, 3)', 248.71, 249.89, 6, 'completed', NULL),
(3, 5, 'template_data_keuangan_2.csv', '2025-11-24 20:24:03', '/Applications/XAMPP/xamppfiles/htdocs/Finhealth-app/app/static/uploads/5_20251125_102403_template_data_keuangan_2.csv', '2024-01-01', '2024-10-01', 10, '(2, 1, 3)', 248.71, 249.89, 6, 'completed', NULL),
(4, 2, 'template_data_keuangan_3.csv', '2025-11-25 20:51:32', '/Applications/XAMPP/xamppfiles/htdocs/Finhealth-app/app/static/uploads/2_20251126_105132_template_data_keuangan_3.csv', '2024-01-01', '2024-10-01', 10, '(2, 1, 3)', 248.71, 249.89, 3, 'completed', NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `prediction_results`
--

CREATE TABLE `prediction_results` (
  `id` int(11) NOT NULL,
  `prediction_id` int(11) NOT NULL,
  `forecast_date` date NOT NULL,
  `forecast_month` int(11) NOT NULL,
  `predicted_pemasukan` decimal(15,2) DEFAULT NULL,
  `predicted_pengeluaran` decimal(15,2) DEFAULT NULL,
  `predicted_cashflow` decimal(15,2) DEFAULT NULL,
  `predicted_transaksi` int(11) DEFAULT NULL,
  `pemasukan_lower` decimal(15,2) DEFAULT NULL,
  `pemasukan_upper` decimal(15,2) DEFAULT NULL,
  `pengeluaran_lower` decimal(15,2) DEFAULT NULL,
  `pengeluaran_upper` decimal(15,2) DEFAULT NULL,
  `cashflow_lower` decimal(15,2) DEFAULT NULL,
  `cashflow_upper` decimal(15,2) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data untuk tabel `prediction_results`
--

INSERT INTO `prediction_results` (`id`, `prediction_id`, `forecast_date`, `forecast_month`, `predicted_pemasukan`, `predicted_pengeluaran`, `predicted_cashflow`, `predicted_transaksi`, `pemasukan_lower`, `pemasukan_upper`, `pengeluaran_lower`, `pengeluaran_upper`, `cashflow_lower`, `cashflow_upper`, `created_at`) VALUES
(1, 1, '2024-10-31', 1, 7720740.32, 4918918.25, 2758929.16, 72, 7381428.25, 8060052.39, 4737042.48, 5100794.02, 2527921.05, 2989937.27, '2025-11-23 15:20:58'),
(2, 1, '2024-11-30', 2, 7935951.52, 5040093.97, 2791981.78, 75, 7433711.62, 8438191.42, 4772312.03, 5307875.90, 2462002.20, 3121961.35, '2025-11-23 15:20:58'),
(3, 1, '2024-12-30', 3, 8140501.20, 5153466.57, 2798409.77, 77, 7493998.14, 8787004.26, 4815299.91, 5491633.24, 2396962.52, 3199857.03, '2025-11-23 15:20:58'),
(4, 2, '2024-10-31', 1, 7720740.32, 4918918.25, 2758929.16, 72, 7381428.25, 8060052.39, 4737042.48, 5100794.02, 2527921.05, 2989937.27, '2025-11-24 20:17:34'),
(5, 2, '2024-11-30', 2, 7935951.52, 5040093.97, 2791981.78, 75, 7433711.62, 8438191.42, 4772312.03, 5307875.90, 2462002.20, 3121961.35, '2025-11-24 20:17:34'),
(6, 2, '2024-12-30', 3, 8140501.20, 5153466.57, 2798409.77, 77, 7493998.14, 8787004.26, 4815299.91, 5491633.24, 2396962.52, 3199857.03, '2025-11-24 20:17:34'),
(7, 2, '2025-01-29', 4, 8349686.44, 5272351.17, 2778588.70, 80, 7589494.03, 9109878.84, 4878385.95, 5666316.39, 2325295.17, 3231882.23, '2025-11-24 20:17:34'),
(8, 2, '2025-02-28', 5, 8553987.37, 5387048.80, 2733974.99, 83, 7685596.94, 9422377.80, 4939029.72, 5835067.88, 2245557.82, 3222392.16, '2025-11-24 20:17:34'),
(9, 2, '2025-03-30', 6, 8759347.76, 5502568.95, 2667019.44, 85, 7793682.78, 9725012.74, 5006143.53, 5998994.36, 2158094.89, 3175943.98, '2025-11-24 20:17:34'),
(10, 3, '2024-10-31', 1, 7720740.32, 4918918.25, 2758929.16, 72, 7381428.25, 8060052.39, 4737042.48, 5100794.02, 2527921.05, 2989937.27, '2025-11-24 20:24:04'),
(11, 3, '2024-11-30', 2, 7935951.52, 5040093.97, 2791981.78, 75, 7433711.62, 8438191.42, 4772312.03, 5307875.90, 2462002.20, 3121961.35, '2025-11-24 20:24:04'),
(12, 3, '2024-12-30', 3, 8140501.20, 5153466.57, 2798409.77, 77, 7493998.14, 8787004.26, 4815299.91, 5491633.24, 2396962.52, 3199857.03, '2025-11-24 20:24:04'),
(13, 3, '2025-01-29', 4, 8349686.44, 5272351.17, 2778588.70, 80, 7589494.03, 9109878.84, 4878385.95, 5666316.39, 2325295.17, 3231882.23, '2025-11-24 20:24:04'),
(14, 3, '2025-02-28', 5, 8553987.37, 5387048.80, 2733974.99, 83, 7685596.94, 9422377.80, 4939029.72, 5835067.88, 2245557.82, 3222392.16, '2025-11-24 20:24:04'),
(15, 3, '2025-03-30', 6, 8759347.76, 5502568.95, 2667019.44, 85, 7793682.78, 9725012.74, 5006143.53, 5998994.36, 2158094.89, 3175943.98, '2025-11-24 20:24:04'),
(16, 4, '2024-10-31', 1, 7720740.32, 4918918.25, 2758929.16, 72, 7381428.25, 8060052.39, 4737042.48, 5100794.02, 2527921.05, 2989937.27, '2025-11-25 20:51:33'),
(17, 4, '2024-11-30', 2, 7935951.52, 5040093.97, 2791981.78, 75, 7433711.62, 8438191.42, 4772312.03, 5307875.90, 2462002.20, 3121961.35, '2025-11-25 20:51:33'),
(18, 4, '2024-12-30', 3, 8140501.20, 5153466.57, 2798409.77, 77, 7493998.14, 8787004.26, 4815299.91, 5491633.24, 2396962.52, 3199857.03, '2025-11-25 20:51:33');

-- --------------------------------------------------------

--
-- Struktur dari tabel `system_logs`
--

CREATE TABLE `system_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `action_type` varchar(50) NOT NULL,
  `action_description` text DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data untuk tabel `system_logs`
--

INSERT INTO `system_logs` (`id`, `user_id`, `action_type`, `action_description`, `ip_address`, `user_agent`, `created_at`) VALUES
(1, 2, 'register', 'New user registered: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-23 15:11:36'),
(2, 2, 'login', 'User logged in: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-23 15:11:48'),
(3, 2, 'analysis', 'Financial analysis performed - Status: Sehat', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-23 15:19:23'),
(4, 2, 'prediction', 'ARIMA prediction completed - 3 months forecast', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-23 15:20:58'),
(5, 2, 'logout', 'User logged out: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-23 15:26:37'),
(6, 2, 'login', 'User logged in: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-23 15:28:42'),
(7, 2, 'logout', 'User logged out: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-23 15:33:48'),
(8, 2, 'login', 'User logged in: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 06:53:01'),
(9, 2, 'logout', 'User logged out: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 06:54:24'),
(10, 2, 'login', 'User logged in: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 06:55:28'),
(11, 2, 'logout', 'User logged out: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 06:56:03'),
(12, 2, 'login', 'User logged in: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 07:22:02'),
(13, 2, 'logout', 'User logged out: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 07:25:13'),
(14, 2, 'login', 'User logged in: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 07:25:36'),
(15, 2, 'logout', 'User logged out: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 07:31:33'),
(16, 2, 'login', 'User logged in: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 07:31:53'),
(17, 2, 'logout', 'User logged out: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 07:36:14'),
(18, 2, 'login', 'User logged in: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 07:36:28'),
(19, 2, 'login', 'User logged in: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 14:39:26'),
(20, 2, 'logout', 'User logged out: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 14:40:00'),
(21, 3, 'register', 'New user registered: bismillah@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 20:12:27'),
(22, 4, 'register', 'New user registered: alpro2@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 20:15:35'),
(23, 4, 'login', 'User logged in: alpro2@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 20:15:46'),
(24, 4, 'analysis', 'Financial analysis performed - Status: Kurang Sehat', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 20:16:48'),
(25, 4, 'prediction', 'ARIMA prediction completed - 6 months forecast', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 20:17:34'),
(26, 4, 'logout', 'User logged out: alpro2@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 20:18:13'),
(27, 5, 'register', 'New user registered: ptalpro2@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 20:22:24'),
(28, 5, 'login', 'User logged in: ptalpro2@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 20:22:41'),
(29, 5, 'analysis', 'Financial analysis performed - Status: Kurang Sehat', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 20:23:23'),
(30, 5, 'prediction', 'ARIMA prediction completed - 6 months forecast', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 20:24:04'),
(31, 5, 'password_change', 'Password changed', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 20:24:40'),
(32, 5, 'logout', 'User logged out: ptalpro2@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 20:24:52'),
(33, 5, 'login', 'User logged in: ptalpro2@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 20:34:03'),
(34, 5, 'logout', 'User logged out: ptalpro2@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 20:39:32'),
(35, 2, 'login', 'User logged in: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-24 22:14:27'),
(36, 2, 'login', 'User logged in: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-25 15:44:34'),
(37, 2, 'login', 'User logged in: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-25 20:49:39'),
(38, 2, 'analysis', 'Financial analysis performed - Status: Kurang Sehat', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-25 20:50:26'),
(39, 2, 'prediction', 'ARIMA prediction completed - 3 months forecast', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-25 20:51:33'),
(40, 2, 'logout', 'User logged out: alpro@umkm.com', '127.0.0.1', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0', '2025-11-25 20:57:39');

-- --------------------------------------------------------

--
-- Struktur dari tabel `uploaded_data_records`
--

CREATE TABLE `uploaded_data_records` (
  `id` int(11) NOT NULL,
  `prediction_id` int(11) NOT NULL,
  `record_date` date NOT NULL,
  `pemasukan` decimal(15,2) DEFAULT NULL,
  `pengeluaran` decimal(15,2) DEFAULT NULL,
  `jumlah_transaksi` int(11) DEFAULT NULL,
  `cashflow` decimal(15,2) DEFAULT NULL,
  `row_number` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data untuk tabel `uploaded_data_records`
--

INSERT INTO `uploaded_data_records` (`id`, `prediction_id`, `record_date`, `pemasukan`, `pengeluaran`, `jumlah_transaksi`, `cashflow`, `row_number`, `created_at`) VALUES
(1, 1, '2024-01-01', 5000000.00, 3500000.00, 45, 1500000.00, 1, '2025-11-23 15:20:58'),
(2, 1, '2024-02-01', 5500000.00, 3800000.00, 50, 1700000.00, 2, '2025-11-23 15:20:58'),
(3, 1, '2024-03-01', 6000000.00, 4000000.00, 55, 2000000.00, 3, '2025-11-23 15:20:58'),
(4, 1, '2024-04-01', 5800000.00, 3900000.00, 52, 1900000.00, 4, '2025-11-23 15:20:58'),
(5, 1, '2024-05-01', 6200000.00, 4100000.00, 58, 2100000.00, 5, '2025-11-23 15:20:58'),
(6, 1, '2024-06-01', 6500000.00, 4200000.00, 60, 2300000.00, 6, '2025-11-23 15:20:58'),
(7, 1, '2024-07-01', 6800000.00, 4400000.00, 62, 2400000.00, 7, '2025-11-23 15:20:58'),
(8, 1, '2024-08-01', 7000000.00, 4500000.00, 65, 2500000.00, 8, '2025-11-23 15:20:58'),
(9, 1, '2024-09-01', 7200000.00, 4600000.00, 68, 2600000.00, 9, '2025-11-23 15:20:58'),
(10, 1, '2024-10-01', 7500000.00, 4800000.00, 70, 2700000.00, 10, '2025-11-23 15:20:58'),
(11, 2, '2024-01-01', 5000000.00, 3500000.00, 45, 1500000.00, 1, '2025-11-24 20:17:34'),
(12, 2, '2024-02-01', 5500000.00, 3800000.00, 50, 1700000.00, 2, '2025-11-24 20:17:34'),
(13, 2, '2024-03-01', 6000000.00, 4000000.00, 55, 2000000.00, 3, '2025-11-24 20:17:34'),
(14, 2, '2024-04-01', 5800000.00, 3900000.00, 52, 1900000.00, 4, '2025-11-24 20:17:34'),
(15, 2, '2024-05-01', 6200000.00, 4100000.00, 58, 2100000.00, 5, '2025-11-24 20:17:34'),
(16, 2, '2024-06-01', 6500000.00, 4200000.00, 60, 2300000.00, 6, '2025-11-24 20:17:34'),
(17, 2, '2024-07-01', 6800000.00, 4400000.00, 62, 2400000.00, 7, '2025-11-24 20:17:34'),
(18, 2, '2024-08-01', 7000000.00, 4500000.00, 65, 2500000.00, 8, '2025-11-24 20:17:34'),
(19, 2, '2024-09-01', 7200000.00, 4600000.00, 68, 2600000.00, 9, '2025-11-24 20:17:34'),
(20, 2, '2024-10-01', 7500000.00, 4800000.00, 70, 2700000.00, 10, '2025-11-24 20:17:34'),
(21, 3, '2024-01-01', 5000000.00, 3500000.00, 45, 1500000.00, 1, '2025-11-24 20:24:04'),
(22, 3, '2024-02-01', 5500000.00, 3800000.00, 50, 1700000.00, 2, '2025-11-24 20:24:04'),
(23, 3, '2024-03-01', 6000000.00, 4000000.00, 55, 2000000.00, 3, '2025-11-24 20:24:04'),
(24, 3, '2024-04-01', 5800000.00, 3900000.00, 52, 1900000.00, 4, '2025-11-24 20:24:04'),
(25, 3, '2024-05-01', 6200000.00, 4100000.00, 58, 2100000.00, 5, '2025-11-24 20:24:04'),
(26, 3, '2024-06-01', 6500000.00, 4200000.00, 60, 2300000.00, 6, '2025-11-24 20:24:04'),
(27, 3, '2024-07-01', 6800000.00, 4400000.00, 62, 2400000.00, 7, '2025-11-24 20:24:04'),
(28, 3, '2024-08-01', 7000000.00, 4500000.00, 65, 2500000.00, 8, '2025-11-24 20:24:04'),
(29, 3, '2024-09-01', 7200000.00, 4600000.00, 68, 2600000.00, 9, '2025-11-24 20:24:04'),
(30, 3, '2024-10-01', 7500000.00, 4800000.00, 70, 2700000.00, 10, '2025-11-24 20:24:04'),
(31, 4, '2024-01-01', 5000000.00, 3500000.00, 45, 1500000.00, 1, '2025-11-25 20:51:33'),
(32, 4, '2024-02-01', 5500000.00, 3800000.00, 50, 1700000.00, 2, '2025-11-25 20:51:33'),
(33, 4, '2024-03-01', 6000000.00, 4000000.00, 55, 2000000.00, 3, '2025-11-25 20:51:33'),
(34, 4, '2024-04-01', 5800000.00, 3900000.00, 52, 1900000.00, 4, '2025-11-25 20:51:33'),
(35, 4, '2024-05-01', 6200000.00, 4100000.00, 58, 2100000.00, 5, '2025-11-25 20:51:33'),
(36, 4, '2024-06-01', 6500000.00, 4200000.00, 60, 2300000.00, 6, '2025-11-25 20:51:33'),
(37, 4, '2024-07-01', 6800000.00, 4400000.00, 62, 2400000.00, 7, '2025-11-25 20:51:33'),
(38, 4, '2024-08-01', 7000000.00, 4500000.00, 65, 2500000.00, 8, '2025-11-25 20:51:33'),
(39, 4, '2024-09-01', 7200000.00, 4600000.00, 68, 2600000.00, 9, '2025-11-25 20:51:33'),
(40, 4, '2024-10-01', 7500000.00, 4800000.00, 70, 2700000.00, 10, '2025-11-25 20:51:33');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `nama_umkm` varchar(150) NOT NULL,
  `nama_pemilik` varchar(150) DEFAULT NULL,
  `produk` varchar(255) DEFAULT NULL,
  `tanggal_berdiri` date DEFAULT NULL,
  `alamat` text DEFAULT NULL,
  `nomor_telepon` varchar(20) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `is_active` tinyint(1) DEFAULT 1,
  `last_login` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `email`, `password_hash`, `nama_umkm`, `nama_pemilik`, `produk`, `tanggal_berdiri`, `alamat`, `nomor_telepon`, `created_at`, `updated_at`, `is_active`, `last_login`) VALUES
(1, 'admin@finhealth.com', 'scrypt:32768:8:1$2qZxKj8V1nYhXZbF$c8e4c4e4c4e4c4e4c4e4c4e4c4e4c4e4c4e4c4e4c4e4c4e4c4e4c4e4c4e4c4e4', 'FinHealth Admin', 'Administrator', 'Software Development', '2024-01-01', NULL, NULL, '2025-11-23 15:11:41', '2025-11-23 15:11:41', 1, NULL),
(2, 'alpro@umkm.com', 'scrypt:32768:8:1$qnzwZgAdjnBlRyGr$4f90fb3fbe70ed58a5c9a48b14b67fb1a3133c80816995d571e1d4475bd39b882f20edd2c5c088cf363eb7682129921ed0f000c42558101943376ef91d510e66', 'Toko Alpro', 'Nauval', 'Joki', '2025-11-24', NULL, '088901147744', '2025-11-23 15:11:36', '2025-11-25 20:49:39', 1, '2025-11-25 20:49:39'),
(3, 'bismillah@umkm.com', 'scrypt:32768:8:1$Xzcrk451KSIUTzm9$7ac4aa97f157abf0c8d041a78e7d14968a07688fffd1ced5bdf8a4e786d0342eb143d39f270fe3dcd6f79042845c147f9da5a4957b4b3963fb4003e670022a0c', 'Bismillah Alpro', 'Nopil', 'Joki', '2025-11-25', NULL, '088901147744', '2025-11-24 20:12:27', '2025-11-24 20:12:27', 1, NULL),
(4, 'alpro2@umkm.com', 'scrypt:32768:8:1$jbJureiUVAm8mmAq$e94529ee9d0dcbceb0bc892f6fc36482a725527e7a3bb3c8c778d7cefefce0a6b38a366649783d57c82ec644340eb7adb83ac4a1e6bd5a2cc27e816e6d4d8a4c', 'Alpro Store', 'Nopal', 'Joki Alpro', '2025-11-25', NULL, '088901147744', '2025-11-24 20:15:35', '2025-11-24 20:15:46', 1, '2025-11-24 20:15:46'),
(5, 'ptalpro2@umkm.com', 'scrypt:32768:8:1$e7F1iq0r88kfdR4G$45b8cda5f47562b03c6bb4f1bbf89cc8739a6c441d28b3211e241011fbd7fbff6eb99b9c27288ef448088decb61f15167e63b1fab6f0c422441599abf0998c1b', 'PT Alpro ', 'Nopill', 'UAS', '2025-11-25', NULL, '088901147744', '2025-11-24 20:22:24', '2025-11-24 20:34:03', 1, '2025-11-24 20:34:03');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `analysis_history`
--
ALTER TABLE `analysis_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user_date` (`user_id`,`analysis_date`),
  ADD KEY `idx_status` (`status_kesehatan`);

--
-- Indeks untuk tabel `prediction_data`
--
ALTER TABLE `prediction_data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user_upload` (`user_id`,`upload_date`),
  ADD KEY `idx_status` (`processing_status`);

--
-- Indeks untuk tabel `prediction_results`
--
ALTER TABLE `prediction_results`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_prediction_date` (`prediction_id`,`forecast_date`),
  ADD KEY `idx_forecast_month` (`forecast_month`);

--
-- Indeks untuk tabel `system_logs`
--
ALTER TABLE `system_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_user_action` (`user_id`,`action_type`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- Indeks untuk tabel `uploaded_data_records`
--
ALTER TABLE `uploaded_data_records`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_prediction_date` (`prediction_id`,`record_date`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_email` (`email`),
  ADD KEY `idx_created_at` (`created_at`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `analysis_history`
--
ALTER TABLE `analysis_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT untuk tabel `prediction_data`
--
ALTER TABLE `prediction_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT untuk tabel `prediction_results`
--
ALTER TABLE `prediction_results`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT untuk tabel `system_logs`
--
ALTER TABLE `system_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT untuk tabel `uploaded_data_records`
--
ALTER TABLE `uploaded_data_records`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `analysis_history`
--
ALTER TABLE `analysis_history`
  ADD CONSTRAINT `analysis_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `prediction_data`
--
ALTER TABLE `prediction_data`
  ADD CONSTRAINT `prediction_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `prediction_results`
--
ALTER TABLE `prediction_results`
  ADD CONSTRAINT `prediction_results_ibfk_1` FOREIGN KEY (`prediction_id`) REFERENCES `prediction_data` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `system_logs`
--
ALTER TABLE `system_logs`
  ADD CONSTRAINT `system_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Ketidakleluasaan untuk tabel `uploaded_data_records`
--
ALTER TABLE `uploaded_data_records`
  ADD CONSTRAINT `uploaded_data_records_ibfk_1` FOREIGN KEY (`prediction_id`) REFERENCES `prediction_data` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
