# from django.db import connection
from django.db import models

class NPK_Experimentales(models.Model):
    Nro = models.IntegerField()
    V_teo_1 = models.FloatField()
    V_teo_2 = models.FloatField()
    V_teo_3 = models.FloatField()
    Fecha = models.DateTimeField()
    Valid=models.BooleanField(default=True)
    class Meta:
        app_label = 'Api_Sensor'

class NPK_Teoricos(models.Model):
    Nro = models.IntegerField()
    V_teo_1 = models.FloatField(null=True, blank=True)
    V_teo_2 = models.FloatField(null=True, blank=True)
    V_teo_3 = models.FloatField(null=True, blank=True)
    Valid=models.BooleanField(default=True)

    class Meta:
        app_label = 'Api_Sensor'

def cargar_dato(clase,V_teo_1,V_teo_2,V_teo_3,fecha=None,Last_Nro=None):
    # V_teo_1 = request.POST.get('V_teo_1')
    # V_teo_2 = request.POST.get('V_teo_2')
    # V_teo_3 = request.POST.get('V_teo_3')
    # if Last_Nro is None: Last_Nro=request.POST.get('Muestra')

    print("En Cargar Nro={}, v1={}, v2={}, v3={}".format(Last_Nro,V_teo_1,V_teo_2,V_teo_3))

    V1 = None if V_teo_1 == 'Null' else float(V_teo_1)
    V2 = None if V_teo_2 == 'Null' else float(V_teo_2)
    V3 = None if V_teo_3 == 'Null' else float(V_teo_3)
    print("En Cargar 2 Nro={}, v1={}, v2={}, v3={}".format(Last_Nro,V1,V2,V3))

    data={'Nro':int(Last_Nro),
          'V_teo_1':V1,
          'V_teo_2':V2,
          'V_teo_3':V3,}
    if fecha is not None: 
        print("Fecha= ",fecha)
        data['Fecha'] = fecha

    instancia = clase(**data)
    instancia.save()   

def repetir_dato(clase,request,Last_Nro,fecha=None):
    V_teo_1 = request.POST.get('V_teo_1')
    V_teo_2 = request.POST.get('V_teo_2')
    V_teo_3 = request.POST.get('V_teo_3')

    print("En repetir Nro={}, v1={}, v2={}, v3={}".format(Last_Nro,V_teo_1,V_teo_2,V_teo_3))

    V1 = None if V_teo_1 == 'Null' else float(V_teo_1)
    V2 = None if V_teo_2 == 'Null' else float(V_teo_2)
    V3 = None if V_teo_3 == 'Null' else float(V_teo_3)
    print("En repetir 2 Nro={}, v1={}, v2={}, v3={}".format(Last_Nro,V1,V2,V3))
    instancia=clase.objects.get(Nro=Last_Nro,Valid=True)
    instancia.V_teo_1= V1
    instancia.V_teo_2= V2
    instancia.V_teo_3= V3

    if fecha is not None: 
        instancia.fecha=fecha
    instancia.save()

def eliminar_dato(clase,Last_Nro):
    instancia=clase.objects.filter(Valid=True).get(Nro=int(Last_Nro))
    instancia.Valid= False
    instancia.save()

def bajar_datos(instancias):
    Last=instancias[len(instancias) - 1]
    llaves = list(Last.__dict__.keys())
    Dic_New = {key: [instancia[key] for instancia in instancias] for key in llaves}
    return Last, Dic_New


def obtener_datos(instancias):
    if instancias.exists():
        last = instancias.last()
        fields = last._meta.fields
        llaves = [field.name for field in fields]
        
        # Crear un nuevo diccionario con las variables que retorna
        nuevo_last = {}
        for key in llaves:
            valor = getattr(last, key)
            nuevo_last[key] = valor if valor is not None else 'Null'
        
        # Crear un nuevo diccionario con las variables de datos
        diccionario_nuevo = {}
        for key in llaves:
            valores = [getattr(instancia, key) for instancia in instancias]
            valores = [valor if valor is not None else 'Null' for valor in valores]
            diccionario_nuevo[key] = valores
    else:
        last = {}
        diccionario_nuevo = {}
        nuevo_last = {}
    return nuevo_last, diccionario_nuevo


