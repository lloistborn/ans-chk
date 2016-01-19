from django.db import models
from django.utils.encoding import python_2_unicode_compatible

class Soal(models.Model):
	@python_2_unicode_compatible
	def __str__(self):
		return self.soal

	soal = models.TextField()
	jawaban = models.TextField()
	
class Siswa(models.Model):
	@python_2_unicode_compatible
	def __str__(self):
		return self.nama

	nama = models.CharField(max_length = 50)
	nomor_induk = models.IntegerField(default = 0)
	tanggal_reg = models.DateTimeField('tanggal registrasi')
		
class Hasil(models.Model):
	@python_2_unicode_compatible
	def __str__(self):
		return self.siswa.nama

	siswa = models.ForeignKey(Siswa, on_delete = models.CASCADE)
	soal = models.ForeignKey(Soal, on_delete = models.CASCADE)
	skor = models.FloatField(default = 0.0)