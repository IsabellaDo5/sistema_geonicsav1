import io
from django.db import OperationalError, connection
from django.shortcuts import render, redirect
import numpy as np
from django.http import HttpResponse, JsonResponse
import json
from . import models
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
    mallas_mm = [ 75, 63, 50, 37.5,25,19,12.5,9.5,4.75, 2.00, 0.425,0.075, 5, 0.080]
    mallas_pulg= ["3", "2 1/2", "2", "1 1/2", "1", "3/4", "1/2", "3/8", "No. 4", "No. 10", "No. 40", "No. 200", "Pasa No. 4", "Pasa No. 200"]
    
    for mm, pulg in zip(mallas_mm, mallas_pulg):
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ensayos_mallas(medida,medida_mm) VALUES("+pulg+""+mm+") ")
    
    # PARA ALMACENAR LOS FACTORES EN MI TABLA FACTORESLL
    factores = [0.895,0.909, 0.915, 0.924, 0.932, 0.940, 0.947, 0.954,0.961, 0.967, 0.973, 0.979, 0.985, 0.990, 0.995, 1.000, 1.005,1.009,1.014,1.018,1.022, 1.026, 1.030, 1.034, 1.038,1.000, 1.005, 1.009, 1.014, 1.018]
    
    id = 1
    N = 10
    for valor in factores:
        
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO factoresll(N,K) VALUES("+str(N)+""+str(valor)+") ")
        N+=1
        id+=1
    return N


# FUNCIONES ASINCRONAS  
def obtener_factores(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ensayos_factoresll")
            # Obtiene los nombres de las columnas, 
            columns = [col[0] for col in cursor.description]
            # Obtener todos los resultados de la consulta como una lista de diccionarios [{"key":value, "key2": value2}]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    except OperationalError as e:
        # Envia un error si la consulta falla
        return JsonResponse({'error': str(e)}, status=500)
    # Devuelve los datos como JSON
    return JsonResponse(rows, safe=False)

def obtener_cliente(request):
    try:
        proyecto = request.GET.get('proyecto')
        print(proyecto)
        with connection.cursor() as cursor:
            cursor.execute("SELECT C.nombre FROM clientes_clientes C INNER JOIN proyectos_proyectos P ON C.id_cliente = P.id_cliente_id WHERE P.nombre= %s", (proyecto,))
            # Obtiene los nombres de las columnas, 
            columns = [col[0] for col in cursor.description]
            # Obtener todos los resultados de la consulta como una lista de diccionarios [{"key":value, "key2": value2}]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            print(columns)
            print(rows)
    except OperationalError as e:
        # Envia un error si la consulta falla
        return JsonResponse({'error': str(e)}, status=500)
    # Devuelve los datos como JSON
    return JsonResponse(rows, safe=False)

''' FUNCIONES NORMALES '''


##############################################################################################
# GRANULOMETRIA

def reportes_granulometria(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            ensayos = cursor.execute("SELECT E.id_ensayo, P.nombre, C.nombre, E.profundidad, E.no_muestra, E.fecha FROM ensayos_ensayoslaboratorio E INNER JOIN clientes_clientes C ON E.id_cliente_id = C.id_cliente INNER JOIN proyectos_proyectos P ON P.id_proyecto = E.id_proyecto_id WHERE E.id_servicio_id=1").fetchall()
        connection.commit()

        print("Ensayos:" + str(ensayos))
    return render(request, 'ensayos/reportes.html', context={
        'info': ensayos,
        'link': "detalle-granulometria",
        'nombre_ensayo': "Granulometría",
    })


def registrar_granulometria(request):
    if request.method == 'POST':
        
        # GRANULOMETRIA
        PRP = request.POST.getlist('PRP')
        PerRP = request.POST.getlist('PeRP')
        PerRA = request.POST.getlist('PeRA')
        PQP = request.POST.getlist('PQP')
        mallas = request.POST.getlist('ID_MALLA')

        # GRANULOMETRIA POR LAVADO
        PRPL = request.POST.getlist('PRPL')
        PerRPL = request.POST.getlist('PeRPL')
        PerRAL = request.POST.getlist('PeRAL')
        PQPL = request.POST.getlist('PQPL')

        peso_retenido = PRP+PRPL
        pce_retenido_parcial = PerRP+PerRPL
        pce_retenido_acumulado = PerRA+PerRAL
        pce_que_pasa = PQP+PQPL

        id_ensayo= info_encabezado_ensayo(request,1,0, 1)

        print("ensayo: "+str(id_ensayo))
        with connection.cursor() as cursor:
            for id_malla, peso, pr, perrp, perra, pp in zip(mallas, peso_retenido,peso_retenido, pce_retenido_parcial, pce_retenido_acumulado, pce_que_pasa):
                print("PESO RETENIDO: "+str(pr)+" PORCENTAJE PESO RETENIDO: "+str(perrp)+" PCE RETENIDO ACUMULADO: "+str(perra)+" PORCENTAJE QUE PASA: "+str(pp))
                sql_granulometria_t1= "INSERT INTO ensayos_granulometria(PRP, PeRP,PRA, PeQP, id_ensayo_id, id_malla_id) VALUES(%s, %s, %s, %s, %s, %s )"
                insertar_granulometria =(pr,perrp,perra,pp, id_ensayo, id_malla)
                cursor.execute(sql_granulometria_t1, insertar_granulometria)


        return redirect('/granulometria/reportes/')
    else:
        mallas = models.Mallas.objects.values_list('medida', 'medida_mm', 'id_malla')

        with connection.cursor() as cursor:
            proyectos= cursor.execute("SELECT * FROM proyectos_proyectos P INNER JOIN proyectos_ordendetrabajo O ON P.id_proyecto = O.id_proyecto_id INNER JOIN proyectos_serviciosporproyecto S ON P.id_proyecto = S.id_proyecto_id WHERE estado= 1 AND S.id_servicio_id = 1").fetchall()
            
        connection.commit()
        print(mallas)
        print("PROYECTOS Y ORDENES DE TRABAJO ACTIVAS :"+str(proyectos))
        return render(request, 'ensayos/registrar_granulometria.html', context={
            'mallas': mallas,
            'proyectos':proyectos,
        })

def detalle_granulometria(request, id_ensayo):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            mallas = cursor.execute("SELECT * FROM ensayos_mallas").fetchall()

            suma_PRP = cursor.execute("SELECT SUM(PRP) FROM ensayos_granulometria WHERE (id_malla_id BETWEEN 1 AND 9 OR id_malla_id = 13) AND id_ensayo_id = %s", (id_ensayo,)).fetchall()
            suma_PRPL = cursor.execute("SELECT SUM(PRP) FROM ensayos_granulometria WHERE (id_malla_id BETWEEN 10 AND 12 OR id_malla_id = 14) AND id_ensayo_id = %s", (id_ensayo,)).fetchall()

            sql_encabezado ="SELECT E.id_ensayo, P.nombre, C.nombre, E.operador, E.descripcion_visual,E.no_sondeo, E.no_muestra, E.profundidad, E.fecha FROM ensayos_ensayoslaboratorio E INNER JOIN clientes_clientes C ON E.id_cliente_id = C.id_cliente INNER JOIN proyectos_proyectos P ON P.id_proyecto = E.id_proyecto_id WHERE E.id_ensayo=%s"
            sql_granulometria = "SELECT * FROM  ensayos_granulometria WHERE id_ensayo_id = %s"
            parametros=(id_ensayo,)

            tablas_ensayo = cursor.execute(sql_granulometria, parametros).fetchall()
            encabezado_ensayo = cursor.execute(sql_encabezado, parametros).fetchall()
            
            print("ID: "+str(id_ensayo))
            print("encabezado: "+str(encabezado_ensayo))
            print(tablas_ensayo)

        if len(encabezado_ensayo) == 0:
            return render(request, 'ensayos/error.html', context={
                'mensaje': "Ups, parece que ha ocurrido un error",
            })
        else:
            return render(request, 'ensayos/detalle_granulometria.html', context={
                'encabezado': encabezado_ensayo,
                'detalle_ensayo': tablas_ensayo,
                't1_suma':suma_PRP[0][0],
                't2_suma':suma_PRPL[0][0],
                'peso_seco_lavado': suma_PRPL[0][0]-tablas_ensayo[13][-6],
                'diferencia':tablas_ensayo[13][-6],
                'mallas': mallas,
                'id_ensayo': encabezado_ensayo[0][0],
            })  


def modificar_granulometria(request, id_ensayo):
    if request.method == 'POST':


        id= info_encabezado_ensayo(request,2,id_ensayo, 1)
                # GRANULOMETRIA
        PRP = request.POST.getlist('PRP')
        PerRP = request.POST.getlist('PeRP')
        PerRA = request.POST.getlist('PeRA')
        PQP = request.POST.getlist('PQP')
        mallas = request.POST.getlist('ID_MALLA')

        # GRANULOMETRIA POR LAVADO
        PRPL = request.POST.getlist('PRPL')
        PerRPL = request.POST.getlist('PeRPL')
        PerRAL = request.POST.getlist('PeRAL')
        PQPL = request.POST.getlist('PQPL')

        peso_retenido = PRP+PRPL
        pce_retenido_parcial = PerRP+PerRPL
        pce_retenido_acumulado = PerRA+PerRAL
        pce_que_pasa = PQP+PQPL

        print(id)
        with connection.cursor() as cursor:
            for id_malla, peso, pr, perrp, perra, pp in zip(mallas, peso_retenido,peso_retenido, pce_retenido_parcial, pce_retenido_acumulado, pce_que_pasa):
                sql_granulometria_t1= "UPDATE ensayos_granulometria SET PRP = %s, PeRP = %s, PRA = %s, PeQP = %s WHERE id_ensayo_id = %s AND id_malla_id = %s;"
                insertar_granulometria =(pr,perrp,perra,pp, id_ensayo, id_malla)
                cursor.execute(sql_granulometria_t1, insertar_granulometria)
        connection.commit()

        return redirect('/granulometria/reporte/'+str(id_ensayo)+'/')
    else:
        with connection.cursor() as cursor:
            mallas = cursor.execute("SELECT * FROM ensayos_mallas").fetchall()
            sql_encabezado ="SELECT E.id_ensayo, P.nombre, C.nombre, E.operador, E.descripcion_visual, E.no_sondeo, E.no_muestra, E.profundidad, E.fecha FROM ensayos_ensayoslaboratorio E INNER JOIN clientes_clientes C ON E.id_cliente_id = C.id_cliente INNER JOIN proyectos_proyectos P ON P.id_proyecto = E.id_proyecto_id WHERE E.id_ensayo=%s"
            sql_granulometria = "SELECT * FROM  ensayos_granulometria WHERE id_ensayo_id = %s"
            parametros=(id_ensayo,)
            tablas_ensayo = cursor.execute(sql_granulometria, parametros).fetchall()
            encabezado_ensayo = cursor.execute(sql_encabezado, parametros).fetchall()
            proyectos= cursor.execute("SELECT * FROM proyectos_proyectos P INNER JOIN proyectos_ordendetrabajo O ON P.id_proyecto = O.id_proyecto_id WHERE estado='1' ").fetchall()

            connection.commit()
        return render(request, 'ensayos/modificar_granulometria.html', context={
            'encabezado': encabezado_ensayo,
            'detalle_ensayo': tablas_ensayo,
            'proyectos':proyectos,
            'mallas': mallas,
            'id_ensayo': encabezado_ensayo[0][0],
        })
    

def eliminar_granulometria(request, id_ensayo):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM ensayos_granulometria WHERE id_ensayo_id = %s", (id_ensayo,))
        cursor.execute("DELETE FROM ensayos_ensayoslaboratorio WHERE id = %s", (id_ensayo,))
    connection.commit()
    return redirect('/granulometria/reportes/')


##############################################################################################
# LIMITES DE ATTERBERG
def reportes_limites_atterberg(request):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            ensayos = cursor.execute("SELECT * FROM ensayos_ensayoslaboratorio WHERE id_servicio_id=2").fetchall()
        connection.commit()
        return render(request, 'ensayos/reportes.html', context={
            'nombre_ensayo': "Límites de Atterberg",
            'link':  "detalle-limites-de-atterberg",
            'info': ensayos,
        })   


def registrar_limites_atterberg(request):
    if request.method == 'POST':

        # LIMITE LIQUIDO
        no_golpesLL= request.POST.getlist("no_golpes_LL")
        no_recipienteLL = request.POST.getlist("recipiente_no_LL")
        pw_mas_recipLL = request.POST.getlist("pw_mas_recip_LL")
        ps_mas_recipLL = request.POST.getlist("ps_mas_recip_LL")
        aguaLL = request.POST.getlist("agua_LL")
        recipienteLL= request.POST.getlist("recipiente_LL")
        peso_secoLL = request.POST.getlist("peso_seco_LL")
        pce_aguaLL = request.POST.getlist("Pe_agua_LL")
        factorLL = request.POST.getlist("factor_LL")
        limite_liquido = request.POST.getlist("Limite_liquido")

        # LIMITE PLASTICO
        no_recipienteLP = request.POST.getlist("recipiente_no_LP")
        pw_mas_recipLP = request.POST.getlist("pw_mas_recip_LP")
        ps_mas_recipLP = request.POST.getlist("ps_mas_recip_LP")
        aguaLP = request.POST.getlist("agua_LP")
        peso_secoLP = request.POST.getlist("peso_seco_LP")
        recipienteLP = request.POST.getlist("recipiente_LP")
        limite_plastico = request.POST.getlist("Limite_Plastico")

        id_ensayo = info_encabezado_ensayo(request,1 ,0, 2)

        for i in range(len(no_golpesLL)):

            if len(no_golpesLL[i])!= 0:
                print("FACTOR: "+factorLL[i])
                print(type(factorLL[i]))
                with connection.cursor() as cursor:
                    id_factor_id= cursor.execute("SELECT id_factor from ensayos_factoresll WHERE K = %s", (factorLL[i],)).fetchall()
                    
                    cursor.execute('''
                        INSERT INTO ensayos_limiteliquido (
                            no_golpes, recipiente_no, pw_mas_recip, ps_mas_recip, agua, ps_mas_recip2,
                            recipiente, peso_seco, Pe_agua, id_factor_id, limite_liquido, id_ensayo_id
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', [no_golpesLL[i], no_recipienteLL[i],  pw_mas_recipLL[i], ps_mas_recipLL[i], aguaLL[i], "1",
                         recipienteLL[i], peso_secoLL[i], pce_aguaLL[i], id_factor_id[0][0], limite_liquido[i], id_ensayo])
                connection.commit()
        
        for item in range(len(no_recipienteLP)):
            print(len(no_recipienteLP))
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO ensayos_limiteplastico (
                        recipiente_no, pw_mas_recip, ps_mas_recip, agua, ps_mas_recip2,
                        recipiente,peso_seco, limite_plastico, id_ensayo_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', [no_recipienteLP[item], pw_mas_recipLP[item], ps_mas_recipLP[item], aguaLP[item], "1",
                    recipienteLP[item], peso_secoLP[item], limite_plastico[item], id_ensayo])    
            connection.commit()
        print(id_ensayo)
        
        return redirect('/limites-de-atterberg/reportes/')
    else:
        with connection.cursor() as cursor:
            limite_L = cursor.execute("SELECT * FROM ensayos_limiteliquido").fetchall()
            limite_P = cursor.execute("SELECT * FROM ensayos_limiteplastico").fetchall()
            proyectos= cursor.execute("SELECT * FROM proyectos_proyectos P INNER JOIN proyectos_ordendetrabajo O ON P.id_proyecto = O.id_proyecto_id INNER JOIN proyectos_serviciosporproyecto S ON P.id_proyecto = S.id_proyecto_id WHERE estado= 1 AND S.id_servicio_id = 2").fetchall()

        return render(request, 'ensayos/registrar_limites_atterberg.html', context={
            'limiteLiquido': limite_L,
            'limitePlastico': limite_P,
            'proyectos': proyectos
        })
    
def detalle_limites_de_attergberg(request, id_ensayo):
    if request.method == 'GET':
        with connection.cursor() as cursor:
            encabezado_ensayo = cursor.execute("SELECT E.id_ensayo, P.nombre, C.nombre, E.operador, E.descripcion_visual,E.no_sondeo, E.no_muestra, E.profundidad, E.fecha FROM ensayos_ensayoslaboratorio E INNER JOIN clientes_clientes C ON E.id_cliente_id = C.id_cliente INNER JOIN proyectos_proyectos P ON P.id_proyecto = E.id_proyecto_id WHERE E.id_ensayo=%s", (id_ensayo,)).fetchall()
            limite_liquido = cursor.execute("SELECT * FROM ensayos_limiteliquido WHERE id_ensayo_id = %s", (id_ensayo,)).fetchall()
            limite_plastico = cursor.execute("SELECT * FROM ensayos_limiteplastico WHERE id_ensayo_id = %s", (id_ensayo,)).fetchall()
        connection.commit()
        print(encabezado_ensayo)
        print(limite_liquido)
    return render(request, 'ensayos/detalle_limites_atterberg.html', context={
        'encabezado': encabezado_ensayo,
        'limite_liquido': limite_liquido,
        'limite_plastico':limite_plastico,
        'id_ensayo': id_ensayo,
    })

def modificar_limites_atterberg(request, id_ensayo):
    if request.method == 'POST':

        
        # LIMITE LIQUIDO
        no_golpesLL= request.POST.getlist("no_golpes_LL")
        no_recipienteLL = request.POST.getlist("recipiente_no_LL")
        pw_mas_recipLL = request.POST.getlist("pw_mas_recip_LL")
        ps_mas_recipLL = request.POST.getlist("ps_mas_recip_LL")
        aguaLL = request.POST.getlist("agua_LL")
        recipienteLL= request.POST.getlist("recipiente_LL")
        peso_secoLL = request.POST.getlist("peso_seco_LL")
        pce_aguaLL = request.POST.getlist("Pe_agua_LL")
        factorLL = request.POST.getlist("factor_LL")
        limite_liquido = request.POST.getlist("Limite_liquido")

        # LIMITE PLASTICO
        no_recipienteLP = request.POST.getlist("recipiente_no_LP")
        pw_mas_recipLP = request.POST.getlist("pw_mas_recip_LP")
        ps_mas_recipLP = request.POST.getlist("ps_mas_recip_LP")
        aguaLP = request.POST.getlist("agua_LP")
        peso_secoLP = request.POST.getlist("peso_seco_LP")
        recipienteLP = request.POST.getlist("recipiente_LP")
        limite_plastico = request.POST.getlist("Limite_Plastico")

        id_ensayo = info_encabezado_ensayo(request,1 ,0, 2)

        for i in range(len(no_golpesLL)):

            if len(no_golpesLL[i])!= 0:
                print("FACTOR: "+factorLL[i])
                print(type(factorLL[i]))
                with connection.cursor() as cursor:
                    id_factor_id = cursor.execute("SELECT id_factor FROM ensayos_factoresll WHERE K = %s", (factorLL[i],)).fetchall()

                    cursor.execute('''
                        UPDATE ensayos_limiteliquido
                        SET 
                            no_golpes = %s, 
                            recipiente_no = %s, 
                            pw_mas_recip = %s, 
                            ps_mas_recip = %s, 
                            agua = %s, 
                            ps_mas_recip2 = %s,
                            recipiente = %s, 
                            peso_seco = %s, 
                            Pe_agua = %s, 
                            id_factor_id = %s, 
                            limite_liquido = %s
                        WHERE id_ensayo_id = %s
                    ''', [
                        no_golpesLL[i], no_recipienteLL[i], pw_mas_recipLL[i], ps_mas_recipLL[i], aguaLL[i], "1",
                        recipienteLL[i], peso_secoLL[i], pce_aguaLL[i], id_factor_id[0][0], limite_liquido[i], id_ensayo
                    ])
                connection.commit()

        
        for item in range(len(no_recipienteLP)):
            print(len(no_recipienteLP))
            with connection.cursor() as cursor:
                cursor.execute('''
                    UPDATE ensayos_limiteplastico
                    SET 
                        recipiente_no = %s, 
                        pw_mas_recip = %s, 
                        ps_mas_recip = %s, 
                        agua = %s, 
                        ps_mas_recip2 = %s,
                        recipiente = %s, 
                        peso_seco = %s, 
                        limite_plastico = %s
                    WHERE id_ensayo_id = %s
                ''', [
                    no_recipienteLP[item], pw_mas_recipLP[item], ps_mas_recipLP[item], aguaLP[item], "1",
                    recipienteLP[item], peso_secoLP[item], limite_plastico[item], id_ensayo
                ])
            connection.commit()

        return redirect('/')
    

    elif request.method == 'GET':

        with connection.cursor() as cursor:
            encabezado_ensayo = cursor.execute("SELECT E.id_ensayo, P.nombre, C.nombre, E.operador, E.descripcion_visual,E.no_sondeo, E.no_muestra, E.profundidad, E.fecha FROM ensayos_ensayoslaboratorio E INNER JOIN clientes_clientes C ON E.id_cliente_id = C.id_cliente INNER JOIN proyectos_proyectos P ON P.id_proyecto = E.id_proyecto_id WHERE E.id_ensayo=%s", (id_ensayo,)).fetchall()
            limite_liquido = cursor.execute("SELECT * FROM ensayos_limiteliquido WHERE id_ensayo_id = %s", (id_ensayo,)).fetchall()
            limite_plastico = cursor.execute("SELECT * FROM ensayos_limiteplastico WHERE id_ensayo_id = %s", (id_ensayo,)).fetchall()
            proyectos= cursor.execute("SELECT * FROM proyectos_proyectos P INNER JOIN proyectos_ordendetrabajo O ON P.id_proyecto = O.id_proyecto_id INNER JOIN proyectos_serviciosporproyecto S ON P.id_proyecto = S.id_proyecto_id WHERE estado= 1 AND S.id_servicio_id = 2").fetchall()
        connection.commit()

    return render(request, 'ensayos/modificar_limites_atterberg.html', context={
        'encabezado': encabezado_ensayo,
        'limite_liquido': limite_liquido,
        'limite_plastico':limite_plastico,
        'id_ensayo': id_ensayo,
        'proyectos':proyectos,
    })

def eliminar_limites_de_atterberg(request, id_ensayo):
    
    return redirect('/proyectos/ver/')
##############################################################################################
# NO SON VISTAS     
def info_encabezado_ensayo(request, accion, ensayo_id, tipo_ensayo):
    # INFORMACION DEL ENSAYO
        nombre_proyecto = request.POST['nombre_proyecto']
        operador = request.POST['operador']
        descripcion = request.POST['descripcion']
        no_sondeo = request.POST['no_sondeo']
        no_muestra = request.POST['no_muestra']
        profundidad = request.POST['profundidad']
        fecha_ensayo = request.POST['fecha_ensayo']

        with connection.cursor() as cursor:
            info_proyecto = cursor.execute("SELECT id_cliente_id, id_proyecto FROM proyectos_proyectos WHERE nombre = %s", (nombre_proyecto,)).fetchall()
        connection.commit()


        if accion == 1:
            with connection.cursor() as cursor:

                sql_info_ensayo = "INSERT INTO ensayos_ensayoslaboratorio(operador,descripcion_visual, no_sondeo,no_muestra, profundidad, fecha, id_cliente_id, id_proyecto_id, id_servicio_id) VALUES(%s, %s, %s,%s, %s, %s, %s, %s, %s)"
                insertar_valores = (operador,descripcion,no_sondeo,no_muestra,profundidad,fecha_ensayo,info_proyecto[0][0],info_proyecto[0][1],tipo_ensayo)
                cursor.execute(sql_info_ensayo, insertar_valores)
                id_ensayo = cursor.execute("SELECT id_ensayo FROM ensayos_ensayoslaboratorio ORDER BY id_ensayo DESC LIMIT 1;").fetchall()
            connection.commit()

            return id_ensayo[0][0]
        
        if accion == 2:
            with connection.cursor() as cursor:
                print("PROFNDIDAD: "+profundidad)
                
                sql_query= "UPDATE ensayos_ensayoslaboratorio SET id_cliente_id = %s,id_proyecto_id=%s, operador = %s, descripcion_visual = %s, no_sondeo = %s,no_muestra=%s, profundidad = %s, fecha = %s, id_servicio_id = %s, no_muestra = %s WHERE id = %s"
                insertar_valores = (info_proyecto[0][1],info_proyecto[0][0],operador,descripcion,no_sondeo, no_muestra, profundidad,fecha_ensayo,tipo_ensayo, no_muestra, ensayo_id)
                cursor.execute(sql_query, insertar_valores)
            connection.commit()
            return "Se actualizó el encabezado"