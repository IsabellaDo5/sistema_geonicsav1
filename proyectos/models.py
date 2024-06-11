from django.db import models


class Proyectos(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    cliente = models.CharField(max_length=255)
    telefono = models.IntegerField()
    descripcion = models.CharField(max_length=255)

class OrdenTrabajo(models.Model):
    id_ordenTrabajo = models.AutoField(primary_key=True)
    no_orden = models.IntegerField()
    proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10)