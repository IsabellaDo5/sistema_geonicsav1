# Generated by Django 3.2 on 2024-06-09 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0007_remove_proyectos_ubicacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordentrabajo',
            name='estado',
            field=models.CharField(default='activo', max_length=10),
            preserve_default=False,
        ),
    ]