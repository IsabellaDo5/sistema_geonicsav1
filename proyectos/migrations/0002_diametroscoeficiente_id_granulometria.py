# Generated by Django 3.2 on 2024-06-08 00:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ensayos', '0006_ensayo_id_ordentrabajo'),
        ('proyectos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diametroscoeficiente',
            name='id_granulometria',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ensayos.granulometria'),
        ),
    ]
