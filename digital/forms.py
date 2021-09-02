from django import forms
from django.forms import ModelForm, DateTimeInput
from .models import *


class SiswaForm(ModelForm):
    class Meta:
        model = Siswa
        fields = [
            'nis', 
            'nama', 
            'alamat', 
            'tgl_lahir',
            'wali_kelas'
            ]
        exclude = ['user']

        widgets = {
            'nis' : forms.TextInput(attrs={'class': 'form-select'}),
            'nama' : forms.TextInput(attrs={'class': 'form-control'}),
            'alamat': forms.TextInput(attrs={'class': 'form-control'}),
            'tgl_lahir' : forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}),
            'wali_kelas' : forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nis' : 'NIS',
            'nama' : 'Nama Siswa',
            'alamat' : 'Alamat',
            'tgl_lahir' : 'Tanggal Lahir',
            'wali_kelas' : 'Wali Kelas',
        }
        

class GuruForm(ModelForm):
    class Meta:
        model = Guru
        fields = [
            'nip', 
            'nama', 
            'alamat', 
            'tgl_lahir', 
            'telpon', 
            'email'
            ]
        exclude = ['user']

        widgets = {
            'nip' : forms.TextInput(attrs={'class': 'form-select'}),
            'nama' : forms.TextInput(attrs={'class': 'form-control'}),
            'alamat': forms.TextInput(attrs={'class': 'form-control'}),
            'tgl_lahir' : forms.DateInput(format = '%Y-%m-%d',attrs={'type': 'date'}),
            'telpon' : forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}),
        }
        labels = {
            'nip' : 'NIP',
            'nama' : 'Nama Guru',
            'alamat' : 'Alamat',
            'tgl_lahir' : 'Tanggal Lahir',
            'telpon' : 'Nomor telepon',
            'email' : 'Email',
        }

class MapelForm(ModelForm):
    class Meta:
        model = Mapel
        fields = ['kode_mapel', 'nama_mapel']

        widgets = {
            'kode_mapel' : forms.TextInput(attrs={'class': 'form-control'}),
            'nama_mapel' : forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'kode_mapel' : 'Kode Mapel',
            'nama_mapel' : 'Nama Mapel',
        }

class RincianNilaiForm(ModelForm):
    class Meta:
        model = RincianNilai
        fields = ['nama_mapel', 'rincian_nilai']

        widgets = {
            'nama_mapel' : forms.Select(attrs={'class': 'form-select'}),
            'rincian_nilai' : forms.Textarea(attrs={'class': 'form-control','type': 'textarea'}),
        }
        labels = {
            'nama_mapel' : 'Nama Mata Pelajran',
            'rincian_nilai' : 'Rincian Nilai',
        }

class NilaiForm(ModelForm):
    class Meta:
        model = Nilai
        fields = '__all__'
        widgets = {
            'siswa' : forms.Select(attrs={'class': 'form-select'}),
            'kelompok' : forms.Select(attrs={'class': 'form-select'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'tahun_ajaran': forms.TextInput(attrs={'class': 'form-control'}),
            'rincian_nilai' : forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'siswa' : 'Siswa',
            'kelompok' : 'Kelompok',
            'semester' : 'Semester',
            'tahun_pelajaran' : 'Tahun Pelajaran',
            'rincian_nilai' : 'Rincian Nilai',
        }

