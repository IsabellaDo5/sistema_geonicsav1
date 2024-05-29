"""
URL configuration for SisGeonicv1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import ensayos.views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ensayos.views.index),
    # ELIMINAR REPORTES
    path('granulometria/eliminar/<int:id_ensayo>/', ensayos.views.eliminar_granulometria, name="eliminar-granulometria"),
    # LISTAR REPORTES
    path('granulometria/reportes/', ensayos.views.reportes_granulometria, name="reportes-granulometria"),
    path('limites-de-atterberg/reportes/', ensayos.views.reportes_limites_atterberg, name="reportes-limite-atterberg"),
    # REGISTROS
    path('granulometria/nuevo/', ensayos.views.registrar_granulometria, name="registrar-granulometria"),
    path('limites-de-atterberg/nuevo/', ensayos.views.registrar_limites_atterberg, name="registrar-limites-de-attemberg"),
    #DETALLE
    path('granulometria/reporte/<int:id_ensayo>/',ensayos.views.detalle_granulometria, name="detalle-granulometria"),
    # ASINCRONO
    path('ajax/obtener_factores/', ensayos.views.obtener_factores, name='obtener_factores'),
    path('ajax/obtener_grafica/', ensayos.views.obtener_grafica, name="obtener-grafica"),
]
