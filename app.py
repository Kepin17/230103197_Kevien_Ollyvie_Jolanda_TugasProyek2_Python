from tracker.mahasiswa import Mahasiswa as mhs
from tracker.penilaian import Penilaian as nilai
from tracker.rekap_kelas import RekapKelas as rekap
from pathlib import Path
import csv

def load_csv(path):
  """Load CSV file and return list of dictionaries."""
  p = Path(path)
  with p.open(encoding="utf-8") as file:
    return list(csv.DictReader(file))

def bootstrap_from_csv(rekap, att_path, grd_path):
  """Bootstrap RekapKelas from CSV files."""
  att_data = load_csv(att_path)
  grd_data = load_csv(grd_path)

  for row in att_data:
    mahasiswa = mhs(
      row["nama"],
      row["nim"]
    )
    rekap.tambah_mahasiswa(mahasiswa)

    weeks = [key for key in row.keys() if key.startswith("week")]
    if weeks:
      total = len(weeks)
      hadir = 0
      for w in weeks:
        val = row[w].strip()
        if val != "":
          hadir += int(val)
      persen = round(hadir/ total * 100, 2)
      rekap.set_hadir(mahasiswa.nim, persen)
  
  by_nim = {}
  for g in grd_data:
    by_nim[g["nim"]] = g

  for nim in list(rekap._by_nim.keys()):
    g = by_nim.get(nim)
    if g:
      rekap.set_penilaian(
        nim,
        quiz=float(g.get("quiz", "0") or 0),
        tugas=float(g.get("tugas", "0") or 0),
        uts=float(g.get("uts", "0") or 0),
        uas=float(g.get("uas", "0") or 0)
      )

def tampilkan_rekap(rows):
  """Menampilkan rekap mahasiswa dalam format tabel."""
  print("\nNIM | Nama | Hadir% | Akhir | Pred")
  print("--------------------------------------------")
  for r in rows:
    print("{:<10} | {:<15} | {:>6.2f} | {:>5.2f} | {}".format(
      r['nim'], r['nama'], r['hadir'], r['akhir'], r['predikat'])
      )
  print()

def filter_nilai_rendah(rows, batas=70):
  """Filter mahasiswa dengan nilai akhir di bawah batas tertentu."""
  return [r for r in rows if r['akhir'] < batas]

def save_mahasiswa_to_csv(nim, nama, hadir_persen, att_path="data/attendance.csv"):
  """Simpan mahasiswa baru ke file CSV attendance.
  Mengkonversi persentase kehadiran menjadi data per minggu.
  """
  p = Path(att_path)
  
  # Baca data yang sudah ada
  existing_data = []
  fieldnames = ['nim', 'nama'] + [f'week{i}' for i in range(1, 9)]  # Default fieldnames
  
  if p.exists() and p.stat().st_size > 0:
    with p.open('r', encoding='utf-8') as f:
      reader = csv.DictReader(f)
      if reader.fieldnames:
        fieldnames = reader.fieldnames
      existing_data = list(reader)
  
  # Hitung jumlah minggu yang hadir berdasarkan persentase
  # Contoh: 87.5% dari 8 minggu = 7 minggu hadir
  total_weeks = len([f for f in fieldnames if f.startswith('week')])
  weeks_present = round(hadir_persen / 100 * total_weeks)
  
  # Buat row baru dengan week sesuai persentase
  new_row = {'nim': nim, 'nama': nama}
  week_count = 0
  for field in fieldnames:
    if field.startswith('week'):
      # Set 1 untuk minggu yang hadir, 0 untuk yang tidak
      new_row[field] = '1' if week_count < weeks_present else '0'
      week_count += 1
  
  # Tambahkan ke existing data
  existing_data.append(new_row)
  
  # Tulis kembali ke file
  with p.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(existing_data)

def update_attendance_to_csv(nim, hadir_persen, att_path="data/attendance.csv"):
  """Update kehadiran mahasiswa di file CSV attendance.
  Mengkonversi persentase kehadiran menjadi data per minggu.
  """
  p = Path(att_path)
  
  if not p.exists() or p.stat().st_size == 0:
    print("File attendance.csv tidak ditemukan atau kosong.")
    return False
  
  # Baca data yang sudah ada
  existing_data = []
  with p.open('r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    existing_data = list(reader)
  
  # Cari mahasiswa berdasarkan NIM
  nim_found = False
  for row in existing_data:
    if row['nim'] == nim:
      nim_found = True
      # Hitung jumlah minggu yang hadir berdasarkan persentase
      total_weeks = len([f for f in fieldnames if f.startswith('week')])
      weeks_present = round(hadir_persen / 100 * total_weeks)
      
      # Update week data
      week_count = 0
      for field in fieldnames:
        if field.startswith('week'):
          # Set 1 untuk minggu yang hadir, 0 untuk yang tidak
          row[field] = '1' if week_count < weeks_present else '0'
          week_count += 1
      break
  
  if not nim_found:
    print(f"NIM {nim} tidak ditemukan di file attendance.csv")
    return False
  
  # Tulis kembali ke file
  with p.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(existing_data)
  
  return True

def save_nilai_to_csv(nim, quiz=0, tugas=0, uts=0, uas=0, grd_path="data/grades.csv"):
  """Simpan nilai mahasiswa ke file CSV grades."""
  p = Path(grd_path)
  
  # Baca data yang sudah ada
  existing_data = []
  fieldnames = ['nim', 'quiz', 'tugas', 'uts', 'uas']
  
  if p.exists() and p.stat().st_size > 0:
    with p.open('r', encoding='utf-8') as f:
      reader = csv.DictReader(f)
      existing_data = list(reader)
  
  # Cek apakah NIM sudah ada
  nim_exists = False
  for row in existing_data:
    if row['nim'] == nim:
      # Update nilai yang ada
      row['quiz'] = str(quiz)
      row['tugas'] = str(tugas)
      row['uts'] = str(uts)
      row['uas'] = str(uas)
      nim_exists = True
      break
  
  # Jika NIM belum ada, tambahkan row baru
  if not nim_exists:
    new_row = {
      'nim': nim,
      'quiz': str(quiz),
      'tugas': str(tugas),
      'uts': str(uts),
      'uas': str(uas)
    }
    existing_data.append(new_row)
  
  # Tulis kembali ke file
  with p.open('w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(existing_data)

def menu():
  r = rekap()
  while True:
    print("===============================")
    print("  Student Performance Tracker  ")
    print("===============================")
    print("""
1) Muat data dari CSV
2) Tambah mahasiswa
3) Ubah presensi
4) Ubah nilai
5) Lihat rekap
6) Lihat mahasiswa nilai < 70
7) Simpan laporan markdown
8) Simpan laporan HTML
""")
    pilihan = input("Pilih menu (1-8) atau 'q' untuk keluar: ")
    if pilihan == '1':
      bootstrap_from_csv(r, "data/attendance.csv", "data/grades.csv")
      print("Data berhasil dimuat.")
    elif pilihan == '2':
      print("\n=== Tambah Mahasiswa Baru ===")
      nim = input("NIM: ")
      nama = input("Nama: ")
      hadir = float(input("Kehadiran (%): "))
      
      print("\n--- Input Nilai ---")
      quiz = float(input("Nilai Quiz (0-100): "))
      tugas = float(input("Nilai Tugas (0-100): "))
      uts = float(input("Nilai UTS (0-100): "))
      uas = float(input("Nilai UAS (0-100): "))
      
      # Buat objek mahasiswa
      m = mhs(nama, nim)
      m.hadir_persen = hadir
      r.tambah_mahasiswa(m)
      
      # Set nilai mahasiswa
      r.set_penilaian(nim, quiz, tugas, uts, uas)
      
      # Simpan ke CSV
      save_mahasiswa_to_csv(nim, nama, hadir)
      save_nilai_to_csv(nim, quiz, tugas, uts, uas)
      
      print("\n✓ Mahasiswa berhasil ditambahkan dan disimpan ke CSV.")
    elif pilihan == '3':
      nim = input("NIM mahasiswa: ")
      hadir = int(input("Kehadiran baru (%): "))
      try:
        r.set_hadir(nim, hadir)
        
        # Simpan ke CSV
        if update_attendance_to_csv(nim, hadir):
          print("Kehadiran berhasil diubah dan disimpan ke CSV.")
        else:
          print("Kehadiran berhasil diubah dalam sistem, tapi gagal menyimpan ke CSV.")
      except ValueError as e:
        print(f"Error: {e}")
        print("Pastikan NIM sudah terdaftar dalam sistem.")
    elif pilihan == '4':
      nim = input("NIM mahasiswa: ")
      quiz = float(input("Nilai Quiz: "))
      tugas = float(input("Nilai Tugas: "))
      uts = float(input("Nilai UTS: "))
      uas = float(input("Nilai UAS: "))
      try:
        # Menggunakan import nilai untuk membuat objek Penilaian
        penilaian_obj = nilai(quiz, tugas, uts, uas)
        r.set_penilaian(nim, quiz, tugas, uts, uas)
        
        # Simpan ke CSV
        save_nilai_to_csv(nim, quiz, tugas, uts, uas)
        
        print("Nilai berhasil diubah dan disimpan ke CSV.")
      except ValueError as e:
        print(f"Error: {e}")
        print("Pastikan NIM sudah terdaftar dalam sistem.")
    elif pilihan == '5':
      rows = r.rekap()
      tampilkan_rekap(rows)
    elif pilihan == '6':
      rows = r.rekap()
      filtered = filter_nilai_rendah(rows, 70)
      if filtered:
        print("\n=== Mahasiswa dengan Nilai < 70 ===")
        tampilkan_rekap(filtered)
        print(f"Total: {len(filtered)} mahasiswa perlu perhatian khusus")
      else:
        print("\n✓ Tidak ada mahasiswa dengan nilai < 70")
    elif pilihan == '7':
      from tracker.report import build_markdown_report, save_text
      rows = r.rekap()
      report_content = build_markdown_report(rows)
      save_text("out/report.md", report_content)
      print("Laporan markdown berhasil disimpan sebagai 'out/report.md'.")
    elif pilihan == '8':
      from tracker.report import build_html_report, save_text
      rows = r.rekap()
      html_content = build_html_report(rows)
      save_text("out/report.html", html_content)
      print("Laporan HTML berhasil disimpan sebagai 'out/report.html'.")
    elif pilihan.lower() == 'q' or pilihan == '9':
      print("Keluar dari program.")
      break  

def main():
  menu()

if __name__ == "__main__":
  main()

  




 