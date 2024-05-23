import matplotlib.pyplot as plt
from django.db import OperationalError, connection
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json
from . import models
# Create your views here.

def querys_utiles():
    '''mm= models.Mallas.objects.get(id_malla=11)
    #mm.medida = "No. 4"
    mm.medida_mm = 0.425
    mm.save()'''

    '''SomeModel.objects.filter(id=id).delete()'''

    '''nueva_malla = models.Mallas(
        medida ="Pasa No. 200"
    )
    nueva_malla.save()'''

    # PARA ALMACENAR LOS FACTORES EN MI TABLA FACTORESLL
    factores = [0.895,0.909, 0.915, 0.924, 0.932, 0.940, 0.947, 0.954,0.961, 0.967, 0.973, 0.979, 0.985, 0.990, 0.995, 1.000, 1.005,1.009,1.014,1.018,1.022, 1.026, 1.030, 1.034, 1.038,1.000, 1.005, 1.009, 1.014, 1.018]
    
    id = 1
    N = 10
    for valor in factores:
        
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO factoresll(N,K) VALUES("+str(N)+""+str(valor)+") ")
        N+=1
        id+=1
    return N

def index(request):

    return redirect('/granulometria/')

# https://medium.com/@rajputgajanan50/ajax-in-django-72b895708167
def obtener_factores(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ensayos_factoresll")
            # Recuperar los nombres de las columnas
            columns = [col[0] for col in cursor.description]
            # Obtener todos los resultados de la consulta como una lista de diccionarios
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    except OperationalError as e:
        # Manejar el error si la consulta falla
        return JsonResponse({'error': str(e)}, status=500)
    # Devolver los datos como JSON
    return JsonResponse(rows, safe=False)

class grafica_granulometria(APIView):
    def obtener_grafica(self,request):

        datos = [1, 2, 3, 4, 5]
        plt.plot(datos)
        plt.xlabel('Eje X')
        plt.ylabel('Eje Y')
        plt.title('Mi Gráfica')
        # Guarda la gráfica en un archivo o en memoria
        img_path = '/graficas/mi_grafica.png'
        plt.savefig(img_path)
        plt.close()  # Cierra la figura para liberar memoria
    
        return Response()


def granulometria(request):
    if request.method == 'POST':
        
        # INFORMACION DEL ENSAYO
        nombre_proyecto = request.POST('nombre_proyecto')
        cliente = request.POST('cliente')
        operador = request.POST('operador')
        descripcion = request.POST('descripcion')
        no_sondeo = request.POST('no_sondeo')
        no_muestra = request.POST('no_muestra')
        profundidad = request.POST('profundidad')
        fecha_ensayo = request.POST('fecha_ensayo')

        # GRANULOMETRIA
        PRP = request.POST.getlist('PRP')
        PerRP = request.POST.getlist('PeRP')
        PerRA = request.POST.getlist('PeRA')
        PQP = request.POST.getlist('PQP')

        # GRANULOMETRIA POR LAVADO
        PRPL = request.POST.getlist('PRPL')
        PerRPL = request.POST.getlist('PeRPL')
        PerRAL = request.POST.getlist('PeRAL')
        PQPL = request.POST.getlist('PQPL')

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ensayos_ensayo(nombre_proyecto, cliente,operador,descripcion, no_sondeo, profundidad, fecha, tipo, codigo_area_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)")
            cursor.execute("SELECT * FROM ensayos_ensayo ORDER BY id DESC LIMIT 1;").fetchall()
            cursor.execute("INSERT INTO ensayos_granulometria(PRP, PeRP,PRA, PeQP, id_ensayo_id, id_malla_id) VALUES(%s, %s, %s, %s, %s, %s )")
            
        cursor.commit()
        print("return html: "+ str(PRP))
        print("return html prpl: "+ str(PRPL))

        return render(request, 'index.html')
    else:
        mallas = models.Mallas.objects.values_list('medida', 'medida_mm', 'id_malla')
        print(mallas)
        return render(request, 'granulometria.html', context={
            'mallas': mallas,
        })

def limites_atterberg(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        with connection.cursor() as cursor:
            limite_L = cursor.execute("SELECT * FROM ensayos_limiteliquido").fetchall()
            limite_P = cursor.execute("SELECT * FROM ensayos_limiteplastico").fetchall()


        return render(request, 'limites_atterberg.html', context={
            'limiteLiquido': limite_L,
            'limitePlastico': limite_P,
        })