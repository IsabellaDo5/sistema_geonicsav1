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
            cursor.execute("SELECT * FROM clientes_clientes").fetchall()
        connection.commit()

        return render(request, 'ver_clientes.html')

def detalle_cliente(request):
    if request.method == 'GET':
        return render(request, 'detalle_cliente.html')         