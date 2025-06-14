# 📦 ETL Pipeline: Data Fashion Studio

## 📍 Deskripsi Proyek
ETL Pipeline ini dibuat untuk memenuhi submission kelas dari Dicoding. Proyek ini bertujuan mengekstrak data fashion dari situs [https://fashion-studio.dicoding.dev](https://fashion-studio.dicoding.dev), melakukan transformasi data, dan memuat data bersih ke dalam dua format: **CSV** dan **Google Sheets**.

## 🧪 Fitur Utama
- 🔄 **Extract**: Mengambil data fashion kompetitor dari API eksternal.
- 🧹 **Transform**: Membersihkan dan memformat data.
- 💾 **Load**: Menyimpan hasil transformasi ke file `products.csv` dan Google Sheets.
- ✅ **Unit Test**: Masing-masing komponen (`extract`, `transform`, `load`) telah diuji dengan *test coverage*.

## 🗂️ Struktur Folder
.
├── main.py # Pipeline utama
├── utils/ # Fungsi modular (extract, transform, load)
│ └── extract.py
│ └── transform.py
│ └── load.py
├── test/ # Unit test masing-masing tahap
│ └── extract_test.py
│ └── transform_test.py
│ └── load_test.py
├── products.csv # Output file hasil load
├── .gitignore # File/folder yang tidak diikutsertakan di Git
├── requirements.txt # Dependency yang dibutuhkan proyek
└── README.md # Dokumentasi proyek ini



## ⚙️ Cara Menjalankan

1. **Clone repo**:
   ```bash
   git clone https://github.com/Ranfl/ETL-Pipeline.git
   cd ETL-Pipeline

Install dependency:
```bash
pip install -r requirements.txt
```

Buat file .env berisi:
```
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_SERVICE_ACCOUNT=your_credentials.json
```

Jalankan pipeline utama:
```
python main.py
```

🧪 Pengujian
Untuk menjalankan unit test dan melihat coverage:
```
pytest --cov=utils test/
```


📊 Sumber Data
Data fashion diambil dari API Dicoding:

🔗 https://fashion-studio.dicoding.dev

🧑‍💻 Kontributor
Rasyid Naufal (@Ranfl)
Submission — Dicoding x DBS Foundation
STIMIK Tunas Bangsa | Informatika
