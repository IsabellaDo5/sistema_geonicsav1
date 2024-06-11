from django.conf import settings
from django.db import connection


def ordenes_trabajo(request):
    with connection.cursor() as cursor:
            ordenes_trabajo =cursor.execute("SELECT O.no_orden, P.nombre FROM proyectos_ordentrabajo O INNER JOIN proyectos_proyectos P ON P.id_proyecto = O.proyecto_id").fetchall()
    connection.commit()
    return {
        'ordenes_trabajo': ordenes_trabajo,
    }