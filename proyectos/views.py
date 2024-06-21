import json
from django.db import OperationalError, connection
from django.http import JsonResponse
from django.shortcuts import redirect, render
import xlsxwriter

# Create your views here.
def querys_utiles():
    '''mm= models.Mallas.objects.get(id_malla=13)
    #mm.medida = "No. 4"
    mm.medida_mm = 5
    mm.save()'''

    '''SomeModel.objects.filter(id=id).delete()'''

    '''nueva_malla = models.Mallas(
        medida ="Pasa No. 200"
    )
    nueva_malla.save()'''
    '''mallas_mm = [ 75, 63, 50, 37.5,25,19,12.5,9.5,4.75, 2.00, 0.425,0.075, 5, 0.080]
    mallas_pulg= ["3", "2 1/2", "2", "1 1/2", "1", "3/4", "1/2", "3/8", "No. 4", "No. 10", "No. 40", "No. 200", "Pasa No. 4", "Pasa No. 200"]
    
    for mm, pulg in zip(mallas_mm, mallas_pulg):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ensayos_mallas(medida,medida_mm) VALUES(%s, %s) ", (pulg, mm,))
    '''
    '''with connection.cursor() as cursor:
        cursor.execute("UPDATE ensayos_ensayoslaboratorio SET tipo = 'GRANULOMETRIA'")
    connection.commit()'''
    '''with connection.cursor() as cursor:
        cursor.execute("delete from ensayos_limiteliquido")
        cursor.execute("delete from ensayos_limiteplastico")
        cursor.execute("delete from ensayos_ensayoslaboratorio where tipo = 'LIMITES DE ATTERBERG'")
        

    connection.commit()'''
    # PARA ALMACENAR LOS FACTORES EN MI TABLA FACTORESLL
    factores = [0.895,0.909, 0.915, 0.924, 0.932, 0.940, 0.947, 0.954,0.961, 0.967, 0.973, 0.979, 0.985, 0.990, 0.995, 1.000, 1.005,1.009,1.014,1.018,1.022, 1.026, 1.030, 1.034, 1.038,1.000, 1.005, 1.009, 1.014, 1.018]
    
    id = 1
    N = 10
    for valor in factores:
        
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ensayos_factoresll(N,K) VALUES(%s, %s) ", (N, valor,))
        N+=1
        id+=1
    return N


def index(request):
    with connection.cursor() as cursor:
        ordenes_trabajo =cursor.execute("SELECT O.id_ordenTrabajo, O.no_orden, P.nombre FROM proyectos_ordendetrabajo O INNER JOIN proyectos_proyectos P ON P.id_proyecto = O.id_proyecto_id WHERE O.estado == 1").fetchall()
        
    connection.commit()
   
    return render(request,'index.html', context={
        'ordenes_trabajo': ordenes_trabajo,
        
    })


def registrar_proyecto(request):
    if request.method == 'POST':

        cliente = request.POST["cliente"]
        proyecto = request.POST["nombre_proyecto"]
        ubicacion = request.POST["ubicacion"]
        descripcion = request.POST["descripcion"]
        servicios = request.POST.getlist("servicio")

        print("SERVICIOS ELEGIDOS: "+str(servicios))
        
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO proyectos_proyectos(nombre,id_cliente_id,ubicacion,descripcion) VALUES(%s,%s,%s,%s)", (proyecto,cliente,ubicacion,descripcion))
            id_proyecto = cursor.execute("SELECT id_proyecto FROM proyectos_proyectos ORDER BY id_proyecto DESC LIMIT 1;")
            
            for x in servicios:
                cursor.execute("INSERT INTO proyectos_serviciosporproyecto(id_proyecto_id,id_servicio_id) VALUES(%s,%s,)", (id_proyecto, x))
        connection.commit()
        return redirect('/proyectos/ver/')
    else:
        with connection.cursor() as cursor:
            clientes = cursor.execute("SELECT * FROM clientes_clientes").fetchall()
            servicios = cursor.execute("SELECT * FROM ensayos_servicio").fetchall()
        connection.commit()
        return render(request, 'proyectos/registrar_proyecto.html', context={
            'clientes': clientes,
            'servicios': servicios,
        })

def modificar_proyecto(request, id_proyecto):
    if request.method == 'POST':

        cliente = request.POST["cliente"]
        proyecto = request.POST["nombre_proyecto"]
        ubicacion = request.POST["ubicacion"]
        descripcion = request.POST["descripcion"]
        servicios = request.POST.getlist("servicio")

        print("SERVICIOS ELEGIDOS: "+str(servicios))
        
        with connection.cursor() as cursor:
            cursor.execute("UPDATE proyectos_proyectos SET nombre = %s ,id_cliente_id= %s ,ubicacion = %s ,descripcion= %s WHERE id_proyecto = %s", (proyecto,cliente,ubicacion,descripcion, id_proyecto))
            cursor.execute("DELETE FROM proyectos_serviciosporproyecto WHERE id_proyecto_id = %s", (id_proyecto,))
            
            for servicio in servicios:
                print("SERVICIO"+str(servicio))
                print("ID PROYECTO: "+str(id_proyecto))
                cursor.execute("INSERT INTO proyectos_serviciosporproyecto(id_proyecto_id,id_servicio_id) VALUES(%s,%s)", (id_proyecto, servicio,))
        connection.commit()
        return redirect('/proyectos/ver/')
    else:
        servicios_lista= []
        with connection.cursor() as cursor:
            clientes = cursor.execute("SELECT * FROM clientes_clientes").fetchall()
            servicios = cursor.execute("SELECT * FROM ensayos_servicio ").fetchall()
            servicios_proyecto = cursor.execute("SELECT * FROM proyectos_serviciosporproyecto WHERE id_proyecto_id = %s", (id_proyecto,)).fetchall()
            info_proyecto = cursor.execute("SELECT * FROM proyectos_proyectos P INNER JOIN clientes_clientes C ON C.id_cliente = P.id_cliente_id WHERE P.id_proyecto = %s", (id_proyecto,)).fetchall()
        connection.commit()

        for x in range(len(servicios)):
            
            try:
                if servicios[x][0] == servicios_proyecto[x][2]:
                    servicios_lista.append((servicios[x][0],servicios[x][1], servicios[x][2], "checked",))
            except:
                servicios_lista.append((servicios[x][0],servicios[x][1], servicios[x][2], "",))    

        print(servicios_lista)        
        print("Info del proyecto: "+str(info_proyecto))
        print("Clientes: "+str(clientes))
        print("Servicios asociados al proyecto: "+str(servicios_proyecto))

        return render(request, 'proyectos/modificar_proyecto.html', context={
            'id_proyecto': id_proyecto,
            'clientes': clientes,
            'servicios_general': servicios_lista,
            'servicios': servicios_proyecto,
            'info_proyecto': info_proyecto,
        })

def listar_proyectos(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            info_proyectos=cursor.execute("SELECT * FROM proyectos_proyectos").fetchall()
        connection.commit()

        return render(request, 'proyectos/listar_proyectos.html', context={
            'info': info_proyectos,
        })
        

def registrar_orden_trabajo(request):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            proyectos=cursor.execute("INSERT INTO proyectos_ordendetrabajo(no_orden, id_proyecto_id, estado) VALUES(%s, %s, %s)", ( request.POST['no_orden'],request.POST['id_proyecto'], '1')).fetchall()
        connection.commit()

        return redirect('/ordenes-de-trabajo/ver/')    
    else:
        with connection.cursor() as cursor:
            proyectos=cursor.execute("SELECT * FROM proyectos_proyectos P LEFT JOIN proyectos_ordendetrabajo O ON P.id_proyecto = O.id_proyecto_id WHERE O.id_proyecto_id IS NULL ").fetchall()
        connection.commit()
        print(proyectos)
        return render(request, 'proyectos/registrar_orden_trabajo.html', context={
            'proyectos': proyectos,
        })
    


def modificar_orden_trabajo(request, id_orden):
    print("ID_ORDEN: "+str(id_orden))
    if request.method == 'GET':
        with connection.cursor() as cursor:
            proyectos= cursor.execute("SELECT * FROM proyectos_proyectos P LEFT JOIN proyectos_ordendetrabajo O ON P.id_proyecto = O.id_proyecto_id WHERE O.id_proyecto_id IS NULL").fetchall()
            orden_trabajo =cursor.execute("SELECT O.no_orden, P.nombre, O.id_proyecto_id, O.estado FROM proyectos_ordendetrabajo O INNER JOIN proyectos_proyectos P ON P.id_proyecto = O.id_proyecto_id WHERE id_ordenTrabajo = %s", (id_orden,)).fetchall()
        connection.commit()
        estado = orden_trabajo[0][3]

        print(proyectos)
        print(orden_trabajo)
        return render(request, 'proyectos/modificar_orden_trabajo.html', context={
            'id_orden': id_orden,
            'proyectos': proyectos,
            'info_orden': orden_trabajo,
            'estado': estado,
        })
    if request.method == 'POST':
        estado_orden = request.POST.get("estado_orden")
        id_proyecto = request.POST["id_proyecto"]
        no_orden = request.POST["no_orden"]

        if estado_orden == "on":
            estado = 1
        elif estado_orden == "off":
            estado = 0

        with connection.cursor() as cursor:
            cursor.execute("UPDATE proyectos_ordendetrabajo SET no_orden = %s, estado = %s, id_proyecto_id = %s WHERE id_ordenTRabajo = %s ", (no_orden, estado, id_proyecto, id_orden))
        connection.commit()
        return redirect('/')


def listar_ordenes_trabajo(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            ordenes_trabajo =cursor.execute("SELECT id_ordenTrabajo, O.no_orden, P.nombre, O.estado FROM proyectos_ordendetrabajo O INNER JOIN proyectos_proyectos P ON P.id_proyecto = O.id_proyecto_id").fetchall()
        connection.commit()

        print(ordenes_trabajo)
        return render(request, 'proyectos/listar_ordenes_trabajo.html', context={
            'ordenes_trabajo': ordenes_trabajo,
        })

def desactivar_orden_trabajo(request):
    if request.method == 'POST':
        try:    
            data = json.loads(request.body)
            id = data.get('id_orden')
            print("ID DE LA ORDEN QUE ACABO DE DESACTIVAR:"+str(id))

            with connection.cursor() as cursor:
                    cursor.execute("UPDATE proyectos_ordendetrabajo SET estado = %s WHERE id_ordenTrabajo= %s", (0, id,))
            connection.commit()
        except OperationalError as e:
            # Envia un error si la consulta falla
            return JsonResponse({'error': str(e)}, status=500)
        # Devuelve los datos como JSON
        return JsonResponse('completao',safe=False)

def activar_orden_trabajo(request):
    if request.method == 'POST':
        try:    
            data = json.loads(request.body)
            id = data.get('id_orden')
            
            print("ID DE LA ORDEN QUE ACABO DE ACTIVAR:"+str(id))

            with connection.cursor() as cursor:
                    cursor.execute("UPDATE proyectos_ordendetrabajo SET estado = %s WHERE id_ordenTrabajo= %s", (1, id,))
            connection.commit()
        except OperationalError as e:
            # Envia un error si la consulta falla
            return JsonResponse({'error': str(e)}, status=500)
        # Devuelve los datos como JSON
        return JsonResponse('completao',safe=False)
    
def obtener_ensayos_orden(request):
    if request.method == 'GET':
        try:
            id_orden = request.GET.get('id_orden')
            with connection.cursor() as cursor:
                ensayos_por_orden = cursor.execute('''SELECT P.id_proyecto, S.servicio FROM proyectos_proyectos P 
                                                   INNER JOIN proyectos_serviciosporproyecto SP ON P.id_proyecto = SP.id_proyecto_id 
                                                   INNER JOIN ensayos_servicio S ON SP.id_servicio_id = S.id_servicio 
                                                   INNER JOIN proyectos_ordendetrabajo O ON O.id_proyecto_id = P.id_proyecto 
                                                   WHERE id_ordenTrabajo = %s''', (id_orden,))
                columns = [col[0] for col in cursor.description]
                # Obtener todos los resultados de la consulta como una lista de diccionarios [{"key":value, "key2": value2}]
                rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        except OperationalError as e:
            # Envia un error si la consulta falla
            return JsonResponse({'error': str(e)}, status=500)
        # Devuelve los datos como JSON
        return JsonResponse(rows, safe=False)   
    
def reportes_GL_por_proyecto(request, id_proyecto):
    if request.method == 'GET':
        try: 
            id_proyecto = request.GET.get('id_proyecto')   
            with connection.cursor() as cursor:
                e_granulometria = cursor.execute("SELECT * FROM ensayos_ensayoslaboratorio E INNER JOIN ensayos_granulometria G ON E.id_ensayo = G.id_ensayo_id WHERE E.id_proyecto_id = %s", (id_proyecto,))
                columns = [col[0] for col in cursor.description]
                # Obtener todos los resultados de la consulta como una lista de diccionarios [{"key":value, "key2": value2}]
                rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

                print(rows)
        except OperationalError as e:
            # Envia un error si la consulta falla
            return JsonResponse({'error': str(e)}, status=500)
        # Devuelve los datos como JSON
        return JsonResponse(rows, safe=False)