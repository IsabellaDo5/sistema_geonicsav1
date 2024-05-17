from django.shortcuts import render
from . import models
# Create your views here.

def index(request):
    mallas = models.Mallas.objects.values_list('medida')

    print(mallas)
    return render(request, 'granulometria.html', context={
        'medidas_mallas': mallas,
    })