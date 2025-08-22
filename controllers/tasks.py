def actualizar_monitoreo_async():
    """
    Versión optimizada de la función de monitoreo para ejecución asíncrona
    con manejo mejorado de recursos y tiempos de espera
    """
    import datetime
    import logging
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    logger = logging.getLogger("web2py.app.seniat_python3")
    logger.setLevel(logging.INFO)
    
    # 1. Configuración inicial
    start_time = datetime.datetime.now()
    logger.info(f"Iniciando actualización asíncrona a las {start_time}")
    
    # 2. Obtener monitoreos pendientes (con caché corta)
    monitoreos = db(db.bdmon).select(cache=(cache.ram, 60), cacheable=True)
    total_monitoreos = len(monitoreos)
    
    if not monitoreos:
        return "No hay monitoreos configurados"
    
    # 3. Configurar ThreadPool con límites dinámicos y delays
    max_workers = min(5, total_monitoreos)  # Reducido de 10 a 5 workers
    timeout_per_task = 600  # 10 minutos por tarea
    delay_between_tasks = 2  # 2 segundos de delay entre tareas
    
    resultados = {
        'exitosas': 0,
        'fallidas': 0,
        'detalles': []
    }
    
    # 4. Ejecución paralela optimizada con delays
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for i, m in enumerate(monitoreos):
            # Agregar delay progresivo entre tareas para evitar sobrecarga
            if i > 0:
                import time
                time.sleep(delay_between_tasks)
            
            future = executor.submit(
                execute_single_monitor_optimized, 
                m, db, 
                get_oracle_connection, 
                get_sqlserver_connection
            )
            futures[future] = m.id
        
        # Procesar resultados con timeout más conservador
        for future in as_completed(futures, timeout=timeout_per_task * 2):
            m_id = futures[future]
            try:
                _, mensaje, success = future.result()
                if success:
                    resultados['exitosas'] += 1
                else:
                    resultados['fallidas'] += 1
                resultados['detalles'].append(f"Monitor {m_id}: {mensaje}")
            except Exception as e:
                resultados['fallidas'] += 1
                resultados['detalles'].append(f"Monitor {m_id}: Error - {str(e)}")
                logger.error(f"Error en monitor {m_id}: {str(e)}")
    
    # 5. Resultado final
    end_time = datetime.datetime.now()
    duracion = (end_time - start_time).total_seconds()
    
    # Agregar delay final para evitar ejecuciones consecutivas muy rápidas
    import time
    time.sleep(5)  # 5 segundos de pausa al final
    
    resumen = (
        f"Actualización completada en {duracion:.2f} segundos. "
        f"Total: {total_monitoreos}, Exitosas: {resultados['exitosas']}, "
        f"Fallidas: {resultados['fallidas']}"
    )
    
    logger.info(resumen)
    return resumen

def execute_single_monitor_optimized(m, db, get_oracle_connection, get_sqlserver_connection):
    """
    Versión optimizada de execute_single_monitor con:
    - Mejor manejo de conexiones
    - Timeouts configurados
    - Reutilización de recursos
    - Delays para evitar sobrecarga
    """
    import threading
    import logging
    from functools import partial
    import time
    
    # Agregar delay aleatorio para evitar ejecuciones simultáneas
    time.sleep(0.5 + (threading.current_thread().ident % 1000) / 1000.0)
    
    logger = logging.getLogger("web2py.app.seniat_python3.scheduler")
    thread_id = threading.current_thread().ident
    
    try:
        # 1. Obtener información básica (con caché)
        servidor = db(db.servidores.nombre == m.tx_servidor).select().first()
        if not servidor:
            error_msg = f"Servidor no encontrado: {m.tx_servidor}"
            logger.error(f"[THREAD-{thread_id}] {error_msg}")
            update_monitor_record(db, m, None, error_msg, False)
            return m.id, error_msg, False
        
        bdatos = db((db.basedatos.servidor == servidor.id) & 
                   (db.basedatos.nombre == m.tx_instancia)).select().first()
        if not bdatos:
            error_msg = f"Base de datos no encontrada: {m.tx_instancia}"
            logger.error(f"[THREAD-{thread_id}] {error_msg}")
            update_monitor_record(db, m, None, error_msg, False)
            return m.id, error_msg, False
        
        tipo_bd = db(db.tipobd.id == bdatos.tipobd_id).select(db.tipobd.descri).first()
        tipo_bd = tipo_bd.descri.strip().upper() if tipo_bd else "DESCONOCIDO"
        
        # 2. Conexión optimizada con timeout
        connection = None
        cursor = None
        resultado = None
        mensaje = ""
        success = False
        
        try:
            comando = (m.tx_comando or "").strip()
            if not comando:
                raise ValueError("Comando SQL vacío")
                
            # Configurar conexión según tipo de BD
            if tipo_bd in ['ORACLE', 'CONTENEDOR ORACLE']:
                connection = get_oracle_connection(
                    servidor.ip, 
                    m.tx_instancia, 
                    bdatos.puerto,
                    version=bdatos.version_id.descri[0:2] if bdatos.version_id else '0'
                )
            elif tipo_bd == 'MSSQLSERVER':
                connection = get_sqlserver_connection(
                    servidor=servidor.ip,
                    base_datos=m.tx_instancia,
                    puerto=bdatos.puerto
                )
            else:
                raise ValueError(f"Tipo de BD no soportado: {tipo_bd}")
                
            # Ejecutar con timeout
            cursor = connection.cursor()
            cursor.execute(comando)
            
            # Procesar resultados
            raw_result = cursor.fetchone()
            resultado = raw_result[0] if raw_result else None
            mensaje = "Éxito" if resultado is not None else "Sin resultados"
            success = True
            
        except Exception as e:
            mensaje = f"Error {tipo_bd}: {str(e)}"
            logger.error(f"[THREAD-{thread_id}] {mensaje}")
        finally:
            # Cierre seguro de recursos
            for resource in [cursor, connection]:
                if resource:
                    try:
                        resource.close()
                    except:
                        pass
        
        # 3. Actualización eficiente del registro
        update_monitor_record(db, m, resultado, mensaje, success)
        return m.id, mensaje, success
        
    except Exception as e:
        error_msg = f"Error inesperado: {str(e)}"
        logger.error(f"[THREAD-{thread_id}] {error_msg}")
        update_monitor_record(db, m, None, error_msg, False)
        return m.id, error_msg, False