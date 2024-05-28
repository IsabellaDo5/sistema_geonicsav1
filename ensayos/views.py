import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.db import OperationalError, connection
from django.shortcuts import render, redirect
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
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

    return render(request,'index.html')

# FUNCIONES ASINCRONAS  
def obtener_factores(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ensayos_factoresll")
            # Obtiene los nombres de las columnas, 
            columns = [col[0] for col in cursor.description]
            # Obtener todos los resultados de la consulta como una lista de diccionarios [{"key":value, "key2": value2}]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    except OperationalError as e:
        # Envia un error si la consulta falla
        return JsonResponse({'error': str(e)}, status=500)
    # Devuelve los datos como JSON
    return JsonResponse(rows, safe=False)


def obtener_grafica(request):
        if request.method == 'GET':
            plt.xlabel('Diámetro de particulas (mm)')
            plt.ylabel('% que pasa')
            plt.title('Curva granulométrica')

            mallas_lista = json.loads(request.GET.get('mallas_lista', '[]'))
            pesos_lista = json.loads(request.GET.get('pesos_lista', '[]'))

             # Filtrar cadenas vacías y convertir a float
            mallas_lista = [float(i) if i else 0 for i in mallas_lista ]
            pesos_lista = [float(i) if i else 0 for i in pesos_lista ]

            print("MEDIDAS MALLAS:", mallas_lista)
            print("PESOS LISTA:", pesos_lista)

            xpoints = np.array(mallas_lista)
            ypoints = np.array(pesos_lista)

            plt.plot(xpoints, ypoints)
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            plt.close()
            buf.seek(0)
            
            print(buf)
            return HttpResponse(buf, content_type='image/png')


# GRANULOMETRIA

def reportes_granulometria(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            ensayos = cursor.execute("SELECT * FROM ensayos_ensayo").fetchall()
        connection.commit()

        print("Ensayos:" + str(ensayos))
    return render(request, 'reportes_granulometria.html', context={
        'ensayos_granulometria': ensayos,
    })


def registrar_granulometria(request):
    if request.method == 'POST':
        
        # INFORMACION DEL ENSAYO
        nombre_proyecto = request.POST['nombre_proyecto']
        cliente = request.POST['cliente']
        operador = request.POST['operador']
        descripcion = request.POST['descripcion']
        no_sondeo = request.POST['no_sondeo']
        no_muestra = request.POST['no_muestra']
        profundidad = request.POST['profundidad']
        fecha_ensayo = request.POST['fecha_ensayo']

        # GRANULOMETRIA
        PRP = request.POST.getlist('PRP')
        PerRP = request.POST.getlist('PeRP')
        PerRA = request.POST.getlist('PeRA')
        PQP = request.POST.getlist('PQP')
        mallas = request.POST.getlist('ID_MALLA')

        # GRANULOMETRIA POR LAVADO
        PRPL = request.POST.getlist('PRPL')
        PerRPL = request.POST.getlist('PeRPL')
        PerRAL = request.POST.getlist('PeRAL')
        PQPL = request.POST.getlist('PQPL')

        peso_retenido = PRP+PRPL
        pce_retenido_parcial = PerRP+PerRPL
        pce_retenido_acumulado = PerRA+PerRAL
        pce_que_pasa = PQP+PQPL

        with connection.cursor() as cursor:

            sql_info_ensayo = "INSERT INTO ensayos_ensayo(nombre_proyecto, cliente,operador,descripcion, no_sondeo, profundidad, fecha, tipo, codigo_area_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            insertar_valores = (nombre_proyecto,cliente,operador,descripcion,no_sondeo,profundidad,fecha_ensayo,"",2)
            cursor.execute(sql_info_ensayo, insertar_valores)
            id_ensayo = cursor.execute("SELECT id FROM ensayos_ensayo ORDER BY id DESC LIMIT 1;").fetchall()

        connection.commit()

        print("ensayo: "+str(id_ensayo[0][0]))
        with connection.cursor() as cursor:
            for id_malla, peso, pr, perrp, perra, pp in zip(mallas, peso_retenido,peso_retenido, pce_retenido_parcial, pce_retenido_acumulado, pce_que_pasa):
                if peso != "":
                    print("PESO RETENIDO: "+str(pr)+" PORCENTAJE PESO RETENIDO: "+str(perrp)+" PCE RETENIDO ACUMULADO: "+str(perra)+" PORCENTAJE QUE PASA: "+str(pp))
                    sql_granulometria_t1= "INSERT INTO ensayos_granulometria(PRP, PeRP,PRA, PeQP, id_ensayo_id, id_malla_id) VALUES(%s, %s, %s, %s, %s, %s )"
                    insertar_granulometria =(pr,perrp,perra,pp, id_ensayo[0][0], id_malla)
                    cursor.execute(sql_granulometria_t1, insertar_granulometria)


        return redirect('/reportes-granulometria/')
    else:
        mallas = models.Mallas.objects.values_list('medida', 'medida_mm', 'id_malla')
        print(mallas)
        return render(request, 'registrar_granulometria.html', context={
            'mallas': mallas,
        })

def detalle_granulometria(request):
    if request.method == 'GET':
        return render(request, 'detalle_granulometria.html')  
        
def registrar_limites_atterberg(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        with connection.cursor() as cursor:
            limite_L = cursor.execute("SELECT * FROM ensayos_limiteliquido").fetchall()
            limite_P = cursor.execute("SELECT * FROM ensayos_limiteplastico").fetchall()


        return render(request, 'registrar_limites_atterberg.html', context={
            'limiteLiquido': limite_L,
            'limitePlastico': limite_P,
        })