# Generated by Django 3.2 on 2024-06-08 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0006_proyectos_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyectos',
            name='ubicacion',
        ),
    ]