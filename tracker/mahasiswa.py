class Mahasiswa:
  """
  Class Mahasiswa untuk merepresentasikan data mahasiswa dengan atribut nim, nama, dan hadir_persen.
  """
  def __init__(self, nama, nim):
    """Inisialisasi objek Mahasiswa dengan nama dan nim."""
    self.nim = nim
    self.nama = nama  
    self._hadir_persen = 0.0

  @property
  def hadir_persen(self):
    """Getter untuk atribut hadir_persen."""
    return self._hadir_persen
  @hadir_persen.setter
  def hadir_persen(self, value):
    """Setter untuk atribut hadir_persen dengan validasi nilai antara 0 dan 100."""
    if value < 0 or value > 100:
      raise ValueError("Persentase kehadiran harus antara 0 dan 100")
    self._hadir_persen = float(value)
  
  def info(self):
    """Mengembalikan informasi lengkap tentang mahasiswa."""
    return f"Nama: {self.nama}, NIM: {self.nim}, Kehadiran: {self.hadir_persen}%"

