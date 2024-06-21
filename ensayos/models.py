# Create your models here.
from django.db import models
from proyectos.models import Proyectos

class Area(models.Model):
    codigo_area = models.CharField(max_length=255, unique=True)
    nombre_area = models.TextField()

class Servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    servicio = models.CharField(max_length=40)
    codigo_area = models.ForeignKey(Area, on_delete=models.CASCADE)
    url_agregar = models.CharField(max_length=80, null=True)
    def __str__(self):
        return self.servicio

class EnsayosLaboratorio(models.Model):
    id_ensayo = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey('clientes.Clientes', on_delete=models.CASCADE)
    operador = models.CharField(max_length=60)
    descripcion_visual = models.TextField()
    no_sondeo = models.IntegerField()
    no_muestra = models.IntegerField()
    profundidad = models.IntegerField()
    fecha = models.DateField()
    id_servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    id_proyecto = models.ForeignKey('proyectos.Proyectos', on_delete=models.CASCADE)

    def __str__(self):
        return f"Ensayo {self.id_ensayo} - Proyecto {self.id_proyecto}"

class Mallas(models.Model):
    id_malla = models.IntegerField(primary_key=True)
    medida = models.TextField()
    medida_mm = models.DecimalField(max_digits=10, decimal_places=3, null=True)

    def __str__(self):
        return f'{self.id_malla}, {self.medida}, {self.medida_mm}'

class Granulometria(models.Model):
    id_ensayo = models.ForeignKey(EnsayosLaboratorio, on_delete=models.CASCADE)
    id_malla = models.ForeignKey(Mallas, on_delete=models.CASCADE)
    PRP = models.DecimalField(max_digits=10, decimal_places=2)
    PeRP = models.DecimalField(max_digits=10, decimal_places=2)
    PRA = models.DecimalField(max_digits=10, decimal_places=2)
    PeQP = models.DecimalField(max_digits=10, decimal_places=2)


class DiametrosCoeficiente(models.Model):
    d10 = models.DecimalField(max_digits=10, decimal_places=2)
    d30 = models.DecimalField(max_digits=10, decimal_places=2)
    d60 = models.DecimalField(max_digits=10, decimal_places=2)
    cu = models.DecimalField(max_digits=10, decimal_places=2)
    cc = models.DecimalField(max_digits=10, decimal_places=2)
    id_ensayo = models.ForeignKey(EnsayosLaboratorio, on_delete=models.CASCADE, null=True)

class FactoresLL(models.Model):
    id_factor = models.IntegerField(primary_key=True)
    N = models.IntegerField()
    K = models.DecimalField(max_digits=10, decimal_places=3)

class LimiteLiquido(models.Model):
    id_ensayo = models.ForeignKey(EnsayosLaboratorio, on_delete=models.CASCADE)
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
    id_ensayo = models.ForeignKey(EnsayosLaboratorio, on_delete=models.CASCADE)
    recipiente_no = models.IntegerField()
    pw_mas_recip = models.FloatField()
    ps_mas_recip = models.FloatField()
    agua = models.FloatField()
    ps_mas_recip2 = models.FloatField()
    recipiente = models.DecimalField(max_digits=10, decimal_places=2)
    peso_seco = models.FloatField()
    limite_plastico = models.FloatField()
