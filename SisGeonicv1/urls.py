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
import proyectos.views
import clientes.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', proyectos.views.index),
    # ELIMINAR ENSAYOS
    path('granulometria/eliminar/<int:id_ensayo>/', ensayos.views.eliminar_granulometria, name="eliminar-granulometria"),
    path('limites-de-atterberg/eliminar/<int:id_ensayo>/', ensayos.views.eliminar_limites_de_atterberg, name="eliminar-limites-de-atterberg"),
    
    # MODIFICAR ENSAYO
    path('granulometria/modificar/<int:id_ensayo>/', ensayos.views.modificar_granulometria, name="modificar-granulometria"),
    path('limites-de-atterberg/modificar/<int:id_ensayo>/', ensayos.views.modificar_limites_atterberg, name="modificar-limites-de-atterberg"),
    # LISTAR ENSAYOS
    path('granulometria/reportes/', ensayos.views.reportes_granulometria, name="reportes-granulometria"),
    path('limites-de-atterberg/reportes/', ensayos.views.reportes_limites_atterberg, name="reportes-limite-atterberg"),
    # REGISTROS
    path('granulometria/nuevo/', ensayos.views.registrar_granulometria, name="registrar-granulometria"),
    path('limites-de-atterberg/nuevo/', ensayos.views.registrar_limites_atterberg, name="registrar-limites-de-attemberg"),
    #DETALLE
    path('granulometria/reporte/<int:id_ensayo>/',ensayos.views.detalle_granulometria, name="detalle-granulometria"),
    path('limites-atterberg/reporte/<int:id_ensayo>/',ensayos.views.detalle_limites_de_attergberg, name="detalle-limites-de-atterberg"),

    #PROYECTOS

    path('proyectos/nuevo/', proyectos.views.registrar_proyecto, name="registrar-proyecto"),
    path('proyectos/modificar/<int:id_proyecto>', proyectos.views.modificar_proyecto, name="modificar-proyecto"),
    path('proyectos/ver/', proyectos.views.listar_proyectos, name="listar-proyectos"),
    path('ordenes-de-trabajo/nuevo/', proyectos.views.registrar_orden_trabajo, name="registrar-orden-de-trabajo"),
    path('ordenes-de-trabajo/ver/', proyectos.views.listar_ordenes_trabajo, name="listar-orden-de-trabajo"),
    path('ordenes-de-trabajo/modificar/<int:id_orden>/', proyectos.views.modificar_orden_trabajo, name="modificar-orden-de-trabajo"),
    #CLIENTES
    path('clientes/nuevo/', clientes.views.registrar_cliente, name="registrar-cliente"),
    path('clientes/ver/', clientes.views.ver_clientes, name="ver-clientes"),
    path('clientes/detalle/<int:id_cliente>', clientes.views.detalle_cliente, name="detalle-cliente"),
    # ASINCRONO
    path('ajax/obtener_factores/', ensayos.views.obtener_factores, name='obtener_factores'),
    path('ajax/obtener_cliente/', ensayos.views.obtener_cliente, name='obtener_cliente'),
    path('ajax/desactivar_orden/', proyectos.views.desactivar_orden_trabajo , name='desactivar_orden'),
    path('ajax/activar_orden/', proyectos.views.activar_orden_trabajo , name='activar_orden'),
    path('ajax/proyectos/ensayos/', proyectos.views.obtener_ensayos_orden , name='obtener_ensayos_orden'),
    path('ajax/proyectos/reportes/granulometria/', proyectos.views.reportes_GL_por_proyecto , name='obtener_reporte_GL'),
]
