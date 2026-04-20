# dicoding-data

# 🚲 Bike Sharing Data Analysis Project

## 📌 Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis pola penggunaan layanan **bike sharing** berdasarkan dataset tahun 2011–2012. Analisis dilakukan untuk memahami distribusi penggunaan serta tren penyewaan sepeda antara hari kerja dan hari libur.

Hasil analisis disajikan dalam bentuk:

* 📓 Notebook analisis data (EDA & insight)
* 📊 Dashboard interaktif menggunakan Streamlit

---

## 🎯 Pertanyaan Bisnis

1. Bagaimana distribusi kategori tingkat penggunaan sepeda (rendah, sedang, tinggi) berdasarkan jumlah penyewaan (cnt) selama periode 2011–2012?
2. Bagaimana tren perubahan jumlah penyewaan sepeda (cnt) antara hari kerja (workingday) dan hari libur dalam periode 2011–2012, serta kapan terjadi peningkatan atau penurunan signifikan?

---

## 🗂️ Struktur Direktori

```
submission/
├── dashboard/
│   ├── main_data.csv
│   └── dashboard.py
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

---

## ⚙️ Proses Analisis Data

### 1. Data Wrangling

* Mengambil dataset dari Kaggle
* Menggabungkan dan memahami struktur data
* Membersihkan data dan mengubah tipe data

### 2. Exploratory Data Analysis (EDA)

* Melihat distribusi data
* Mengidentifikasi pola awal
* Menganalisis hubungan antar variabel

### 3. Visualization & Explanatory Analysis

* Visualisasi distribusi kategori penggunaan
* Analisis tren penyewaan sepeda
* Perbandingan antara hari kerja dan hari libur
* Identifikasi titik peak dan drop

### 4. Analisis Lanjutan

* Clustering sederhana menggunakan teknik **binning (qcut)**
* Mengelompokkan penggunaan menjadi Low, Medium, High

---

## 📊 Insight Utama

* Mayoritas penggunaan sepeda berada pada kategori **Medium dan High**
* Hari kerja memiliki pola penggunaan yang lebih **stabil dan tinggi**
* Hari libur menunjukkan **fluktuasi yang lebih besar**
* Terdapat **pola musiman** dalam penggunaan sepeda
* Terdapat perbedaan signifikan antara hari dengan penyewaan tertinggi dan terendah

---

## 📈 Dashboard

Dashboard dibuat menggunakan **Streamlit** untuk menyajikan hasil analisis secara interaktif.

Fitur utama:

* Filter data berdasarkan tanggal
* Visualisasi distribusi penggunaan
* Tren penyewaan sepeda
* Analisis peak & drop
* Insight langsung pada setiap visualisasi

---

## ▶️ Cara Menjalankan Dashboard

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Jalankan Streamlit:

```
streamlit run dashboard/dashboard.py
```

3. Buka browser:

```
http://localhost:8501
```

---

## 🌐 Deployment

Link dashboard online tersedia di file:

```
url.txt
```

---

## 👤 Author

Nama: Sabrina Marliani
Email: cdcc156d6x1770@student.devacademy.id
ID Dicoding: cdcc156d6x1770

---

## 📌 Catatan

Proyek ini dibuat sebagai bagian dari submission kelas Analisis Data Dicoding.

