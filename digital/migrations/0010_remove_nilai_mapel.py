# Generated by Django 3.1.2 on 2021-09-01 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digital', '0009_remove_rinciannilai_kode_nilai'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nilai',
            name='mapel',
        ),
    ]
