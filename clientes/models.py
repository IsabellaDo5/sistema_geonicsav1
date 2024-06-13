from django.db import models

# Create your models here.
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    telefono = models.IntegerField()

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

