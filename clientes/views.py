from django.db import connection
from django.shortcuts import redirect, render

# Create your views here.

def registrar_cliente(request):
    if request.method == 'POST':
        nombres= request.POST['nombre']
        telefono= request.POST['telefono']

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO clientes_clientes(nombre, telefono) VALUES(%s,%s)", (nombres,telefono,))
        connection.commit()
        return redirect('/clientes/ver/')
    else:
        return render(request, 'registrar_cliente.html')

def ver_clientes(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            clientes= cursor.execute("SELECT * FROM clientes_clientes").fetchall()
        connection.commit()

        return render(request, 'ver_clientes.html', context={
            'clientes': clientes,
        })

def detalle_cliente(request, id_cliente):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            cliente = cursor.execute("SELECT * FROM clientes_clientes C LEFT JOIN proyectos_proyectos P ON C.id_cliente = P.id_cliente_id WHERE C.id_cliente = %s", (id_cliente,)).fetchall()
        connection.commit()

        print(cliente)
        return render(request, 'detalle_cliente.html', context={
            'cliente': cliente,
        })         