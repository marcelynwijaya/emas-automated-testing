# 🥇 Gold Analytics Dashboard with Automated Testing

[![Python Flask CI](https://github.com/marcelynwijaya/emas-automated-testing/actions/workflows/main.yml/badge.svg)](https://github.com/marcelynwijaya/emas-automated-testing/actions)
![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen)

## 📋 Deskripsi Aplikasi
Aplikasi ini adalah dashboard analitika perilaku dan tren media sosial X terhadap pergerakan harga emas di Indonesia. Menggunakan algoritma **LMKNN (Local Mean K-Nearest Neighbor)** untuk klasifikasi sentimen publik.

## 🚀 Fitur Utama
1. **Prediksi Sentimen Real-Time:** Mengklasifikasikan cuitan menjadi Positif, Negatif, atau Netral.
2. **Dashboard Visualisasi:** Menampilkan distribusi sentimen, top kata, dan tren aktivitas cuitan.
3. **Automated Preprocessing:** Pembersihan teks otomatis sebelum analisis.

## 🛠️ Teknologi yang Digunakan
- **Bahasa:** Python 3.9
- **Framework Web:** Flask
- **Machine Learning:** Scikit-Learn (LMKNN Model)
- **Testing:** Pytest & Pytest-cov
- **CI/CD:** GitHub Actions

## 🧪 Cara Menjalankan Test
Pastikan semua library terinstall, lalu jalankan perintah berikut di terminal:
```bash
# Menjalankan semua test
pytest

# Menjalankan test dengan laporan coverage
pytest --cov=processor --cov=app tests/