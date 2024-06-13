import json
from django.db import OperationalError, connection
from django.http import JsonResponse
from django.shortcuts import redirect, render

# Create your views here.

def index(request):
    '''with connection.cursor() as cursor:
        cursor.execute("UPDATE ensayos_ensayoslaboratorio SET tipo = 'GRANULOMETRIA'")
    connection.commit()'''
    '''with connection.cursor() as cursor:
        cursor.execute("delete from ensayos_limiteliquido")
        cursor.execute("delete from ensayos_limiteplastico")
        cursor.execute("delete from ensayos_ensayoslaboratorio where tipo = 'LIMITES DE ATTERBERG'")
        

    connection.commit()'''

    with connection.cursor() as cursor:
        ordenes_trabajo =cursor.execute("SELECT O.no_orden, P.nombre FROM proyectos_ordendetrabajo O INNER JOIN proyectos_proyectos P ON P.id_proyecto = O.id_proyecto_id WHERE O.estado == 1").fetchall()
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

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO proyectos_proyectos(nombre,id_cliente_id,ubicacion,descripcion) VALUES(%s,%s,%s,%s)", (proyecto,cliente,ubicacion,descripcion))
        connection.commit()
        return redirect('/proyectos/ver/')
    else:
        with connection.cursor() as cursor:
            clientes = cursor.execute("SELECT * FROM clientes_clientes").fetchall()
        connection.commit()
        return render(request, 'proyectos/registrar_proyecto.html', context={
            'clientes': clientes,
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
        
        print(proyectos)
        print(orden_trabajo)
        return render(request, 'proyectos/modificar_orden_trabajo.html', context={
            'id_orden': id_orden,
            'proyectos': proyectos,
            'info_orden': orden_trabajo,
        })
    if request.method == 'POST':
        print(request.POST.get("estado_orden"))
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