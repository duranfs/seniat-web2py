import time
from datetime import datetime
import json  # Añade esta línea al inicio del archivo


def consulta_log_error():
    # Obtener conexión
    connection = get_oracle_connection("172.16.32.67", "SENIAT.seniat.gov.ve", "1523","11")
    
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
    connection = get_oracle_connection("172.17.34.106", "SENIATFE", "1521","11")
    
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
    connection = get_oracle_connection("172.16.32.67", "SENIAT.seniat.gov.ve", "1523","11")
    
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
            connection = get_oracle_connection("172.16.32.67", "SENIAT.seniat.gov.ve", "1523","11")
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
            connection = get_oracle_connection("172.16.32.67", "SENIAT.seniat.gov.ve", "1523","11")
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
def declaraciones():
    # Obtener parámetros de fecha (con valores por defecto)
    fecha_inicio = request.vars.fecha_inicio or '25-03-2025'
    fecha_fin = request.vars.fecha_fin or '28-03-2025'
    
    # Validar fechas
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%d-%m-%Y')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%d-%m-%Y')
        
        if fecha_fin_dt < fecha_inicio_dt:
            return dict(error="La fecha final no puede ser anterior a la fecha inicial")
            
    except ValueError:
        return dict(error="Formato de fecha inválido. Use DD-MM-YYYY")
    
    # Obtener conexión a Oracle
    connection = get_oracle_connection("172.16.32.66", "SENIAT.seniat.gov.ve", "1521", "11")
    
    try:
        # Consulta con parámetros de fecha
        sql = """
        SELECT TO_CHAR(FECHA_INGRESO_DECLARACION, 'DD/MON/YYYY') AS "DAY"
            , count(*) AS Total
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '00', 1, 0), '99')) "00"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '01', 1, 0), '99')) "01"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '02', 1, 0), '99')) "02"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '03', 1, 0), '99')) "03"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '04', 1, 0), '99')) "04"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '05', 1, 0), '99')) "05"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '06', 1, 0), '99')) "06"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '07', 1, 0), '99')) "07"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '08', 1, 0), '99')) "08"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '09', 1, 0), '99')) "09"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '10', 1, 0), '99')) "10"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '11', 1, 0), '99')) "11"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '12', 1, 0), '99')) "12"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '13', 1, 0), '99')) "13"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '14', 1, 0), '99')) "14"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '15', 1, 0), '99')) "15"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '16', 1, 0), '99')) "16"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '17', 1, 0), '99')) "17"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '18', 1, 0), '99')) "18"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '19', 1, 0), '99')) "19"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '20', 1, 0), '99')) "20"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '21', 1, 0), '99')) "21"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '22', 1, 0), '99')) "22"
            , SUM(TO_NUMBER(DECODE(TO_CHAR(FECHA_INGRESO_DECLARACION, 'HH24'), '23', 1, 0), '99')) "23"
        FROM declaracion
        WHERE extract(year FROM trunc(FECHA_INGRESO_DECLARACION)) = 2025
            and trunc(fecha_ingreso_declaracion) BETWEEN TO_DATE(:fecha_inicio,'dd-mm-rrrr') AND TO_DATE(:fecha_fin,'dd-mm-rrrr') 
        GROUP BY TO_CHAR(FECHA_INGRESO_DECLARACION, 'DD/MON/YYYY')
        ORDER BY 1
        """
        
        cursor = connection.cursor()
        cursor.execute(sql, {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})
        
        # Obtener datos
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        
        # Preparar datos para el gráfico
        horas = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', 
                '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
        
        # Sumar totales por hora para todas las fechas
        totales_por_hora = [0] * 24
        for row in rows:
            for i in range(24):
                totales_por_hora[i] += row[i+2] or 0  # Las horas empiezan en la columna 2
        
        return dict(
            columns=columns,
            rows=rows,
            horas=horas,
            totales_por_hora=totales_por_hora,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            error=None
        )
        
    except Exception as e:
        return dict(error=str(e))
        
    finally:
        if connection:
            connection.close()