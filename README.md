# Project Skripsi

# 📊 Aplikasi Klasifikasi Efektivitas Intervensi Stunting di Desa

Aplikasi berbasis Streamlit untuk melakukan klasifikasi efektivitas respon intervensi stunting berdasarkan indikator kegiatan desa. Dataset menggunakan data dari Kementerian Desa PDTT tahun 2023.

---

## 🎯 Fitur

- 📁 Upload file Excel dengan format PDTT
- 🔄 Otomatis preprocessing dan labeling efektivitas
- 🌳 Klasifikasi menggunakan Decision Tree & Random Forest
- 📈 Visualisasi akurasi, confusion matrix, dan feature importance
- 🧠 Klasifikasi manual untuk 1 desa
- 🔍 Filter desa berdasarkan label efektivitas
- ⬇️ Download hasil klasifikasi sebagai Excel

---

## 🗂️ Struktur Folder pada branch ini

stunting\*classifier/
│
├── app.py # Halaman utama (navigasi)
├── requirements.txt
│
├── preprocessing.py
├── modeling.py
│
├── pages/ # Halaman khusus
│ ├── 1. FirstPage.py # Unggah file raw data dan preprocessing
│ ├── 2. SecondPage.py # Analisis Data
│ └── 3. ThirdPage.py # Modeling Klasifikasi

---

## 🛠️ Cara Menjalankan (Local)

1. **Clone / Buat Folder Project**

```bash
mkdir stunting-classifier && cd stunting-classifier
```

2. **Buat Virtual Environment**

```bash
   python -m venv env
```

3. **Aktifkan Environment**
   Windows :

```bash
env\Scripts\activate
```

    Mac/Linux :

```bash
source env/bin/activate
```

4. **Install Dependensi**

```bash
pip install -r requirements.txt
```

5. **Jalankan Aplikasi**

```bash
streamlit run app.py
```

📌 Ketentuan Dataset
Format Excel dengan header di baris ke-3.
Kolom indikator berisi kata kunci seperti “ada”, “rutin”, atau “aktif”.

📝 Sumber data : [Satu Data Indonesia](https://data.go.id/dataset/dataset/jumlah-penerima-layanan-pencegahan-stunting-tahun-2023)
