# Create your models here.
from django.db import models

class Area(models.Model):
    codigo_area = models.CharField(max_length=255, unique=True)
    nombre_area = models.TextField()

class Ensayo(models.Model):
    codigo_area = models.ForeignKey(Area, on_delete=models.CASCADE)
    nombre_proyecto = models.TextField()
    cliente = models.TextField(null=True)
    operador = models.TextField(null=True)
    descripcion = models.TextField()
    no_sondeo = models.IntegerField()
    no_muestra = models.IntegerField(null=True)
    profundidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    tipo = models.TextField(null=True)

class Mallas(models.Model):
    id_malla = models.IntegerField(primary_key=True)
    medida = models.TextField()
    medida_mm = models.DecimalField(max_digits=10, decimal_places=3, null=True)


class Granulometria(models.Model):
    id_ensayo = models.ForeignKey(Ensayo, on_delete=models.CASCADE)
    id_malla = models.ForeignKey(Mallas, on_delete=models.CASCADE)
    PRP = models.DecimalField(max_digits=10, decimal_places=2)
    PeRP = models.DecimalField(max_digits=10, decimal_places=2)
    PRA = models.DecimalField(max_digits=10, decimal_places=2)
    PeQP = models.DecimalField(max_digits=10, decimal_places=2)

class FactoresLL(models.Model):
    id_factor = models.IntegerField(primary_key=True)
    N = models.IntegerField()
    K = models.DecimalField(max_digits=10, decimal_places=2)

class LimiteLiquido(models.Model):
    id_ensayo = models.ForeignKey(Ensayo, on_delete=models.CASCADE)
    no_golpes = models.IntegerField()
    recipiente_no = models.IntegerField()
    pw_mas_recip = models.FloatField()
    ps_mas_recip = models.FloatField()
    agua = models.FloatField()
    ps_mas_recip2 = models.FloatField()
    recipiente = models.DecimalField(max_digits=10, decimal_places=2)
    peso_seco = models.FloatField()
    Pe_agua = models.FloatField()
    id_factor = models.ForeignKey(FactoresLL, on_delete=models.CASCADE)
    limite_liquido = models.FloatField()

class LimitePlastico(models.Model):
    id_ensayo = models.ForeignKey(Ensayo, on_delete=models.CASCADE)
    recipiente_no = models.IntegerField()
    pw_mas_recip = models.FloatField()
    ps_mas_recip = models.FloatField()
    agua = models.FloatField()
    ps_mas_recip2 = models.FloatField()
    recipiente = models.DecimalField(max_digits=10, decimal_places=2)
    peso_seco = models.FloatField()
    limite_plastico = models.FloatField()
