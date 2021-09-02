from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Guru(models.Model):
    nip = models.CharField(max_length=200, unique =True, null=True)
    nama = models.CharField(max_length=200, blank=True, null=True)
    alamat = models.CharField(max_length=200, blank=True, null=True)
    tgl_lahir = models.DateField(auto_now=False, auto_now_add=False)
    telpon = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    user = models.OneToOneField(User, blank =True, null=True, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.nama
    class Meta:
        verbose_name_plural = "Guru"

class Siswa(models.Model):
    nis = models.CharField(max_length=200, unique =True, null=True)
    nama = models.CharField(max_length=200, blank=True, null=True)
    alamat = models.CharField(max_length=200, blank=True, null=True)
    tgl_lahir = models.DateField(auto_now=False, auto_now_add=False)
    wali_kelas = models.ForeignKey(Guru, blank=True, null=True, on_delete=models.SET_NULL)
    user = models.OneToOneField(User, blank =True, null=True, on_delete = models.CASCADE)

    def __str__(self):
        return self.nama 
    class Meta:
        verbose_name_plural = "Siswa"

class Mapel(models.Model):
    kode_mapel = models.CharField(max_length=200, unique =True, null=True)
    nama_mapel = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nama_mapel
    class Meta:
        verbose_name_plural = "Mapel"

class RincianNilai(models.Model):
    nama_mapel = models.ForeignKey(Mapel, blank=True, null=True, on_delete=models.SET_NULL)
    rincian_nilai = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.rincian_nilai
    class Meta:
         verbose_name_plural = "RincianNilai"

class Nilai(models.Model):
    Kelas = (
        ('Kelompok A', 'Kelompok A'),
        ('Kelompok B', 'Kelompok B'),
    )
    Semester = (
        ('GANJIL', 'GANJIL'),
        ('GENAP', 'GENAP'),
    )
    siswa = models.ForeignKey(Siswa, blank=True, null=True, on_delete=models.SET_NULL)
    kelompok = models.CharField(max_length=200, null=True, choices=Kelas)
    semester = models.CharField(max_length=200, null=True, choices=Semester)
    tahun_ajaran = models.CharField(max_length=200, blank=True, null=True)
    rincian_nilai = models.ForeignKey(RincianNilai, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "%s" %(self.siswa)
    class Meta:
         verbose_name_plural = "Nilai"
