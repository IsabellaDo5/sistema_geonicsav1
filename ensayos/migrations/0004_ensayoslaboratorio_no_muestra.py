# Generated by Django 4.2.13 on 2024-06-20 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0003_ensayoslaboratorio_id_servicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='ensayoslaboratorio',
            name='no_muestra',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]