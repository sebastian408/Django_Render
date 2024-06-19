from django.http import HttpResponse  #Permite responder peticiones
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . models import NPK_Experimentales, NPK_Teoricos, cargar_dato, repetir_dato, eliminar_dato,bajar_datos, obtener_datos
from datetime import datetime,timedelta
from django.urls import reverse
from django.http import HttpResponseRedirect
import json
# from .models import SensorData


#Variables Globales




def index(request):
    return render(request,'index.html',{
        'message':'Listado de productos',
        'title' :'Productos',
        'products':[
            {'title': 'Playera','price':5,'stock':True}, #producto
            {'title': 'Camisa','price':7,'stock':True}, #producto
            {'title': 'Mochila','price':20,'stock':False}, #producto
        ]
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username') #Diccionario
        password = request.POST.get('password')

        user = authenticate(username = username,password = password) #none

        if user: 
            login(request, user)

    return render(request,'users/login.html',{
    })

@csrf_exempt
def upload_sensor_data(request):
    if request.method == 'POST':
        Nro = NPK_Teoricos.objects.filter(Valid=True).latest('Nro').Nro
        Cant_teo = NPK_Teoricos.objects.filter(Valid=True).count()
        Cant_Exp = NPK_Experimentales.objects.filter(Valid=True).count()

        data = json.loads(request.body.decode('utf-8'))
        V_teo_1 = data.get('V_teo_1')
        V_teo_2 = data.get('V_teo_2')
        V_teo_3 = data.get('V_teo_3')
        Delete = data.get('Delete')
        Valid = data.get('Valid')

        print(" En sensor data Nro: {}  V1: {} V2: {} V3: {} Valid: {} Delete: {} ".format(Nro,V_teo_1,V_teo_2,V_teo_3,Valid,Delete))
        print("Datos_Teo: {} ,Datos_Exp: {}".format(Cant_teo, Cant_Exp))

        if Valid:
            print("Flag1")
            if Cant_teo -1 == Cant_Exp:
                print("Flag2")
                cargar_dato(NPK_Experimentales, V_teo_1,V_teo_2,V_teo_3,fecha = datetime.now()-timedelta(hours=5),Last_Nro=Nro)
        else:
            if Delete:
                eliminar_dato(NPK_Experimentales,Nro)
            else:
                repetir_dato(NPK_Experimentales, V_teo_1,V_teo_2,V_teo_3,Nro,fecha=datetime.now())

        return HttpResponse("Ok",status=200)

    if request.method == "GET":
        return HttpResponse("Peticion GET SENSOR DATA", status=200)
    else:
        return HttpResponse("Error en la solicitud", status=400)

@csrf_exempt
def upload_page_data(request):
    if request.method == 'POST':
        Cant_Base=request.POST.get("Cant_Base")
        Cant_teo = NPK_Teoricos.objects.filter(Valid=True).count()
        Cant_Exp = NPK_Experimentales.objects.filter(Valid=True).count()
        V_teo_1 = request.POST.get('V_teo_1')
        V_teo_2 = request.POST.get('V_teo_2')
        V_teo_3 = request.POST.get('V_teo_3')
        Nro= request.POST.get('Muestra')

        if request.POST.get('Valid')=='True':
            if Cant_teo == Cant_Exp:
                cargar_dato(NPK_Teoricos,V_teo_1,V_teo_2,V_teo_3,Last_Nro=Nro)
        else:
                Last_Nro=request.POST.get('Muestra')
                if request.POST.get('Delete')=='True':
                    eliminar_dato(NPK_Teoricos,int(Nro))
                else:
                    repetir_dato(NPK_Teoricos,V_teo_1,V_teo_2,V_teo_3,Last_Nro=int(Nro)-1)
        return HttpResponseRedirect('https://django-render-app-rc48.onrender.com/get_data/{}'.format(Cant_Base))

    if request.method == "GET":
        return HttpResponse("Peticion GET PAGE DATA", status=200)
    else:
        return HttpResponse("Error en la solicitud", status=400)

@csrf_exempt
def get_sensor_data(request,Cant_Base=1):  
        if Cant_Base is not None:
            Cant_Base = float(Cant_Base)  # Convertir el valor de Cant_Base a entero si es necesario
        else:
            Cant_Base = 1
        data_Teo = NPK_Teoricos.objects.filter(Valid=True).all()
        data_Exp = NPK_Experimentales.objects.filter(Valid=True).all()
        if data_Teo.exists():
            last_Teo, datos_Teo = obtener_datos(data_Teo)
        else:
            last_Teo = {'Nro':0,
                        'V_teo_1':0,
                        'V_teo_2':0,
                        'V_teo_3':0}
            datos_Teo = {'Nro':["",""],
                        'V_teo_1':["",""],
                        'V_teo_2':["",""],
                        'V_teo_3':["",""]}

        if data_Exp.exists():
            last_Exp, datos_Exp = obtener_datos(data_Exp)
        else:
            last_Exp = {'Nro':0,
                        'V_teo_1':0,
                        'V_teo_2':0,
                        'V_teo_3':0}
            datos_Exp = {'Nro':["",""],
                        'V_teo_1':["",""],
                        'V_teo_2':["",""],
                        'V_teo_3':["",""]}
        last_Teo['Nro'] += 1
        Cant=3
        try:
            Tabla_Teo = {key: value[-Cant:] for key, value in datos_Teo.items()}
        except:
            Tabla_Teo = datos_Teo
        try:
            Tabla_Exp = {key: value[-Cant:] for key, value in datos_Exp.items()}
        except:
            Tabla_Exp = datos_Teo
        print(datos_Teo)
        return render(request, 'get_data.html', {
            'Last_Obj': last_Teo,
            'Datos_Teo':Tabla_Teo,
            'Cant_Base':Cant_Base,
            'Datos_Exp':Tabla_Exp,
        })
