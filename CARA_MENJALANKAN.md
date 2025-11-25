# 🚀 Cara Menjalankan Project PREDICTEL

## Persyaratan

- Python 3.8 atau lebih tinggi
- pip (package manager Python)

## Langkah-langkah

### 1. Aktifkan Virtual Environment

**Untuk PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**Untuk Command Prompt (CMD):**

```cmd
venv\Scripts\activate.bat
```

**Catatan:** Jika virtual environment bermasalah, buat ulang dengan:

```powershell
# Hapus folder venv yang lama (opsional)
Remove-Item -Recurse -Force venv

# Buat virtual environment baru
python -m venv venv

# Aktifkan
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

Setelah virtual environment aktif, install semua package yang diperlukan:

```powershell
pip install -r requirements.txt
```

Atau install secara manual:

```powershell
pip install streamlit>=1.51.0 pandas>=2.0.0 numpy>=1.24.0 matplotlib>=3.7.0 seaborn>=0.12.0 scikit-learn>=1.3.0 Pillow>=10.0.0
```

### 3. Jalankan Aplikasi

Setelah semua dependencies terinstall, jalankan aplikasi Streamlit:

```powershell
streamlit run Home.py
```

Aplikasi akan otomatis terbuka di browser pada alamat:

- **Local URL:** http://localhost:8501
- **Network URL:** (akan ditampilkan di terminal)

### 4. Menggunakan Aplikasi

1. **Home** - Halaman utama dengan informasi tentang sistem
2. **Input Data** - Upload file CSV dataset Telco Customer Churn
3. **Processing Data** - Preprocessing dan encoding data
4. **Test Data** - Melatih model dan melakukan prediksi
5. **Data Visualization** - Visualisasi data dan hasil analisis
6. **About Us** - Informasi tentang tim pengembang

## Troubleshooting

### Error: "Unable to create process"

- **Solusi:** Virtual environment perlu dibuat ulang karena path berubah
- Hapus folder `venv` dan buat ulang dengan `python -m venv venv`

### Error: "streamlit: command not found"

- **Solusi:** Pastikan virtual environment aktif dan dependencies sudah terinstall
- Jalankan: `pip install -r requirements.txt`

### Error: "Module not found"

- **Solusi:** Install module yang missing dengan `pip install <nama-module>`

### Port 8501 sudah digunakan

- **Solusi:** Gunakan port lain dengan: `streamlit run Home.py --server.port 8502`

## Struktur Project

```
PREDICTEL/
├── Home.py                 # Halaman utama
├── style.py                # Styling global
├── requirements.txt        # Dependencies
├── pages/
│   ├── Input_Data.py      # Input data
│   ├── Preprocessing_Data.py  # Preprocessing
│   ├── Test_Data.py       # Testing & Prediction
│   ├── Visualisasi_Data.py # Visualization
│   └── About_Us.py        # About page
└── image/                 # Assets gambar
```

## Catatan Penting

- Pastikan file dataset CSV sudah siap sebelum menggunakan fitur Input Data
- Model akan dilatih otomatis saat menggunakan fitur Test Data
- Semua hasil visualisasi dapat di-download dari halaman Data Visualization
