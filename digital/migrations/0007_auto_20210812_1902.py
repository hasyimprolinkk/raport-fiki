# Generated by Django 3.1.2 on 2021-08-12 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('digital', '0006_nilai_wali_kelas'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nilai',
            name='wali_kelas',
        ),
        migrations.AddField(
            model_name='siswa',
            name='wali_kelas',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='digital.guru'),
        ),
    ]
