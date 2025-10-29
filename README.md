# Student Performance Tracker

Sistem tracking performa mahasiswa berbasis Python dengan fitur manajemen data mahasiswa, penilaian, dan laporan otomatis.

## 📋 Deskripsi

Aplikasi ini dirancang untuk membantu pengelolaan data akademik mahasiswa, mencakup:

- Data mahasiswa (NIM, nama, kehadiran)
- Penilaian (Quiz, Tugas, UTS, UAS)
- Rekap kelas otomatis
- Laporan dalam format Markdown

## 🎯 Tujuan Pembelajaran

Setelah menyelesaikan tugas ini, mampu:

1. ✅ Merancang kelas dan objek dengan relasi yang tepat
2. ✅ Menggunakan enkapsulasi untuk melindungi data
3. ✅ Menyusun ulang program menjadi paket modular dengan `__init__.py`
4. ✅ Menghasilkan laporan teks terformat otomatis
5. ✅ Menulis dokumentasi dasar (README.md, docstring, dan requirements.txt)

## 📁 Struktur Proyek

```
tugas89/
├── app.py                  # Program utama
├── README.md               # Dokumentasi proyek
├── requirements.txt        # Dependensi Python
├── data/
│   ├── attendance.csv      # Data kehadiran mahasiswa
│   └── grades.csv          # Data nilai mahasiswa
├── tracker/
│   ├── __init__.py         # Inisialisasi package
│   ├── mahasiswa.py        # Kelas Mahasiswa
│   ├── penilaian.py        # Kelas Penilaian
│   ├── rekap_kelas.py      # Kelas RekapKelas
│   └── report.py           # Fungsi laporan
└── out/
    └── report.md           # Output laporan (generated)
```

## 🚀 Instalasi

1. Clone repository atau download source code
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## 💻 Cara Penggunaan

Jalankan aplikasi:

```bash
python app.py
```

### Menu Aplikasi

1. **Muat data dari CSV** - Load data mahasiswa dari file CSV
2. **Tambah mahasiswa** - Tambahkan data mahasiswa baru
3. **Ubah presensi** - Update persentase kehadiran mahasiswa
4. **Ubah nilai** - Update nilai mahasiswa (Quiz, Tugas, UTS, UAS)
5. **Lihat rekap** - Tampilkan rekap kelas di terminal
6. **Simpan laporan markdown** - Generate laporan ke `out/report.md`

## 📚 Fitur

### 3.1. Data Mahasiswa (Kelas `Mahasiswa`)

- **Atribut**: `nim`, `nama`, `_hadir_persen`
- **Properti**: `hadir_persen` dengan validasi 0-100
- **Method**: `info()` untuk menampilkan profil mahasiswa

### 3.2. Data Penilaian (Kelas `Penilaian`)

- **Atribut**: `quiz`, `tugas`, `uts`, `uas`
- **Method**: `nilai_akhir()` dengan bobot:
  - Quiz: 15%
  - Tugas: 25%
  - UTS: 25%
  - UAS: 35%
- **Validasi**: Nilai 0-100

### 3.3. Manajer Rekap (Kelas `RekapKelas`)

Struktur data: `{nim: {'mhs': obj, 'nilai': obj}}`

**Fungsi tersedia**:

- `tambah_mahasiswa()` - Menambah mahasiswa baru
- `set_hadir()` - Set persentase kehadiran
- `set_penilaian()` - Set nilai mahasiswa
- `rekap()` - Generate list rekap kelas
- `predikat()` - Konversi nilai ke huruf (A-E)

### 3.4. Laporan

- `build_markdown_report(records)` - Generate tabel markdown
- `save_text(path, content)` - Simpan ke file .md
- Output: `out/report.md`

## 📊 Format Data CSV

### attendance.csv

```csv
nim,nama,week1,week2,week3,...
2301001,Andi Pratama,1,1,0,...
```

### grades.csv

```csv
nim,quiz,tugas,uts,uas
2301001,85,90,88,87
```

## 🎓 Predikat Nilai

| Nilai | Predikat |
| ----- | -------- |
| ≥ 85  | A        |
| ≥ 70  | B        |
| ≥ 55  | C        |
| ≥ 40  | D        |
| < 40  | E        |

## 👨‍💻 Author

**Kevien Ollyvie Jolanda**

- NIM: 230103197
- Kelas: 23TIA6

## 📝 Lisensi

Proyek ini dibuat untuk keperluan pembelajaran mata kuliah Pemrograman Berorientasi Objek.
