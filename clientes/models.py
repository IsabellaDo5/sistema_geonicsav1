from django.db import models

# Create your models here.
class Clientes(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    telefono = models.IntegerField()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

