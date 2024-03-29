# Generated by Django 3.1.3 on 2021-07-26 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kelas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kelas', models.CharField(blank=True, choices=[('Kelas A', 'Kelas A'), ('Kelas B', 'Kelas B')], max_length=200, null=True)),
                ('semester', models.CharField(blank=True, choices=[('Ganjil', 'Ganjil'), ('Genap', 'Genap')], max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Kelas',
            },
        ),
        migrations.CreateModel(
            name='Mapel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_mapel', models.CharField(max_length=200, null=True, unique=True)),
                ('nama_mapel', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Mapel',
            },
        ),
        migrations.CreateModel(
            name='RincianNilai',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_nilai', models.CharField(max_length=200, null=True, unique=True)),
                ('rincian_nilai', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'RincianNilai',
            },
        ),
        migrations.CreateModel(
            name='Siswa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nis', models.CharField(max_length=200, null=True, unique=True)),
                ('nama', models.CharField(blank=True, max_length=200, null=True)),
                ('alamat', models.CharField(blank=True, max_length=200, null=True)),
                ('tgl_lahir', models.DateField()),
                ('kelas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='digital.kelas')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Siswa',
            },
        ),
        migrations.CreateModel(
            name='Guru',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nip', models.CharField(max_length=200, null=True, unique=True)),
                ('nama', models.CharField(blank=True, max_length=200, null=True)),
                ('alamat', models.CharField(blank=True, max_length=200, null=True)),
                ('tgl_lahir', models.DateField()),
                ('telpon', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(blank=True, max_length=200, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Guru',
            },
        ),
    ]
