# Generated by Django 3.2 on 2024-06-08 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0007_diametroscoeficiente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diametroscoeficiente',
            name='id_granulometria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ensayos.ensayo'),
        ),
    ]