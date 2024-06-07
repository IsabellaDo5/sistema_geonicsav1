from django.shortcuts import redirect, render

# Create your views here.
def registrar_proyecto(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return render(request, 'proyectos/registrar_proyecto.html')
    
def listar_proyectos(request):
    if request.method == 'POST':
        return redirect('/')
    else:
        return render(request, 'proyectos/listar_proyectos.html')

def registrar_orden_trabajo(request):
    if request.method == 'POST':
        return redirect('/')    
    else:
        return render(request, 'proyectos/registrar_orden_trabajo.html')
    
def listar_ordenes_trabajo(request):
    if request.method == 'GET':
        return render(request, 'proyectos/listar_ordenes_trabajo.html')