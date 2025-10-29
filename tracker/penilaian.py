class Penilaian:
  """"Class untuk menyimpan dan mengelola penilaian mahasiswa."""
  def __init__(self, quiz=0, tugas=0,uts=0, uas=0):
    self._quiz = 0.0
    self._tugas = 0.0
    self._uts = 0.0
    self._uas = 0.0
    self.quiz = quiz
    self.tugas = tugas
    self.uts = uts
    self.uas = uas
  
  def _validate(self, value):
    """Validasi nilai agar berada dalam rentang 0 hingga 100."""
    if value < 0 or value > 100:
      raise ValueError("Nilai harus antara 0 hingga 100")
    return float(value)
  
  @property
  def quiz(self):
    """Getter untuk nilai quiz."""
    return self._quiz
  @quiz.setter
  def quiz(self, value):
    """Setter untuk nilai quiz dengan validasi."""
    self._quiz = self._validate(value)
  
  @property
  def tugas(self):
    """Getter untuk nilai tugas."""
    return self._tugas
  @tugas.setter
  def tugas(self, value):
    """Setter untuk nilai tugas dengan validasi."""
    self._tugas = self._validate(value)
  
  @property
  def uts(self):
    """Getter untuk nilai UTS."""
    return self._uts
  @uts.setter
  def uts(self, value):
    """Setter untuk nilai UTS dengan validasi."""
    self._uts = self._validate(value)
  
  @property
  def uas(self):
    """Getter untuk nilai UAS."""
    return self._uas
  @uas.setter
  def uas(self, value):
    """Setter untuk nilai UAS dengan validasi."""
    self._uas = self._validate(value)

  def nilai_akhir(self, w_quiz=0.15, w_tugas=0.25, w_uts=0.25, w_uas=0.35):
      """Menghitung nilai akhir berdasarkan bobot yang diberikan.
      Default: Quiz 15%, Tugas 25%, UTS 25%, UAS 35%
      """
      nilai_akhir = (
          self.quiz * w_quiz +
          self.tugas * w_tugas +
          self.uts * w_uts +
          self.uas * w_uas
      )
      return round(nilai_akhir, 2)

  def __repr__(self):
      
      return (f"Penilaian(quiz={self.quiz}, tugas={self.tugas}, "
              f"uts={self.uts}, uas={self.uas}, "
              f"nilai_akhir={self.nilai_akhir()})")