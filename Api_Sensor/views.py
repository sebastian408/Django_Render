from django.http import HttpResponse  #Permite responder peticiones
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . models import Tabla_NPK
from datetime import datetime
# from .models import SensorData


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

        instancia = Tabla_NPK(
            Nro='valor_para_Nro',
            V_med_1=request.POST.get('V_med_1'),
            V_teo_1=request.POST.get('V_teo_1'),
            V_med_2=request.POST.get('V_med_2'),
            V_teo_2=request.POST.get('V_teo_2'),
            V_med_3=request.POST.get('V_med_3'),
            V_teo_3=request.POST.get('V_teo_3'),
            Fecha=datetime.now(),
        )
        instancia.save()        

        print("Todo bello, Datos: ")
        for key, value in instancia.__dict__.items():
            print("{}: {}".format(key, value))
        return HttpResponse("OK", status=200)
    if request.method == "GET":
        return HttpResponse("Peticion GEt", status=200)
        
    else:
        # return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
        return HttpResponse("Error en la solicitud", status=400)