# Generated by Django 3.1.2 on 2021-09-01 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digital', '0008_rinciannilai_nama_mapel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rinciannilai',
            name='kode_nilai',
        ),
    ]
