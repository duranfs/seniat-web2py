import time
from datetime import datetime
import json  # Añade esta línea al inicio del archivo


def consulta_log_error():
    # Obtener conexión
    
    datos = db(
        (db.servidores.id == 488) &
        (db.servidores.id == db.basedatos.servidor)
    ).select().first()
    
    error=''    
    if not datos:
        return dict(error="No se pudo obtener información del servidor")

    connection = get_oracle_connection(
        datos.servidores.ip,
        "SENIAT.seniat.gov.ve",
        datos.basedatos.puerto,
        "11"
    )
    
    
    try:
        # Consulta para obtener los últimos errores
        sql = """
        SELECT * FROM (
            SELECT fecha_generacion_error, proceso_origen_error, 
                   tabla_afectada_error, mensaje_error 
            FROM log_error where tabla_afectada_error not like 'PREGUNTA_USUARIO_%' AND tabla_afectada_error not like 'TRANSACC_%' 
            ORDER BY fecha_generacion_error DESC
        ) 
        WHERE ROWNUM <= 10
        """
        
        cursor = connection.cursor()
        cursor.execute(sql)
        
        # Obtener nombres de columnas
        columns = [col[0] for col in cursor.description]
        
        # Obtener todos los registros
        rows = cursor.fetchall()
        
        return dict(columns=columns, rows=rows, error=None)
        
    except Exception as e:
        return dict(error=str(e))
        
    finally:
        if connection:
            connection.close()


def consulta_seniatfe():
    # Obtener conexión
    
    datos = db(
        (db.servidores.id == 501) & #seniatfe
        (db.servidores.id == db.basedatos.servidor)
    ).select().first()
    
    error=''    
    if not datos:
        return dict(error="No se pudo obtener información del servidor")

    connection = get_oracle_connection(
        datos.servidores.ip,
        "SENIATFE",
        datos.basedatos.puerto,
        "12"
    )
    
  
    
    try:
        # Consulta para obtener los últimos errores
        sql = """
            SELECT to_char(REGISTRO_FECHA, 'YYYY-mm-dd') as FECHA, COUNT(1) AS CANTIDAD
            FROM ITAXUSER.LIB_REPORTEZ lr
            WHERE REGISTRO_FECHA >= TRUNC(ADD_MONTHS(SYSDATE, -1), 'MONTH')
            -- AND REGISTRO_FECHA < TRUNC(SYSDATE, 'MONTH')
            GROUP BY to_char(REGISTRO_FECHA, 'YYYY-mm-dd')
            ORDER BY to_char(REGISTRO_FECHA, 'YYYY-mm-dd') ASC
        """
        
        cursor = connection.cursor()
        cursor.execute(sql)
        
        # Obtener nombres de columnas
        columns = [col[0] for col in cursor.description]
        
        # Obtener todos los registros
        rows = cursor.fetchall()
        
        return dict(columns=columns, rows=rows, error=None)
        
    except Exception as e:
        return dict(error=str(e))
        
    finally:
        if connection:
            connection.close()


def refresh_data():
    """Función para actualizar los datos via AJAX"""
    
    datos = db(
        (db.servidores.id == 488) &
        (db.servidores.id == db.basedatos.servidor)
    ).select().first()
    
    error=''    
    if not datos:
        return dict(error="No se pudo obtener información del servidor")

    connection = get_oracle_connection(
        datos.servidores.ip,
        "SENIAT.seniat.gov.ve",
        datos.basedatos.puerto,
        "11"
    )
    
    
    
    try:
        # Usar la misma consulta que en index()
        sql = """
        SELECT * FROM (
            SELECT fecha_generacion_error, proceso_origen_error, 
                   tabla_afectada_error, mensaje_error 
            FROM log_error 
            ORDER BY fecha_generacion_error DESC
        ) 
        WHERE ROWNUM <= 10
        """
        
        cursor = connection.cursor()
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        return response.render('oracle/refresh.html', dict(columns=columns, rows=rows))
        
    except Exception as e:
        return DIV("Error al actualizar: ", str(e), _class="alert alert-danger")
    finally:
        if connection:
            connection.close()



# Acción para iniciar el monitoreo
def monitorear_tps():
    if not auth.has_membership('admin'):  # Proteger esta acción
        redirect(URL('default', 'index'))
    
    response = monitor_tps()
    return response

# Acción para ver resultados

import time
from datetime import datetime

import json
from datetime import datetime, timedelta

def ver_tps():
    # Obtener la hora hace 1 minuto
    umbral = datetime.now() - timedelta(minutes=1)
    
    # Obtener registros del último minuto
    registros = db((db.oracle_tps.fecha_hora >= umbral)).select(
        orderby=~db.oracle_tps.fecha_hora
    )
    
    # Preparar datos para el gráfico
    horas = [r.hora for r in registros]
    tps_values = [r.tps for r in registros]
    
    return dict(
        registros=registros,
        horas_json=XML(json.dumps(horas)),
        tps_json=XML(json.dumps(tps_values)),
        ultima_actualizacion=datetime.now().strftime("%H:%M:%S"),
        grafico_title="TPS - Último Minuto"
    )

def actualizar_tps():
    # Esta función solo será llamada via AJAX
    monitor_tps()  # Tu función existente para capturar TPS
    return ver_tps()  # Devolver los datos actualizados



def monitorear_rutinas():
    # Obtener todas las rutinas habilitadas
    rutinas = db(db.rutina_status.status == "HABILITADO").select()
    
    for rutina in rutinas:
        # Obtener información del servidor y tipo de BD
        servidor = db.servidores(rutina.servidor_id)
        tipo_bd = db.tipobd(rutina.tipobd_id)
        
        if not servidor or not tipo_bd:
            continue  # Saltar si no hay información del servidor o tipo de BD
            
        try:
            # Obtener conexión
            connection = get_oracle_connection()
            cursor = connection.cursor()
            
            inicio = time.time()
            
            # Ejecutar el comando de la rutina
            cursor.execute(rutina.comando)
            resultado = cursor.fetchall()
            
            fin = time.time()
            duracion = fin - inicio
            
            # Registrar el resultado exitoso
            db.rutina_monitoreo.insert(
                rutina_status_id=rutina.id,
                fecha_ejecucion=datetime.now(),
                estado="EJECUTADO",
                resultado=str(resultado),
                duracion=duracion
            )
            
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            # Registrar el error
            db.rutina_monitoreo.insert(
                rutina_status_id=rutina.id,
                fecha_ejecucion=datetime.now(),
                estado="FALLIDO",
                resultado=f"Error {error.code}: {error.message}",
                duracion=0
            )
            
        finally:
            # Cerrar la conexión si existe
            if 'connection' in locals() and connection:
                cursor.close()
                connection.close()
    
    return dict(message="Monitoreo completado")

# Para ejecutar este script periódicamente, puedes:
# 1. Llamarlo desde un controlador web2py
# 2. Configurarlo como un cron job que llame a la URL del controlador
# 3. Usar el programador de tareas de web2py (si estás usando web2py scheduler)

import cx_Oracle
import time
from datetime import datetime

def ejecutar_monitoreo():
    # Verificar si hay rutinas habilitadas
    rutinas = db(db.rutina_status.status == "HABILITADO").select()
    
    if not rutinas:
        return dict(success=False, message="No hay rutinas habilitadas para monitorear")
    
    resultados = []
    
    for rutina in rutinas:
        try:
            # Obtener información del servidor
            servidor = db.servidores(rutina.servidor_id)
            if not servidor:
                raise Exception(f"Servidor no encontrado para ID {rutina.servidor_id}")
            
            # Configurar conexión Oracle
            connection = get_oracle_connection()
            
            # Ejecutar la consulta
            start_time = time.time()
            cursor = connection.cursor()
            cursor.execute(rutina.comando)
            resultado = cursor.fetchall()
            
            duracion = time.time() - start_time
            
            # Registrar éxito
            monitoreo_id = db.rutina_monitoreo.insert(
                rutina_status_id=rutina.id,
                fecha_ejecucion=datetime.now(),
                estado="EJECUTADO",
                resultado=str(resultado[:100]),  # Guardar solo parte del resultado
                duracion=duracion,
                detalles_adicionales=f"Consultado en {servidor.nombre}"
            )
            
            resultados.append(dict(
                rutina=rutina.rutina,
                estado="OK",
                tiempo=round(duracion, 2)
            ))
            
        except Exception as e:
            # Registrar error
            db.rutina_monitoreo.insert(
                rutina_status_id=rutina.id,
                fecha_ejecucion=datetime.now(),
                estado="FALLIDO",
                resultado=str(e),
                duracion=0,
                detalles_adicionales=f"Error al conectar a {servidor.nombre if servidor else 'servidor desconocido'}"
            )
            
            resultados.append(dict(
                rutina=rutina.rutina,
                estado="ERROR",
                mensaje=str(e)
            ))
    
    return dict(
        success=True,
        total=len(rutinas),
        ejecutadas=len([r for r in resultados if r['estado'] == "OK"]),
        resultados=resultados
    )


def ejecutar_sql():
    # Esta función solo maneja el formulario y muestra resultados
    form = SQLFORM.factory(
        Field('consulta_sql', 'text', label='Consulta SQL',
              requires=IS_NOT_EMPTY(error_message='Debe ingresar una consulta SQL')),
        Field('max_registros', 'integer', default=1000000,
              label='Límite de registros', requires=IS_INT_IN_RANGE(1, 10000001)),
        submit='Ejecutar'
    )
    
    columns = []
    rows = []
    error = None
    total_registros = 0
    consulta_original = ""
    
    if form.process().accepted:
        try:
            
            datos = db(
                (db.servidores.id == 488) &
                (db.servidores.id == db.basedatos.servidor)
            ).select().first()
            
            error=''    
            if not datos:
                return dict(error="No se pudo obtener información del servidor")

            connection = get_oracle_connection(
                datos.servidores.ip,
                "SENIAT.seniat.gov.ve",
                datos.basedatos.puerto,
                "11"
            )
    
            
            # Obtener la consulta SQL del formulario
            consulta_original = form.vars.consulta_sql.strip()
            
            # Limpiar la consulta y agregar límite si no tiene
            consulta = consulta_original.upper()
            if "WHERE ROWNUM" not in consulta and "ROWNUM <=" not in consulta:
                if "WHERE" in consulta:
                    consulta_original += f" AND ROWNUM <= {form.vars.max_registros}"
                else:
                    # Buscamos las diferentes cláusulas para determinar dónde insertar el ROWNUM
                    group_by_pos = consulta.find("GROUP BY")
                    order_by_pos = consulta.find("ORDER BY")
                    
                    if group_by_pos != -1:
                        # Si hay GROUP BY, insertamos antes de él
                        consulta_original = (consulta_original[:group_by_pos] + 
                                           f" WHERE ROWNUM <= {form.vars.max_registros} " + 
                                           consulta_original[group_by_pos:])
                    elif order_by_pos != -1:
                        # Si hay ORDER BY pero no GROUP BY, insertamos antes de ORDER BY
                        consulta_original = consulta_original.replace("ORDER BY", 
                                           f"WHERE ROWNUM <= {form.vars.max_registros} ORDER BY")
                    else:
                        # Si no hay GROUP BY ni ORDER BY, añadimos al final
                        consulta_original += f" WHERE ROWNUM <= {form.vars.max_registros}"

            
            cursor = connection.cursor()
            cursor.execute(consulta_original)
            
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            total_registros = len(rows)
            
            # Guardar los resultados en sesión para el export a Excel
            session.columns = columns
            session.rows = rows
            session.consulta_original = consulta_original
            
        except Exception as e:
            error = str(e)
        finally:
            if connection:
                connection.close()
    
    return dict(form=form, columns=columns, rows=rows, error=error, 
                total_registros=total_registros, consulta_original=consulta_original)

def exportar_excel():
    # Esta función separada solo maneja la exportación a Excel
    if not (session.columns and session.rows):
        redirect(URL('ejecutar_sql'))
    
    import io
    from openpyxl import Workbook
    
    # Configurar respuesta
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = 'attachment; filename=consulta_resultados.xlsx'
    
    # Crear libro de Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Resultados"
    
    # Escribir encabezados
    ws.append(session.columns)
    
    # Escribir datos
    for row in session.rows:
        ws.append(list(row))
    
    # Guardar en un stream de bytes
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    return output.read()

def ejecutar_sql2():
    form = SQLFORM.factory(
        Field('consulta_sql', 'text', label='Consulta SQL',
              requires=IS_NOT_EMPTY(error_message='Debe ingresar una consulta SQL')),
        Field('max_registros', 'integer', default=100000,
              label='Límite de registros', requires=IS_INT_IN_RANGE(1, 1000001)),
        submit='Ejecutar'
    )
    
    columns = []
    rows = []
    error = None
    total_registros = 0
    consulta_original = ""
    
    if form.process().accepted:
        try:
            #connection = get_oracle_connection("172.0.0.1", "SEN.ve", "1523", "11")
            
            datos = db(
                (db.servidores.id == 488) &
                (db.servidores.id == db.basedatos.servidor)
            ).select().first()
            
            error=''    
            if not datos:
                return dict(error="No se pudo obtener información del servidor")

            connection = get_oracle_connection(
                datos.servidores.ip,
                "SENIAT.seniat.gov.ve",
                datos.basedatos.puerto,
                "11"
            )
    
            
            consulta_original = form.vars.consulta_sql.strip()
            
            # Limpiar la consulta y agregar límite si no tiene
            consulta = consulta_original.upper()
            if "WHERE ROWNUM" not in consulta and "ROWNUM <=" not in consulta:
                if "WHERE" in consulta:
                    consulta_original += f" AND ROWNUM <= {form.vars.max_registros}"
                else:
                    if "ORDER BY" in consulta:
                        consulta_original = consulta_original.replace("ORDER BY", 
                                    f"WHERE ROWNUM <= {form.vars.max_registros} ORDER BY")
                    else:
                        consulta_original += f" WHERE ROWNUM <= {form.vars.max_registros}"
            
            cursor = connection.cursor()
            cursor.execute(consulta_original)
            
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            total_registros = len(rows)
            
        except Exception as e:
            error = str(e)
        finally:
            if connection:
                connection.close()
    
    # Exportar a Excel si se solicita
    if request.vars.exportar == 'excel' and rows:
        import io
        from openpyxl import Workbook
        
        # Configurar respuesta
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers['Content-Disposition'] = 'attachment; filename=consulta_resultados.xlsx'
        
        # Crear libro de Excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Resultados"
        
        # Escribir encabezados
        ws.append(columns)
        
        # Escribir datos
        for row in rows:
            ws.append(list(row))
        
        # Guardar en un stream de bytes
        output = io.BytesIO()
        wb.save(output)
        output.seek(0)
        
        return output.read()
    
    return dict(form=form, columns=columns, rows=rows, error=error, 
                total_registros=total_registros, consulta_original=consulta_original)
    
    
    
    #------- declaraciones ------------

# En el controlador (por ejemplo, default.py)

from datetime import datetime, timedelta  # Agrega esta línea

def declaraciones():
    # Importaciones necesarias
    from datetime import datetime, timedelta
    import json
    
    # Obtener parámetros del request
    fecha_inicio = request.vars.fecha_inicio or (datetime.now() - timedelta(days=4)).strftime('%d-%m-%Y')
    fecha_fin = request.vars.fecha_fin or datetime.now().strftime('%d-%m-%Y')
    dia_seleccionado = request.vars.dia
    
    # obtener datos del servidor y bd
    datos = db(
        (db.servidores.id == 486) & #servidor cygnus prod
        (db.servidores.id == db.basedatos.servidor)
    ).select(
        db.servidores.ip,
        db.basedatos.nombre,
        db.basedatos.puerto,
        left=db.basedatos.on(db.basedatos.servidor == db.servidores.id)
    ).first()
    
    # Validación de fechas
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%d-%m-%Y')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%d-%m-%Y')
        if fecha_fin_dt < fecha_inicio_dt:
            return dict(error="La fecha final no puede ser anterior a la inicial")
    except ValueError:
        return dict(error="Formato de fecha inválido. Use DD-MM-YYYY")
    
    # Conexión a Oracle
    connection = get_oracle_connection(
        datos.servidores.ip,
        "SENIAT.seniat.gov.ve",
        datos.basedatos.puerto,
        "11"
    )
    
    try:
        # Consulta SQL para Oracle
        sql = """
        SELECT TO_CHAR(FECHA_INGRESO_DECLARACION, 'DD/MON/YYYY') AS "DAY",
               count(*) AS TOTAL,
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '00', 1, 0), '99')) "00",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '01', 1, 0), '99')) "01",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '02', 1, 0), '99')) "02",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '03', 1, 0), '99')) "03",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '04', 1, 0), '99')) "04",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '05', 1, 0), '99')) "05",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '06', 1, 0), '99')) "06",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '07', 1, 0), '99')) "07",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '08', 1, 0), '99')) "08",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '09', 1, 0), '99')) "09",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '10', 1, 0), '99')) "10",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '11', 1, 0), '99')) "11",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '12', 1, 0), '99')) "12",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '13', 1, 0), '99')) "13",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '14', 1, 0), '99')) "14",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '15', 1, 0), '99')) "15",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '16', 1, 0), '99')) "16",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '17', 1, 0), '99')) "17",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '18', 1, 0), '99')) "18",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '19', 1, 0), '99')) "19",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '20', 1, 0), '99')) "20",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '21', 1, 0), '99')) "21",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '22', 1, 0), '99')) "22",
               SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '23', 1, 0), '99')) "23"
        FROM declaracion
        WHERE trunc(fecha_ingreso_declaracion) BETWEEN TO_DATE(:fecha_inicio,'dd-mm-rrrr') 
                                                  AND TO_DATE(:fecha_fin,'dd-mm-rrrr') 
        GROUP BY TO_CHAR(FECHA_INGRESO_DECLARACION, 'DD/MON/YYYY')
        ORDER BY TO_DATE("DAY", 'DD/MON/YYYY')
        """
        
        cursor = connection.cursor()
        cursor.execute(sql, {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})
        
        # Procesar resultados
        columns = [col[0].upper() for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        horas = [f"{h:02d}" for h in range(24)]  # ['00', '01', ..., '23']
        total_general = sum(row['TOTAL'] for row in rows) if rows else 0
        dias = (fecha_fin_dt - fecha_inicio_dt).days + 1
        promedio_diario = round(total_general / dias, 2) if dias > 0 else 0
        acumulado_por_hora = {hora: sum(row[hora] for row in rows) for hora in horas} if rows else {hora: 0 for hora in horas} 
        # Preparar datos para el gráfico si hay día seleccionado
        datos_grafico = None
        if dia_seleccionado:
            for row in rows:
                if row['DAY'] == dia_seleccionado:
                    valores = [row[hora] for hora in horas]
                    max_val = max(valores) if valores else 0
                    
                    # Preparar colores basados en los valores
                    colores = []
                    for valor in valores:
                        if valor == max_val and max_val > 0:  # Solo si hay valores
                            colores.append('rgba(220, 53, 69, 0.7)')  # Rojo para el máximo
                        else:
                            colores.append('rgba(13, 110, 253, 0.7)')  # Azul normal
                    
                    datos_grafico = {
                        'dia': dia_seleccionado,
                        'total': row['TOTAL'],
                        'horas': horas,
                        'valores': valores,
                        'colores': colores
                    }
                    break
        
        # Calcular distribución acumulada
        distribucion_acumulada = {hora: sum(row[hora] for row in rows) for hora in horas}
        total_general = sum(distribucion_acumulada.values())
        
        # Calcular porcentajes
        porcentajes = {hora: round((count/total_general)*100, 2) if total_general > 0 else 0 
                      for hora, count in distribucion_acumulada.items()}
        
        return dict(
            rows=rows,
            horas=horas,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            dia_seleccionado=dia_seleccionado,
            datos_grafico=datos_grafico,
            totales_por_hora=distribucion_acumulada,  # Datos acumulados por hora
            total_general=total_general,              # Total general acumulado
            porcentajes=porcentajes,                  # Porcentajes por hora
            promedio_diario=promedio_diario,
            acumulado_por_hora=acumulado_por_hora,
            error=None
        )
        
    except Exception as e:
        return dict(error=f"Error en la consulta: {str(e)}")
    finally:
        if connection:
            connection.close()


def declaraciones_por_anio():
    from datetime import datetime
    import locale

    # Configurar locale para español
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except:
        locale.setlocale(locale.LC_TIME, 'spanish')

    # Obtener y validar año
    anio = request.vars.anio or str(datetime.now().year)
    try:
        anio_int = int(anio)
        if anio_int < 2000 or anio_int > datetime.now().year:
            return dict(anio=anio, error="Año inválido. Debe estar entre 2000 y el año actual")
    except ValueError:
        return dict(anio=anio, error="Año inválido. Debe ser un número")

    # Conexión a Oracle
    try:
        datos = db(
            (db.servidores.id == 486) &
            (db.servidores.id == db.basedatos.servidor)
        ).select().first()
        
        if not datos:
            return dict(anio=anio, error="No se pudo obtener información del servidor")

        connection = get_oracle_connection(
            datos.servidores.ip,
            "SENIAT.seniat.gov.ve",
            datos.basedatos.puerto,
            "11"
        )

        # Consulta SQL con formato de mes en español
        sql = """
        SELECT 
            TRIM(TO_CHAR(TRUNC(FECHA_INGRESO_DECLARACION, 'MM'), 'MONTH', 'NLS_DATE_LANGUAGE=SPANISH')) AS MES_NOMBRE,
            COUNT(*) AS TOTAL_MENSUAL,
            ROUND(COUNT(*) / 
                EXTRACT(DAY FROM LAST_DAY(TO_DATE('01-'||TO_CHAR(TRUNC(FECHA_INGRESO_DECLARACION, 'MM'), 'MM-YYYY'), 'DD-MM-YYYY')))
            , 2) AS PROMEDIO_DIARIO
        FROM 
            declaracion
        WHERE 
            EXTRACT(YEAR FROM FECHA_INGRESO_DECLARACION) = :anio
        GROUP BY 
            TRUNC(FECHA_INGRESO_DECLARACION, 'MM')
        ORDER BY 
            TRUNC(FECHA_INGRESO_DECLARACION, 'MM')
        """

        cursor = connection.cursor()
        cursor.execute(sql, {'anio': anio_int})
        
        # Procesar resultados
        columns = [col[0].upper() for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Nombres de meses en español para completar
        meses_espanol = [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
            'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        
        # Completar meses faltantes
        meses_completos = []
        for i, nombre_mes in enumerate(meses_espanol, 1):
            mes_encontrado = next((m for m in rows if m['MES_NOMBRE'].strip().upper() == nombre_mes.upper()), None)
            
            if mes_encontrado:
                # Asegurar formato consistente (primera letra mayúscula)
                mes_encontrado['MES_NOMBRE'] = mes_encontrado['MES_NOMBRE'].strip().capitalize()
                meses_completos.append(mes_encontrado)
            else:
                meses_completos.append({
                    'MES_NOMBRE': nombre_mes,
                    'TOTAL_MENSUAL': 0,
                    'PROMEDIO_DIARIO': 0.00
                })

        # Calcular totales
        total_anual = sum(mes['TOTAL_MENSUAL'] for mes in meses_completos)
        promedio_anual = round(total_anual / 12, 2) if total_anual > 0 else 0.00

        # Generar colores para el gráfico
        colores, bordes = generar_colores_meses(meses_completos)

        return dict(
            anio=anio,
            meses=meses_completos,
            total_anual=total_anual,
            promedio_anual=promedio_anual,
            colores_barras=colores,
            bordes_barras=bordes,
            error=None
        )

    except Exception as e:
        return dict(anio=anio, error=f"Error en la consulta: {str(e)}")
    finally:
        if connection:
            connection.close()
            

def generar_colores_meses(meses):
    # Colores base para los meses (puedes personalizarlos)
    colores_base = {
        'Enero': 'rgba(54, 162, 235, 0.7)',     # Azul
        'Febrero': 'rgba(255, 99, 132, 0.7)',    # Rojo
        'Marzo': 'rgba(75, 192, 192, 0.7)',      # Verde azulado
        'Abril': 'rgba(255, 159, 64, 0.7)',      # Naranja
        'Mayo': 'rgba(153, 102, 255, 0.7)',      # Morado
        'Junio': 'rgba(255, 205, 86, 0.7)',      # Amarillo
        'Julio': 'rgba(201, 203, 207, 0.7)',     # Gris
        'Agosto': 'rgba(54, 162, 235, 0.7)',     # Azul
        'Septiembre': 'rgba(255, 99, 132, 0.7)', # Rojo
        'Octubre': 'rgba(75, 192, 192, 0.7)',    # Verde azulado
        'Noviembre': 'rgba(255, 159, 64, 0.7)',  # Naranja
        'Diciembre': 'rgba(153, 102, 255, 0.7)'  # Morado
    }
    
    # Colores para bordes
    bordes_base = {
        'Enero': 'rgba(54, 162, 235, 1)',
        'Febrero': 'rgba(255, 99, 132, 1)',
        'Marzo': 'rgba(75, 192, 192, 1)',
        'Abril': 'rgba(255, 159, 64, 1)',
        'Mayo': 'rgba(153, 102, 255, 1)',
        'Junio': 'rgba(255, 205, 86, 1)',
        'Julio': 'rgba(201, 203, 207, 1)',
        'Agosto': 'rgba(54, 162, 235, 1)',
        'Septiembre': 'rgba(255, 99, 132, 1)',
        'Octubre': 'rgba(75, 192, 192, 1)',
        'Noviembre': 'rgba(255, 159, 64, 1)',
        'Diciembre': 'rgba(153, 102, 255, 1)'
    }
    
    # Encontrar el valor máximo para destacarlo
    max_valor = max(mes['TOTAL_MENSUAL'] for mes in meses) if meses else 0
    
    colores = []
    bordes = []
    for mes in meses:
        nombre_mes = mes['MES_NOMBRE']
        if mes['TOTAL_MENSUAL'] == max_valor and max_valor > 0:
            # Destacar el mes con mayor valor
            colores.append('rgba(220, 53, 69, 0.7)')  # Rojo más intenso
            bordes.append('rgba(220, 53, 69, 1)')
        elif mes['TOTAL_MENSUAL'] == 0:
            # Meses sin datos
            colores.append('rgba(200, 200, 200, 0.5)')
            bordes.append('rgba(200, 200, 200, 1)')
        else:
            # Usar color asignado al mes
            colores.append(colores_base.get(nombre_mes, 'rgba(75, 192, 192, 0.7)'))
            bordes.append(bordes_base.get(nombre_mes, 'rgba(75, 192, 192, 1)'))
    
    return colores, bordes