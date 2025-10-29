class RekapKelas:
  """"Kelas untuk merekap data kelas.
  Menyimpan banyak objek Mahasiswa dan Penilaian.
  Menggunakan struktur: {nim: {'mhs': obj, 'nilai': obj}}
  """
  def __init__(self):
    self._by_nim = {}

  def tambah_mahasiswa(self, mahasiswa):
    """Menambahkan mahasiswa baru ke rekap kelas."""
    if mahasiswa.nim not in self._by_nim:
      self._by_nim[mahasiswa.nim] = {
          "mhs": mahasiswa,
          "nilai": None
      }

  def tambah_siswa(self, nim, name):
    """Menambahkan siswa baru ke rekap kelas (backward compatibility)."""
    from .mahasiswa import Mahasiswa
    if nim not in self._by_nim:
      mhs_obj = Mahasiswa(name, nim)
      self._by_nim[nim] = {
          "mhs": mhs_obj,
          "nilai": None
      }

  def set_hadir(self, nim, persen):
    """Mengatur persentase kehadiran mahasiswa."""
    item = self._by_nim.get(nim)
    if not item:
      raise ValueError("NIM tidak ditemukan")
    item["mhs"].hadir_persen = persen

  def set_penilaian(self, nim, quiz=None, tugas=None, uts=None, uas=None):
    """Mengatur penilaian untuk siswa berdasarkan NIM."""
    item = self._by_nim.get(nim)
    if not item:
        raise ValueError("NIM tidak ditemukan")
    
    # Inisialisasi penilaian jika belum ada
    if item["nilai"] is None:
        from .penilaian import Penilaian
        item["nilai"] = Penilaian()

    p = item["nilai"]
    if quiz is not None:
        p.quiz = quiz
    if tugas is not None:
        p.tugas = tugas
    if uts is not None:
        p.uts = uts
    if uas is not None:
        p.uas = uas

  def predikat(self,skor):
    """Menentukan predikat berdasarkan skor."""
    if skor >= 85:
      return "A"
    elif skor >= 70:
      return "B"
    elif skor >= 55:
      return "C"
    elif skor >= 40:
      return "D"
    else:
      return "E"
    
  def rekap(self):
    """Merekap data kelas dan mengembalikan daftar hasil."""
    hasil = []
    for nim, data in self._by_nim.items():
      mhs_obj = data["mhs"]
      p = data["nilai"]
      if p is None:
        continue
      nilai_akhir = p.nilai_akhir()
      hasil.append({
          "nim": nim,
          "nama": mhs_obj.nama,
          "hadir": mhs_obj.hadir_persen,
          "akhir": nilai_akhir,
          "predikat": self.predikat(nilai_akhir)
      })
    return hasil