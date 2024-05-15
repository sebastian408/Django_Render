# from django.db import connection
from django.db import models

class Tabla_NPK(models.Model):
    Nro = models.CharField(max_length=100)
    V_med_1 = models.IntegerField()
    V_teo_1 = models.FloatField(null=True, blank=True)
    V_med_2 = models.IntegerField()
    V_teo_2 = models.FloatField(null=True, blank=True)
    V_med_3 = models.IntegerField()
    V_teo_3 = models.FloatField(null=True, blank=True)
    Fecha = models.DateTimeField()
    # Esto puede servir como un cambio para que Django detecte una diferencia
    class Meta:
        app_label = 'Api_Sensor'

