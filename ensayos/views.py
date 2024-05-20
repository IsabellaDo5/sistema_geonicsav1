from django.shortcuts import render, redirect
from . import models
# Create your views here.


def index(request):

    '''mm= models.Mallas.objects.get(id_malla=11)
    #mm.medida = "No. 4"
    mm.medida_mm = 0.425
    mm.save()'''

    '''SomeModel.objects.filter(id=id).delete()'''

    '''nueva_malla = models.Mallas(
        medida ="Pasa No. 200"
    )
    nueva_malla.save()'''

    return redirect('/granulometria/')


def granulometria(request):
    if request.method == 'POST':

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

        print("return html: "+ str(PRP))
        print("return html prpl: "+ str(PRPL))

        return render(request, 'index.html')
    else:
        mallas = models.Mallas.objects.values_list('medida', 'medida_mm', 'id_malla')
        print(mallas)
        return render(request, 'granulometria.html', context={
            'mallas': mallas,
        })