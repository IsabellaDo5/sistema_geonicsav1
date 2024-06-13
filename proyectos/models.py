from django.db import models

class Proyectos(models.Model):
    id_proyecto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    ubicacion = models.CharField(max_length=255)
    descripcion = models.TextField()
    id_cliente = models.ForeignKey('clientes.Clientes', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class ServiciosPorProyecto(models.Model):
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    id_servicio = models.ForeignKey('ensayos.Servicio', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_proyecto', 'id_servicio')


class OrdenDeTrabajo(models.Model):
    id_ordenTrabajo = models.AutoField(primary_key=True)
    no_orden = models.IntegerField()
    id_proyecto = models.ForeignKey(Proyectos, on_delete=models.CASCADE)
    estado = models.IntegerField()

    def __str__(self):
        return f"Orden {self.no_orden} - Proyecto {self.id_proyecto}"
