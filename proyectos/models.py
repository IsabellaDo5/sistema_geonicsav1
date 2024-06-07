from django.db import models

class DiametrosCoeficiente(models.Model):
    d10 = models.DecimalField(max_digits=10, decimal_places=2)
    d30 = models.DecimalField(max_digits=10, decimal_places=2)
    d60 = models.DecimalField(max_digits=10, decimal_places=2)
    cu = models.DecimalField(max_digits=10, decimal_places=2)
    cc = models.DecimalField(max_digits=10, decimal_places=2)

class Proyectos(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    cliente = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255)

class OrdenTrabajo(models.Model):
    id_ordenTrabajo = models.AutoField(primary_key=True)
    no_orden = models.IntegerField()
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)