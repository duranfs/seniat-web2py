from gluon import *
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------
import logging
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s [%(levelname)s] %(message)s',
	handlers=[
		logging.FileHandler('monitor_oracle.log', encoding='utf-8'),
		logging.StreamHandler()
	]
)
# para evitar que se vea el codigo html cuando le dan F12
response.minify = True  # En tu modelo o controlador

# coding: utf8
### required - do no delete
import sys
import random
import string
#reload(sys)
#sys.setdefaultencoding('utf8')

def user(): return dict(form=auth.login())
def download(): return response.download(request,db)

def call(): 
	session.forget()
	return service()

me = auth.user_id

error_page=URL('error')

### end requires

def error():
	response.flash = T('¡Error no existe id')
	return dict()



# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
	if not request.env.request_method == 'GET': raise HTTP(403)
	return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('ADMIN') # can only be accessed by members of admin groupd
def grid():
	response.view = 'generic.html' # use a generic view
	tablename = request.args(0)
	if not tablename in db.tables: raise HTTP(403)
	grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
	return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
	auth.wikimenu() # add the wiki to the menu
	return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
	"""
	exposes:
	http://..../[app]/default/user/login
	http://..../[app]/default/user/logout
	http://..../[app]/default/user/register
	http://..../[app]/default/user/profile
	http://..../[app]/default/user/retrieve_password
	http://..../[app]/default/user/change_password
	http://..../[app]/default/user/bulk_register
	use @auth.requires_login()
		@auth.requires_membership('group name')
		@auth.requires_permission('read','table name',record_id)
	to decorate functions that need access control
	also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
	"""
	return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action(time_expire=300, cache_model=cache.ram, session=False, vars=True, public=True)
def download():
	"""
	allows downloading of uploaded files
	http://..../[app]/default/download/[filename]
	"""
	return response.download(request, db)



error_page=URL('error')

if not session.recent_companies: session.recent_companies=[]
if not session.recent_persons: session.recent_persons=[]
if not session.servidores_recientes: session.servidores_recientes=[]
if not session.basedatos_recientes: session.basedatos_recientes=[]
if not session.servidor_aux: session.servidor_aux=[]


def add(mylist,item):
	if not item.id in [x[0] for x in mylist]:
		return mylist[:9]+[(item.id,item.name)]
	else:
		return mylist

def add2(mylist,item):
	if not item.id in [x[0] for x in mylist]:
		return mylist[:9]+[(item.id,item.nombre)]
	else:
		return mylist

def add3(mylist,item):
	if not item.id in [x[0] for x in mylist]:
		return mylist[:9]+[(item.id,item.nombre,item.servidor)]
	else:

		return mylist

@auth.requires_membership('ADMIN')
def audit_visitas():
	visited = recently_visited(a=request.applicacion, c="default", f="otheraction")
	return dict(visited=visited, all_visited=session.visited)


def index():
	from gluon import current
	session.a = (session.a or 0) + 1
	nombre = request.env.server_name
	user_ip = request.now.strftime("%c")
	response.flash="Bienvenid@ %s" % auth.user.first_name + " " + auth.user.last_name if auth.user else ''
	#form = crud.create(db.ambiente)
	return dict(host=request.env.http_host, counter=session.a,ip=1,message='(%s)' %nombre, user_ip=user_ip)

def user(): 
	#registros = db(db.auth_user).select(db.auth_user.id.count())
	registros = db(db.auth_user).count()
	if request.args(0) == 'register' and registros and (registros > 100): # limita la cantidad de usuario a registrarse
		form = None
	else:
		#if request.args(0) == 'login' and request.post_vars.username:
		#	request.post_vars.username = request.vars.username = request.post_vars.username.upper()
		form = auth()
		#if form.accepted:
		#	response.flash ='Bievenido'
	#response.flash='Hay '  + str(registros) +  ' usuarios registrados ' 	
	return dict(form=form)




def list_data():
	from datetime import date
	response.generic_patterns = ['*']
	#test_data = {"name":"root" , "children" : [{"name": "Dates", "children": [{"name": "Sunday"}, {"name": "Monday"}, {"name": "Tuesday"}]}]}
	json_list = {"name":"Filters" , "children" : [{"name" : "All"},{"name" : "Nombre" , "children" : None}]}
	vals= []
	for r in db( db.servidores.id>0 ).select( db.servidores.nombre,distinct=True):
		vals.append( {"name" :r.nombre} )

	#if  vals:
	#	if (vals[-1]['name'] != date.today()):
	#		vals.append({"name" : date.today().isoformat()})
	#	else:
	#		json_list['children'][1]["children"] = vals
	#		return json_list
	#else:
	#	vals = [{"name" : date.today().isoformat()}]

	json_list['children'][1]["children"] = vals
	return  json_list

def keygen(size=8,chars=string.ascii_letters + string.digits +"$#%&*+"):
	return ''.join(random.SystemRandom().choice(chars) for _ in range(size))

def get_rows():
	response.generic_patterns = ['json']
	results = []
	filter_str = request.vars.query
	if not filter_str or filter_str == "All" :
		query=(db.basedatos.servidor==db.servidores.id)
	else:
		query = (db.basedatos.servidor==db.servidores.id) & (db.servidores.nombre==filter_str)
	rows = db(query).select(db.basedatos.id,db.basedatos.nombre)

	for r in rows:
		items=r.basedatos.as_dict()
		items.update(r.servidores.as_dict())
		results.append(items)

	return  response.json(results)





def select_bd_servidor():
	servidor_id=request.post_vars.server or request.vars.get("server")
	bases=db(db.basedatos.servidor==servidor_id).select(db.basedatos.id, db.basedatos.nombre, db.basedatos.tipobd_id, orderby=db.basedatos.nombre)
	return dict(bases=bases)
   

@auth.requires_membership('ADMIN')
def user_conn():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#user_conn').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	import datetime
	limit = request.now - datetime.timedelta(minutes=30)
	query = db.auth_event.time_stamp > limit
	query &= db.auth_event.description.contains('Logged-')
	events = db(query).select(db.auth_event.user_id, db.auth_event.description,
		orderby=db.auth_event.user_id|db.auth_event.time_stamp)
	users = []
	for i in range(len(events)):
		last_event = ((i == len(events) - 1) or
					events[i+1].user_id != events[i].user_id)
		if last_event and 'Logged-in' in events[i].description:
			users.append(events[i].user_id)
		logged_in_users = db(db.auth_user.id.belongs(users)).select()
	return dict(conectados=logged_in_users, script=script)


@auth.requires_login()
def monitor_bd():
	from gluon.cache import Cache
	from gluon.scheduler import Scheduler
	import datetime
	tipo_bd = request.args(0) or 9  # Default to 9 if no argument is provided
	#tipo_bd_descri = db(db.tipobd.id == tipo_bd).select(db.tipobd.descri.upper()).first()
	descri = db(db.tipobd.id == tipo_bd).select(db.tipobd.descri.upper()).first()
	tipo_bd_descri = descri._extra['UPPER("tipobd"."descri")']
	# Resultado: 'ORACLE'
	cache = Cache(request)
	now = datetime.datetime.now()
	mensajes = None
	
	# 1. Obtener datos de monitoreo con caché inteligente
	def obtener_datos_actualizados_ORACLE():
		# Solo datos de los últimos 5 minutos
		return db(db.bdmon.f_corrida >= (now - datetime.timedelta(minutes=5)))(db.bdmon.tx_tipobd == tipo_bd_descri) \
			  .select(orderby=db.bdmon.tx_servidor|db.bdmon.tx_tipobd|db.bdmon.tx_puerto|db.bdmon.tx_instancia|db.bdmon.tx_rutina)
	
	mon = cache.ram('datos_monitoreo', obtener_datos_actualizados_ORACLE, time_expire=1)
	
	# 2. Verificar si necesitamos actualización (versión corregida)
	necesita_actualizar = True
	ultima_actualizacion = db(db.bdmon.tx_tipobd==tipo_bd_descri).select(db.bdmon.f_corrida, orderby=~db.bdmon.f_corrida).first()
	
	if ultima_actualizacion and ultima_actualizacion.f_corrida:
		# Convertir datetime.date a datetime.datetime si es necesario
		if isinstance(ultima_actualizacion.f_corrida, datetime.date):
			ultima_actualizacion_dt = datetime.datetime.combine(
				ultima_actualizacion.f_corrida, 
				datetime.time.min
			)
		else:
			ultima_actualizacion_dt = ultima_actualizacion.f_corrida
		
		diferencia = now - ultima_actualizacion_dt
		if diferencia.total_seconds() < 3:  # 5 minutos
			necesita_actualizar = False
	
	# 3. Procesamiento asíncrono si es necesario
	if necesita_actualizar:
		try:
			scheduler = Scheduler(db)
			# Verificar si ya hay una tarea en progreso
			if not scheduler.task_status('actualizar_monitoreo_async', status='RUNNING'):
				scheduler.queue_task(
					'actualizar_monitoreo_async', 
					timeout=1,  # 20 minutos de timeout
					sync_output=5,
					immediate=True
				)
				mensajes = "Los datos se están actualizando en segundo plano..."
			else:
				mensajes = "Actualización en progreso... (por favor espere)"
		except Exception as e:
			# Fallback seguro con logging
			import traceback
			tb = traceback.format_exc()
			#db.log.insert(tipo='ERROR', descripcion=f"Error en scheduler: {str(e)}\n{tb}")
			
			mensajes = "Iniciando actualización directa (modo seguro)..."
			try:
				resultado = actualizar_y_mostrar_monitor_parallel()
				if resultado and 'resumen' in resultado:
					mensajes = resultado['resumen']
				mon = obtener_datos_actualizados_ORACLE()
			except Exception as e2:
				mensajes = "Error en actualización directa"
				#db.log.insert(tipo='ERROR', descripcion=f"Error en actualización directa: {str(e2)}")
	
	# 4. Obtener lista de bases de datos (con caché extendido)
	def obtener_basedatos():
		return db(db.basedatos.status_mon.upper() == 'SI').select(
			db.basedatos.id,
			db.basedatos.nombre,
			db.basedatos.servidor,
			db.basedatos.tipobd_id,
			db.basedatos.version_id,
			db.basedatos.puerto,
			db.basedatos.ambiente_id,
			cache=(cache.ram, 10),  # Cache por 1 hora
			cacheable=True
		)
	
	basedatos_mon = obtener_basedatos()
	
	return dict(
		mon=mon, 
		mensajes=mensajes, 
		ultima_actualizacion=now, 
		basedatos_mon=basedatos_mon,
		necesita_actualizar=necesita_actualizar,
		tipo_bd_descri=tipo_bd_descri

	)


#------- en paralelo ------------------------------------------------------------------------

from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
import traceback
import logging
import threading

def execute_single_monitor(m, db, get_oracle_connection, get_sqlserver_connection):
	"""Versión final adaptada para múltiples tipos de bases de datos"""
	try:
		thread_id = threading.current_thread().ident
		logging.info(f"[THREAD-{thread_id}] Iniciando monitoreo: {m.tx_instancia}@{m.tx_servidor}")
		
		try:
			servidor = db(db.servidores.nombre == m.tx_servidor).select().first()
			if not servidor:
				error_msg = f"Servidor no encontrado: {m.tx_servidor}"
				logging.error(f"[THREAD-{thread_id}] {error_msg}")
				update_monitor_record(db, m, None, error_msg, False)
				return m.id, error_msg, False
		except Exception as e:
			error_msg = f"Error al buscar servidor: {str(e)}"
			logging.error(f"[THREAD-{thread_id}] {error_msg}")
			update_monitor_record(db, m, None, error_msg, False)
			return m.id, error_msg, False

		# Obtener información completa de la base de datos
		try:
			bdatos = db((db.basedatos.servidor == servidor.id) & 
					   (db.basedatos.nombre == m.tx_instancia)).select(
					   db.basedatos.puerto, 
					   db.basedatos.version_id,
					   db.basedatos.tipobd_id).first()
			
			if not bdatos:
				error_msg = f"Base de datos no encontrada: {m.tx_instancia}"
				logging.error(f"[THREAD-{thread_id}] {error_msg}")
				update_monitor_record(db, m, None, error_msg, False)
				return m.id, error_msg, False
		except Exception as e:
			error_msg = f"Error al buscar base de datos: {str(e)}"
			logging.error(f"[THREAD-{thread_id}] {error_msg}")
			update_monitor_record(db, m, None, error_msg, False)
			return m.id, error_msg, False

		# Obtener tipo de base de datos
		tipo_bd = db(db.tipobd.id == bdatos.tipobd_id).select(db.tipobd.descri).first()
		if not tipo_bd:
			error_msg = f"Tipo de base de datos no definido para: {m.tx_instancia}"
			logging.error(f"[THREAD-{thread_id}] {error_msg}")
			update_monitor_record(db, m, None, error_msg, False)
			return m.id, error_msg, False

		tipo_bd = tipo_bd.descri.strip().upper()
		
		resultado = None
		mensaje = ""
		success = False
		connection = None
		cursor = None
		rutina = m.tx_rutina
		
		try:
			comando = (m.tx_comando or "").strip()
			if not comando:
				raise ValueError("Comando SQL vacío o nulo")
				
			if comando.count("'") % 2 != 0 or comando.count('"') % 2 != 0:
				raise ValueError("Comando SQL con comillas sin cerrar")
				
			comando = comando.rstrip(';')
			
			# Conexión según tipo de base de datos
			if tipo_bd in ['ORACLE', 'CONTENEDOR ORACLE']:
				# Configuración específica para Oracle
				dominio = servidor.dominio.lower() if servidor.dominio else ""
				service_name = f"{m.tx_instancia}.{dominio}" if dominio else m.tx_instancia
				ver_str = bdatos.version_id.descri[0:2].replace('.', '') if bdatos.version_id else '0'
				ver = int(ver_str) if ver_str.isdigit() else 0
				
				logging.info(f"[THREAD-{thread_id}] Conectando a Oracle: {servidor.ip}:{bdatos.puerto}/{service_name}")
				connection = get_oracle_connection(servidor.ip, service_name, bdatos.puerto, ver)
				cursor = connection.cursor()
				
			elif tipo_bd == 'MSSQLSERVER':
				# Configuración específica para SQL Server
				logging.info(f"[THREAD-{thread_id}] Conectando a SQL Server: {servidor.ip}:{bdatos.puerto}/{m.tx_instancia}")
				connection = get_sqlserver_connection(
					servidor=servidor.ip,
					base_datos=m.tx_instancia,
					puerto=bdatos.puerto,
					controlador='ODBC Driver 17 for SQL Server'
				)
				cursor = connection.cursor()
				
			elif tipo_bd in ['POSTGRESQL', 'DOCKER-KUBERNETES-PGSQL']:
				# Configuración para PostgreSQL (requiere implementación)
				error_msg = f"Conexión PostgreSQL no implementada aún para: {m.tx_instancia}"
				logging.error(f"[THREAD-{thread_id}] {error_msg}")
				update_monitor_record(db, m, None, error_msg, False)
				return m.id, error_msg, False
				
			elif tipo_bd in ['MYSQL', 'MARIADB', 'DOCKER-KUBERNETES-MYSQL']:
				# Configuración para MySQL/MariaDB (requiere implementación)
				error_msg = f"Conexión MySQL/MariaDB no implementada aún para: {m.tx_instancia}"
				logging.error(f"[THREAD-{thread_id}] {error_msg}")
				update_monitor_record(db, m, None, error_msg, False)
				return m.id, error_msg, False
				
			elif tipo_bd == 'MONGODB':
				# Configuración para MongoDB (requiere implementación)
				error_msg = f"Conexión MongoDB no implementada aún para: {m.tx_instancia}"
				logging.error(f"[THREAD-{thread_id}] {error_msg}")
				update_monitor_record(db, m, None, error_msg, False)
				return m.id, error_msg, False
				
			else:
				error_msg = f"Tipo de base de datos no soportado: {tipo_bd}"
				logging.error(f"[THREAD-{thread_id}] {error_msg}")
				update_monitor_record(db, m, None, error_msg, False)
				return m.id, error_msg, False
				
			# Ejecución del comando (común para todos los tipos)
			logging.info(f"[THREAD-{thread_id}] Ejecutando comando en {m.tx_instancia} ({tipo_bd})")
			cursor.execute(comando)
			
			# Procesamiento de resultados
			try:
				raw_result = cursor.fetchone()
				if raw_result:
					resultado = raw_result[0] if len(raw_result) == 1 else raw_result
					if isinstance(resultado, (int, float)) and resultado == 0:
						mensaje = f"Advertencia: Resultado cero en {m.tx_instancia}"
					else:
						mensaje = f"Éxito - Resultado: {resultado}"
				else:
					mensaje = "Éxito - Sin resultados"
				success = True
				
			except Exception as fetch_error:
				mensaje = f"Error al obtener resultados: {str(fetch_error)}"
				logging.warning(f"[THREAD-{thread_id}] {mensaje}")
				
		except Exception as db_error:
			mensaje = f"Error de {tipo_bd}: {servidor.ip} {rutina} {m.tx_instancia} - {str(db_error)}"
			logging.error(f"[THREAD-{thread_id}] {mensaje}")
			
		finally:
			# Cierre seguro de recursos
			for resource in [cursor, connection]:
				if resource:
					try:
						resource.close()
					except Exception as close_error:
						logging.warning(f"[THREAD-{thread_id}] Error al cerrar recurso: {str(close_error)}")
		
		# Actualización de resultados
		try:
			update_monitor_record(db, m, resultado, mensaje, success)
		except Exception as update_error:
			logging.error(f"[THREAD-{thread_id}] Error al actualizar registro: {str(update_error)}")
			return m.id, f"Error al guardar resultados: {str(update_error)}", False
		
		return m.id, mensaje, success
		
	except Exception as e:
		error_msg = f"Error inesperado: {str(e)}"
		logging.error(f"[THREAD-{thread_id}] {error_msg}\n{traceback.format_exc()}")
		try:
			update_monitor_record(db, m, None, error_msg, False)
		except:
			pass
		return m.id, error_msg, False

def actualizar_y_mostrar_monitor_parallel():
	"""Función principal para monitoreo paralelo multi-BD"""
	logging.info("[MAIN] Iniciando monitoreo paralelo de instancias...")
	
	monitoreos = db(db.bdmon).select()
	
	conexiones_exitosas = 0
	conexiones_fallidas = 0
	resultados = {}
	
	with ThreadPoolExecutor(max_workers=10) as executor:
		futures = {
			executor.submit(execute_single_monitor, m, db, get_oracle_connection, get_sqlserver_connection): m
			for m in monitoreos
		}
		
		for future in as_completed(futures):
			m = futures[future]
			try:
				m_id, mensaje, success = future.result()
				logging.info(f"[MAIN] Resultado para {m.tx_instancia} ({m.id}): {mensaje[:100]}...")
				if success:
					conexiones_exitosas += 1
				else:
					conexiones_fallidas += 1
				resultados[m_id] = mensaje
			except Exception as e:
				conexiones_fallidas += 1
				resultados[m.id] = f"Error inesperado: {str(e)}"
				logging.error(f"[MAIN] ERROR inesperado en {m.tx_instancia}: {str(e)}\n{traceback.format_exc()}")
	
	# Generar reporte resumen por tipo de BD
	resumen = (
		f"Proceso completado. Total: {len(monitoreos)}, "
		f"Exitosas: {conexiones_exitosas}, Fallidas: {conexiones_fallidas}"
	)
	
	# Ordenar mensajes por ID de monitor
	mensajes_ordenados = [resultados[id] for id in sorted(resultados.keys())]
	mensajes_ordenados.insert(0, resumen)
	logging.info(f"[MAIN] {resumen}")
	
	return dict(
		mensajes=mensajes_ordenados,
		resumen=resumen,
		exitosas=conexiones_exitosas,
		fallidas=conexiones_fallidas
	)

def update_monitor_record(db, monitor, resultado, mensaje, success):
	"""Función mejorada con caché inteligente y manejo robusto de errores"""
	try:
		# Obtener el timestamp actual una sola vez
		ahora = datetime.datetime.now()
		
		# Verificar si necesitamos actualizar
		necesita_actualizar = True
		
		# Comprobar si podemos usar caché (solo si tenemos un resultado previo válido)
		registro_actual = db(db.bdmon.id == monitor.id).select(
			db.bdmon.f_corrida, 
			db.bdmon.tx_resultado
		).first()
		
		if registro_actual and registro_actual.f_corrida and registro_actual.tx_resultado is not None:
			# Convertir a datetime si es necesario
			fecha_corrida = registro_actual.f_corrida
			if isinstance(fecha_corrida, datetime.date):
				fecha_corrida = datetime.datetime.combine(fecha_corrida, datetime.time.min)
			
			# Calcular diferencia
			diferencia = ahora - fecha_corrida
			
			# Usar caché si los datos son recientes (menos de 5 minutos)
			if diferencia < datetime.timedelta(minutes=5):
				logging.info(f"[CACHÉ] Usando datos recientes para {monitor.id} (actualizado hace {diferencia.total_seconds()} segundos)")
				necesita_actualizar = False
		
		# Actualizar solo si es necesario
		if necesita_actualizar:
			update_data = {
				'tx_resultado': str(resultado) if resultado is not None else None,
				'tx_resultado_detalle': mensaje[:4000] if mensaje else None,
				'f_corrida': ahora,
				'estado': 'OK' if success else 'ERROR'
			}
			
			# Actualización con verificación
			try:
				db(db.bdmon.id == monitor.id).update(**update_data)
				db.commit()
				logging.info(f"[ACTUALIZACIÓN] Registro {monitor.id} actualizado correctamente")
			except Exception as e:
				db.rollback()
				logging.error(f"[ERROR] Fallo al actualizar {monitor.id}: {str(e)}")
				raise
		
		return necesita_actualizar
		
	except Exception as e:
		logging.error(f"[ERROR CRÍTICO] En update_monitor_record: {str(e)}\n{traceback.format_exc()}")
		raise



#------ en paralelo ------------------------------------------------------------------------



def prueba_9i():
	mensaje = []
	resultado = []
	rutina = ""
	ver = ""
	conexiones_exitosas = 0
	conexiones_fallidas = 0
	
	# Obtener todos los registros a procesar
	#registros = db(db.bdmon)(db.bdmon.tx_servidor=='LAGUAIRA1')(db.bdmon.tx_rutina=='SESIONES>90%').select()
	registros = db(db.bdmon)(db.bdmon.tx_servidor=='LAGUAIRA1').select()
	
	for m in registros:
		try:
			servidor = db(db.servidores.nombre==m.tx_servidor).select().first()
			if not servidor:
				mensaje.append(f"Servidor no encontrado: {m.tx_servidor}")
				continue
				
			bdatos = db(db.basedatos.servidor == servidor.id)(db.basedatos.nombre == m.tx_instancia)\
					 .select(db.basedatos.puerto, db.basedatos.version_id).first()
			if not bdatos:
				mensaje.append(f"Base de datos no encontrada: {m.tx_instancia}")
				continue
				
			ver = int(bdatos.version_id.descri[0:2].replace('.', ''))
			
			try:
				connection = get_oracle_connection_9i("172.16.32.147", "ASY_DB1", 1525, ver)
				conexiones_exitosas += 1
			except Exception as e:
				mensaje.append(f"Error de conexión: {str(e)}")
				conexiones_fallidas += 1
				continue
				
			try:
				cursor = connection.cursor()
				rutina += m.tx_rutina + " , "
				comando = m.tx_comando
				
				cursor.execute(comando)
				resultado_query = cursor.fetchone()
				if resultado_query:
					resultado.append(resultado_query[0])
				else:
					resultado.append("Sin resultados")
					
				mensaje.append(f"Conexión exitosa a: {connection}")
				
			except Exception as e:
				mensaje.append(f"Error ejecutando query: {str(e)}")
				resultado.append(f"Error en query: {m.tx_rutina}")
				
			finally:
				if 'cursor' in locals() and cursor is not None:
					cursor.close()
				if 'connection' in locals() and connection is not None:
					connection.close()
					
		except Exception as e:
			mensaje.append(f"Error general procesando registro: {str(e)}")
			continue
			
	return dict(
		resultado=resultado, 
		mensaje=mensaje, 
		rutina=rutina, 
		ver=ver,
		conexiones_exitosas=conexiones_exitosas,
		conexiones_fallidas=conexiones_fallidas
	)


@auth.requires_login()
def asignar_rutinas():
	"""
	Asigna rutinas de monitoreo a servidores - Versión compatible con Web2py 3.12+
	"""
	# Cachear consultas de servidores y rutinas (válido por 1 hora)
	cache_key = f"asignar_rutinas_data_{request.now}"
	cached_data = cache.ram(cache_key, lambda: None, time_expire=100)
	
	if cached_data is None:
		# Consulta optimizada para servidores
		servidores = db((db.servidores.id > 0) & 
					   (db.servidores.status_mon == 'SI')).select(
					   orderby=db.servidores.nombre,
					   cache=(cache.ram, 100))
		
		# Consulta optimizada para rutinas
		rutinas = db(db.rutinas.id > 0).select(
				  orderby=db.rutinas.nombre,
				  cache=(cache.ram, 100))
		cached_data = (servidores, rutinas)
	else:
		servidores, rutinas = cached_data
	
	# Procesamiento de parámetros
	servidores_seleccionados = []
	if request.vars.servidores:
		servidores_seleccionados = request.vars.servidores
		if not isinstance(servidores_seleccionados, list):
			servidores_seleccionados = [servidores_seleccionados]
	
	# Precarga de rutinas asignadas
	rutinas_asignadas = []
	if len(servidores_seleccionados) >= 1:
		try:
			servidor_id = int(servidores_seleccionados[0])
			rutinas_asignadas = [str(r.rutina) for r in 
							   db(db.rutina_status.servidor_id == servidor_id).select(
							   cache=(cache.ram, 100))]
		except ValueError:
			pass
	
	# Procesamiento de asignaciones
	if request.vars.rutinas and servidores_seleccionados:
		rutinas_seleccionadas = request.vars.rutinas
		if isinstance(rutinas_seleccionadas, str):
			rutinas_seleccionadas = [rutinas_seleccionadas]
		
		try:
			# Validación y conversión de IDs
			serv_ids = [int(sid) for sid in servidores_seleccionados if sid.isdigit()]
			rutina_ids = [int(rid) for rid in rutinas_seleccionadas if rid.isdigit()]
			
			if len(serv_ids) != len(servidores_seleccionados) or len(rutina_ids) != len(rutinas_seleccionadas):
				raise ValueError("IDs no válidos detectados")
			
			# Verificación de existencia
			if db(db.servidores.id.belongs(serv_ids)).count() != len(serv_ids):
				raise ValueError("Algunos servidores no existen")
				
			if db(db.rutinas.id.belongs(rutina_ids)).count() != len(rutina_ids):
				raise ValueError("Algunas rutinas no existen")
			
			# Transacción atómica
			db.commit()  # Cerrar transacciones pendientes
			
			try:
				for servidor_id in serv_ids:
					db(db.rutina_status.servidor_id == servidor_id).delete()
					tipobd = db(db.basedatos.servidor == servidor_id).select().first()
					if tipobd:
						db.rutina_status.bulk_insert([
							{'servidor_id': servidor_id, 'rutina': rutina_id, 'tipobd_id': tipobd.tipobd_id}
							for rutina_id in rutina_ids
						])
				
				db.commit()
				response.flash = 'Rutinas asignadas correctamente'
				
				# Invalidar caché
				cache.ram.clear(regex='^asignar_rutinas_data_.*')
				
				# Llamada a guarda_log_bdmon() sin scheduler
				guarda_log_bdmon()
				
			except Exception as e:
				db.rollback()
				raise HTTP(500, f"Error en asignación: {str(e)}")
				
		except ValueError as ve:
			raise HTTP(400, str(ve))
		
	elif not request.vars.rutinas and servidores_seleccionados:
		serv_ids = [int(sid) for sid in servidores_seleccionados if sid.isdigit()]
		db.commit()  # Cerrar transacciones pendientes
		try:
				for servidor_id in serv_ids:
					db(db.rutina_status.servidor_id == servidor_id).delete()
				
				db.commit()
				response.flash = 'Rutinas eliminadas correctamente'
				guarda_log_bdmon()
		except Exception as e:
				db.rollback()
				raise HTTP(500, f"Error en eliminacion: {str(e)}")
			
			
	return dict(
		servidores=servidores,
		rutinas=rutinas,
		rutinas_asignadas=rutinas_asignadas,
		servidores_seleccionados=servidores_seleccionados
	)

def guarda_log_bdmon():
	from datetime import datetime
	
	# En lugar de TRUNCATE que bloquea toda la tabla
	db(db.bdmon).delete()  # DELETE es menos bloqueante
	db.commit()  # Commit inmediato para liberar locks
	
	todas_rutinas = db(db.rutina_status).select()
	fecha_actual = datetime.now()
	
	# Pre-cargar relaciones para evitar N+1
	rutinas = db(db.rutinas.id.belongs([r.rutina for r in todas_rutinas])).select()
	servidores = db(db.servidores.id.belongs([r.servidor_id for r in todas_rutinas])).select()
	
	# Procesamiento por lotes
	batch_size = 100
	batch = []
	
	for rutina in todas_rutinas:
		bases_datos = db(db.basedatos.servidor == rutina.servidor_id)(
					  db.basedatos.status_mon == 'SI').select()
		
		for bd in bases_datos:
			batch.append({
				'tx_ambiente': next(s.ambiente_id.descri for s in servidores if s.id == rutina.servidor_id),
				'tx_servidor': next(s.nombre for s in servidores if s.id == rutina.servidor_id),
				'tx_instancia': bd.nombre,
				'tx_puerto': bd.puerto,
				'tx_tipobd': rutina.tipobd_id.descri,
				'tx_rutina': next(r.nombre for r in rutinas if r.id == rutina.rutina),
				'tx_comando': next(r.sql_code for r in rutinas if r.id == rutina.rutina),
				'tx_resultado': "",
				'f_corrida': fecha_actual
			})
			
			if len(batch) >= batch_size:
				db.bdmon.bulk_insert(batch)
				batch = []
	
	if batch:
		db.bdmon.bulk_insert(batch)
	
	db.commit()


def rutinas_asignadas():
	# Esta función ahora es muy simple porque la vista hace las consultas directamente
	return dict()

def manage_assignmentXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	response.view = 'generic.json'
	
	try:
		rutina_id = request.vars.rutina_id
		servidor_id = request.vars.servidor_id
		action = request.vars.action
		
		if not (rutina_id and servidor_id and action):
			return dict(success=False, message="Parámetros incompletos")
		
		if action == 'add' or action == 'update':
			status = request.vars.status or 'HABILITADO'
			
			# Buscar si ya existe
			registro = db((db.rutina_status.rutina == rutina_id) & 
						 (db.rutina_status.servidor_id == servidor_id)).select().first()
			
			if registro:
				registro.update_record(status=status)
			else:
				db.rutina_status.insert(
					rutina=rutina_id,
					servidor_id=servidor_id,
					status=status,
					is_active='T'
				)
				
		elif action == 'remove':
			db((db.rutina_status.rutina == rutina_id) & 
			   (db.rutina_status.servidor_id == servidor_id)).delete()
		
		return dict(success=True)
		
	except Exception as e:
		return dict(success=False, message=str(e))




@auth.requires_login()
def detalle_estructuraXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	basedatos_nombre=request.args[0]
	#basedatos_nombre=request.args(0) es diferente a tener []
	
	bs=db.basedatos_estructura
	#servidor=db.servidores[servidor_id] or redirect(error_page)
	#session.servidores_recientes = add2(session.servidores_recientes,servidor)
	
	#r=db.executesql('select cola,colb from mytable;')
	#r[0][0] is cols and r[0][1] is col b. It does not matter in which
	#order they were in the table definition[All that amatters is the order with which you made the query].
	
	#r = db.executesql('select soso, lolo from my_table')
	#print r  # [(u'a', u'c')]
	#print r[0][0], r[0][1] #a c
	#return dict()
	
	
	now = datetime.datetime.now()
	span = datetime.timedelta(days=1)
	
	#q = db()._select(bs.fecha_act)
	
	query = (bs.nombre == basedatos_nombre) & (bs.fecha_act >= request.now.date())
	#query = (bs.nombre == basedatos_nombre) & (bs.fecha_act >= now-span)
	rows  = db(query).select(
		bs.tablespace.with_alias("Tablespace"),
		bs.datafiles.with_alias("Datafiles"),
		bs.espacio.with_alias("Tamaño"),
		bs.sp_ocupado.with_alias("Ocupado"),
		bs.sp_libre.with_alias("Libre"),
		bs.porc_ocupado.replace('X','â–ˆ').replace('-','â”€').with_alias("Porc_ocupado"),
		bs.porc_libre.with_alias("Porc_libre"),
		bs.fecha_act
		#bs.fecha_act.belongs(q)
		)
	print (db._lastsql)
	estructuras = db(query).select(bs.ALL)
	#form=SQLFORM.factory(*[Field('need_%s'%item.id, default=item.cantidad) for item in items])
	form=TABLE(TR(*[TD('need_%s'%est.id, default=est.tablespace) for est in estructuras]))
	table  = SQLTABLE(rows, _id="estructura", linkto=URL(f="cargar"), headers="fieldname:capitalize")
	
	return dict(basedatos_nombre=basedatos_nombre, table=table, form=form)


@auth.requires_login()
def claves_manage():
	
	claves = db(db.t_claves.f_servidor>0 ).select(orderby=db.t_claves.f_servidor)
	#form = crud.create(db.t_claves)
	return dict(claves=claves)


@auth.requires_login()
def todas_las_clavesxxXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX(): #maestro de claves query
	todas_las_claves = db(db.servidores.id>0)\
	(db.basedatos.servidor==db.servidores.id).\
	select(orderby=db.servidores.nombre|db.basedatos.tipobd_id|db.basedatos.nombre,  cacheable=True)
	return dict(todas_las_claves=todas_las_claves)

@auth.requires_login()
def todas_las_clavesXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX(): #maestro de claves query
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#todas_las_claves').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	todas_las_claves = db(db.servidores.id>0)\
	(db.servidores.id==db.cuentas_so.servidor_id).\
	select(orderby=db.servidores.nombre,  cacheable=False)
	return dict(todas_las_claves=todas_las_claves, script=script)

@auth.requires_login()
def claves_managexXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	
	servidores = db(db.t_claves.id>0).select()
	
	
	form = crud.create(db.t_claves)
	#form = crud.search(db.t_claves, query=db.t_claves.id>0)
	#form = SQLFORM(db.t_claves, headers='fieldname:capitalize')
	servidores = db().select(db.servidores.id,db.servidores.nombre,db.basedatos.nombre)
	return dict(form=form, servidores=servidores)

def error(message="No autorizado"):
	session.flash = message
	redirect(URL('index'))



def indexxxxXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	now = datetime.datetime.now()
	span = datetime.timedelta(days=10)
	product_list = db(db.task.created_on >= (now-span)).select(limitby=(0,3), orderby=~db.task.created_on)
	return locals()

def reporte_novedadesxXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	#generates a html form to filter the data to be displayed in the report
	form = plugin_appreport.REPORTFORM(table=task_guardias)

	if form.accepts(request.vars, session):
		#build a report based on table fields (aka auto generates html) and filters informed in form
		return plugin_appreport.REPORTPISA(table = task_guardias, args = dict(form.vars))

	return dict(form = form)



def createReportXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	import os
	import uuid
	import subprocess   
	from appy.pod.renderer import Renderer
	persons = []
	for person in db(db.auth_user).select():
		persons.append(dict(name=person.first_name,
							surname=person.last_name,
							adress=person.email))            
	# Report creation               
	template_file = os.path.join(request.folder, 'private', 'template.odt')
	tmp_uuid = uuid.uuid4()        
	#output_file_odt = "/var/tmp/%s.odt"%tmp_uuid
	#output_file_pdf = "/var/tmp/%s.pdf"%tmp_uuid                                                            
	output_file_odt = "/tmp/%s.odt"%tmp_uuid
	output_file_pdf = "/tmp/%s.pdf"%tmp_uuid                                                            
	beingPaidForIt = True     
	renderer = Renderer(template_file, locals(), output_file_odt)
	renderer.run()                          
	#subprocess.Popen("libreoffice --headless --invisible --convert-to pdf %s --outdir %s "%(output_file_odt, "/tmp") ,shell=True)                                                     
	subprocess.Popen("libreoffice --headless --convert-to pdf %s --outdir %s "%(output_file_odt, "/tmp") ,shell=True)                                                     
	#subprocess.Popen("swriter --headless --convert-to pdf %s --outdir %s "%(output_file_odt, "/tmp/") ,shell=True) 
	while True:
		if os.path.exists(output_file_pdf):
			break
	data = open(output_file_pdf, "rb").read()                 
	for file in [output_file_odt, output_file_pdf]:
		os.unlink(file)                                                                                                                                                                                                                      
	response.headers['Content-Type'] = 'application/pdf'
	response.headers['Content-Disposition'] = 'attachment; filename=RepNovedades.pdf'
	return data                                                             
	


def reportxxxXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	response.title = "web2py sample report"

	# include a google chart (download it dynamically!)
	url = "http://chart.apis.google.com/chart?cht=p3&chd=t:60,40&chs=500x200&chl=Hello|World&.png"
	chart = IMG(_src=url, _width="250", _height="100")

	# create a small table with some data:
	rows = [THEAD(TR(TH("Key", _width="70%"), TH("Value", _width="30%"))),
			TBODY(TR(TD("Hello"), TD("60")), 
				  TR(TD("World"), TD("40")))]
	rows = db(db.task_guardias).select()
	table = TABLE(*rows, _border="0", _align="center", _width="50%")

	if request.extension != "pdf":
		from gluon.contrib.pyfpdf import FPDF, HTMLMixin

		# create a custom class with the required functionality 
		class MyFPDF(FPDF, HTMLMixin):
			def header(self): 
				"hook to draw custom page header (logo and title)"
				#logo = os.path.join(request.env.web2py_path, "gluon", "contrib", "pyfpdf", "tutorial", "logo_pb.png")
				#self.image(logo, 10, 8, 33)
				self.set_font('Arial', 'B', 15)
				self.cell(65) # padding
				self.cell(60, 10, response.title, 1, 0, 'C')
				self.ln(20)

			def footer(self):
				"hook to draw custom page footer (printing page numbers)"
				self.set_y(-15)
				self.set_font('Arial', 'I', 8)
				txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
				self.cell(0, 10, txt, 0, 0, 'C')

		pdf = MyFPDF()
		# create a page and serialize/render HTML objects
		pdf.add_page()
		pdf.write_html(str(XML(table, sanitize=False)))
		pdf.write_html(str(XML(CENTER(chart), sanitize=False)))
		# prepare PDF to download:
		response.headers['Content-Type'] = 'application/pdf'
		return pdf.output(dest='S')
	else:
		# normal html view:
		return dict(chart=chart, table=table)

#from plugin_sqleditable.editable import SQLEDITABLE
#SQLEDITABLE.init()

#Funcion para probar si es accesible todos los servidores y si el proceso esta levantado
def test_port_sshXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	import socket
	import sys
	server_id=request.args[0]
	server=db(db.servidores.id==server_id).select(db.servidores.nombre, db.servidores.ip)
	#server=systemd(systemd.server.id==server_id).select().ALL
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(60)
	try:
		#sock.connect((server[0].ip, server[0].port))
		sock.connect((server[0].ip, 22))
	except Exception as e:
		print ("%s closed " % (server[0].port))
		return '<span style="color:red;">FAIL</span>'
	else:
		return '<span style="color:green;">OK</span>'
	
	sock.close()
	return local()        



def test_connect_sshXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	import sys, paramiko
	server_id=request.args[0]
	server=systemd(systemd.server.id==server_id).select(systemd.server.name, systemd.server.ip, systemd.server.port)
	conexion = paramiko.SSHClient()
	conexion.load_system_host_keys()
  
	try:
		conexion.connect(server[0].ip, server[0].port, username = ssh_user_admin, key_filename = rsa_private_key_admin)
		#stdin, stdout, stderr = conexion.exec_command('echo "conectado..."')
	
	
	except Exception as e:
		return '<span style="color:red;">FAIL</span>'
		conexion.close()
	else:
		#Only tested on Linux, maybe works for Solaris
		#stdin, stdout, stderr = conexion.exec_command('ps -ef | grep procallator | grep -v grep | awk {'+"'"+'print $2'+"'"+'}')
		stdin, stdout, stderr = conexion.exec_command('ps -e')
		result=stdout.read()
		conexion.close()

	if result:
		message='ORCA running'
	else:
		message='<span style="color:red;">ORCA stoped</span>'
		return '<span style="color:green;">OK, '+message+'</span>'

def demo10XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	response.title = 'demo10'
	response.view = 'plugin_sqleditable/sample.html'
	editable = SQLEDITABLE(db.rutina_status, showid=False, maxrow=20).process()
	return dict(editable=editable)


	
def valida_rutina():
	if request.vars and 'hab_des' in request.vars and request.vars.hab_des:
		if request.vars.get('ret')=='DESHABILITADO':
			response.flash = "Habilitado"
			db(db.rutina_status.id == request.vars.get('hab_des')).update(status = 'HABILITADO')
			
		else:
			response.flash = "Deshabilitado"
			db(db.rutina_status.id == request.vars.get('hab_des')).update(status = 'DESHABILITADO')
	elif request.vars and 'todos' in request.vars and request.vars.todos:
		response.flash = "Todos"
		if request.vars.get('todos')=='SI':
			response.flash = "Exito" 
			db(db.rutina_status).update(status = 'HABILITADO')
			db.commit()
		else:
			db(db.rutina_status).update(status = 'DESHABILITADO')
			db.commit()
	#r=db.executesql('update bdmon set status=rutina_status.status from rutina_status where rutina_status.rutina = tx_rutina and f_corrida >=current_date::timestamp;')
	##--revisar aqui ----------------------
	##r=db.executesql('update bdmon set status=rutina_status.status from rutina_status where rutina_status.rutina.nombre = tx_rutina;')
	db.commit()
	response.flash = "Exito" 
	redirect(URL('list_rutina_status'))
	return	 locals()   
  
def valida_resaltado():
	if request.vars and 'si_no' in request.vars and request.vars.si_no: 
		if request.vars.get('res')=='NO':
			response.flash = "Si"
			db(db.rutina_status.id == request.vars.get('si_no')).update(resaltado = 'SI')
			
		else:
			response.flash = "No"
			db(db.rutina_status.id == request.vars.get('si_no')).update(resaltado = 'NO')
	elif request.vars and 'todos' in request.vars and request.vars.todos:
		response.flash = "Todos"
		if request.vars.get('todos')=='SI':
			db(db.rutina_status).update(resaltado = 'SI')
			db.commit()
		else:
			db(db.rutina_status).update(resaltado = 'NO')
			db.commit()
	#r=db.executesql('update bdmon set status=rutina_status.status from rutina_status where rutina_status.rutina = tx_rutina and f_corrida >=current_date::timestamp;')
	#r=db.executesql('update bdmon set resaltado=rutina_status.status from rutina_status where rutina_status.rutina = tx_rutina;')
	#db.commit()	 
	redirect(URL('list_rutina_status'))
	return	 locals()   
 

import subprocess

def get_command_result(command):
	"""
	Used to execute terminal commands and get the return result
		 :param command: command to be executed
	:return:
	"""
	output_stdout, output_error = "None1", "None2"
	try:
		popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, bufsize=4096)
		output_stdout, output_error = popen.communicate()
	except Exception as e:
		print("exec command error: {}".format(e))
	finally:
		return output_stdout.decode(), output_error.decode()

def lista_rman12_onlineXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	import subprocess
	return locals()

def reporte_rman12XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	from gluon.tools import Expose
	output_stdout, output_error = "None1", "None2"
	usuario="oracle12"
	servidor="sun2315p"
	password="Oracle$123"
	test_ip = "oracle12@sun2315p"

	#comando = "/home/oracle12/exec_remoto.sh 'sun2315p' 'oracle12' Oracle$123 'monitorbd/report_rman.sh'"
	#comando = "sh - oracle12 -c /home/oracle12/trae_report.sh; su - oracle12 -c /home/oracle12/get.sh"
	#comando = "sh - oracle12 -c 'rm /home/oracle12/*.txt'; sh - oracle12 - c '/home/oracle12/trae_report.sh;'"
	comando = request.folder + "/private/trae_report.sh"
	proceso = subprocess.Popen(str(comando), 
		shell=True, 
		stdout = subprocess.PIPE, 
		stderr = subprocess.PIPE,
		stdin = subprocess.PIPE, 
		universal_newlines=True)
	salida = proceso.communicate()
	#return dict(files=Expose('/home/oracle12', basename='.', extensions=['.txt']), salida=salida)
	return dict(files=Expose('/opt/web-apps/web2py/applications/bdvinv/private/', basename='.', extensions=['txt','sh']), salida=salida, folder=request.folder+'/private')

	#return dict(var = get_command_result(ssh_check_command))
#return locals()
	#command = request.folder + "/private/trae_report.sh ";
#popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True, bufsize=4096)
#output_stdout, output_error = popen.communicate()
#return output_stdout.decode(), output_error.decode()


def lista_bd_onlineXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	import subprocess
	print ("Servidor seleccionado: %s"% (request.args(0)))
	usuario="postgres"
	servidor_id=request.args(0)
	servidor=db.servidores[servidor_id] or redirect(error_page)
	#comando = "ssh -l postgres@"+str(servidor.nombre) + ".pdvsa.com  'psql -l'"
	#comando = "/home/duranfs/monitorbd/lista_bd.sh " + usuario+"@"+servidor.nombre + ".pdvsa.com"
	comando = request.folder + "/private/lista_bd.sh " + usuario+"@"+servidor.nombre + ".pdvsa.com"
	proceso = subprocess.Popen(str(comando), 
		shell=True, 
		stdout = subprocess.PIPE, 
		stderr = subprocess.PIPE,
		stdin = subprocess.PIPE, 
		universal_newlines=True)
	salida = proceso.communicate()
	return salida

def func_lista_bd_online_bdXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	import subprocess
	home=None
	comando=None
	id_servidor=0
	

	
	if request.vars and 'servidor' in request.vars and request.vars.servidor: 
		basedatos_id = request.vars.get('basedatos_id')
		session.basedatos_id = basedatos_id
		servidor_id = request.vars.get('servidor')
		session.servidor_id = servidor_id
		usuario = request.vars.get('usuario')
		clave = request.vars.get('clave')
		tipobd = request.vars.get('tipobd')
		home = request.vars.get('home')
		puerto = request.vars.get('puerto')
		instancia = request.vars.get('instancia')
		servidor=db.servidores[servidor_id] or redirect(error_page)
		ruta_origen = request.folder + 'private'
		
	else:
		# estos datos vienen desde monitor_graf
		basedato=request.args[0]
		servidor=request.args[1]
		
		id_servidor=func_id_servidor(request.args[1])
		#id_servidor=request.args[1]
		
		datos = datos_basedatos(basedato, id_servidor)
		
		if datos:
			basedatos_id = datos.nombre
			session.basedatos_id = basedatos_id
			servidor_id = datos.servidor
			session.servidor_id = servidor_id
			usuario = datos.usuario
			clave = datos.clave
			tipobd = nombre_tipobd(datos.tipobd_id)
			home = datos.home
			puerto = datos.puerto
			instancia = datos.nombre
			servidor=db.servidores[servidor_id] or redirect(error_page)
			ruta_origen = request.folder + 'private'

# https://167.134.178.159:8000/monitorbd/default/func_lista_bd_online_bd/ADMINCALE/METLTQ110	

	if tipobd == "postgres": 
		comando = request.folder + "/private/bd_online_psql.sh '" + \
		clave + "' " + usuario+"@"+servidor.nombre + ".pdvsa.com " + puerto  
	if tipobd == "oracle":
		comando = request.folder + "private/bd_online_oracle.sh '" + \
		clave + "' " + usuario+"@"+servidor.nombre + ".pdvsa.com " + \
		ruta_origen + " " + home + " " + instancia
	if tipobd == "mysql":
		comando = request.folder + "/private/bd_online_mysql.sh '" + \
		clave + "' " + usuario+"@"+servidor.nombre + ".pdvsa.com " + puerto + \
		" " + usuario + " " + home + " " + instancia
	if tipobd == "db2":
		comando = request.folder + "/private/bd_online_db2.sh '" + \
		clave + "' " + usuario+"@"+servidor.nombre + ".pdvsa.com " 
	
	proceso = subprocess.Popen(str(comando), shell=True, stdout = subprocess.PIPE, 	stderr = subprocess.PIPE,	stdin = subprocess.PIPE, universal_newlines=True)
	
	salida = proceso.communicate()	
	session.flash='Listado de Estructura Online Exitoso!'
	#session.flash=id_servidor
	return salida

def func_limpia_filtrobd():
	session.basedatos_id=''
	session.servidor_id=''
	redirect(URL('list_basedatos'))
	return

def func_limpia_filtroMatriz():
	session.basedatos_id=''
	session.matriz_id=''
	redirect(URL('list_matriz_politica_resp'))
	return

def func_limpia_cuentasSO():
	session.basedatos_id=''
	session.servidor_id=''
	redirect(URL('list_cuentas_so'))
	return

def desbloq_usuariosXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	import subprocess
	comando=''
	salida=''
	home=None
	proceso=''
	
	if request.vars and 'servidor' in request.vars and request.vars.servidor: 
			nombre_bd = request.vars.get('instancia')
			servidor_id = request.vars.get('servidor')
			usuario = request.vars.get('usuario')
			clave = request.vars.get('clave')
			tipobd = request.vars.get('tipobd')
			home = request.vars.get('home')
			puerto = request.vars.get('puerto')
			servidor=db.servidores[servidor_id] or redirect(error_page)
			ruta_origen = request.folder + '/private'
	campos = [
	INPUT( _name='indicador' , _type='string'),
	INPUT( _name='cambio' , _type='boolean'),
	INPUT( _name='clave_user' , _type='string') ]
	response.flash = 'Ã‰xito'
	forma = FORM(*campos)
	if forma.accepts(request.vars,formname='formaHTML'):
		#if form.process().accepted:
		#if form.accepts(request, keepvalues=True):
		if tipobd == "postgres": 
			comando = request.folder + "/private/bd_online_psql.sh '" + \
			clave + "' " + usuario+"@"+servidor.nombre + ".pdvsa.com " + puerto  

		if tipobd == "oracle":

			if bool(forma.vars['indicador']) !='': 
				comando = request.folder + "/private/desbloq_usuario_oracle.sh '" + \
				clave + "' " + usuario+"@"+servidor.nombre + ".pdvsa.com " + \
				ruta_origen + " " + home + " " + forma.vars['indicador'] + " " \
				+ forma.vars['clave_user']
			
		if tipobd == "mysql":
			comando = request.folder + "/private/bd_online_mysql.sh '" + \
			clave + "' " + usuario+"@"+servidor.nombre + ".pdvsa.com " + puerto + \
			" " + usuario

		if tipobd == "db2":
			comando = request.folder + "/private/bd_online_db2.sh '" + \
			clave + "' " + usuario+"@"+servidor.nombre + ".pdvsa.com " 

		proceso = subprocess.Popen(str(comando), 
			shell=True, 
			stdout = subprocess.PIPE, 
			stderr = subprocess.PIPE,
			stdin = subprocess.PIPE, 
			universal_newlines=True)
		salida = proceso.communicate()	
	elif forma.errors:
		response.flash = 'Hubo un error al llenar la forma'
	return dict(forma=forma, salida=salida,nombre_bd=nombre_bd)


def ejecuta_dfXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	import subprocess
	home=None
	comando=None
	ruta_origen = request.folder + 'private'
	
	if request.vars and 'servidor' in request.vars and request.vars.servidor: 
		basedatos_id = request.vars.get('basedatos_id')
		session.basedatos_id = basedatos_id
		servidor_id = request.vars.get('servidor')
		session.servidor_id = servidor_id
		usuario = request.vars.get('usuario')
		clave = request.vars.get('clave')
		tipobd = request.vars.get('tipobd')
		home = request.vars.get('home')
		puerto = request.vars.get('puerto')
		instancia = request.vars.get('instancia')
		servidor=db.servidores[servidor_id] or redirect(error_page)
		
		
	else:
		# estos datos vienen desde monitor_graf
		basedato=request.args[0]
		servidor=request.args[1]
		
		id_servidor=func_id_servidor(request.args[1])
		#id_servidor=request.args[1]
		
		datos = datos_basedatos(basedato, id_servidor)
		
		if datos:
			basedatos_id = datos.nombre
			session.basedatos_id = basedatos_id
			servidor_id = datos.servidor
			session.servidor_id = servidor_id
			usuario = datos.usuario
			clave = datos.clave
			tipobd = nombre_tipobd(datos.tipobd_id)
			home = datos.home
			puerto = datos.puerto
			instancia = datos.nombre
			servidor=db.servidores[servidor_id] or redirect(error_page)
			ruta_origen = request.folder + 'private'
		

	
	session.flash='Listado filesystem Exitoso!'
	archivo_salida = open("/tmp/df.txt", "w")
	
	#comando = request.folder + "/private/ejecuta_df_html.sh '" + clave + "' " + usuario+"@"+servidor.nombre + ".pdvsa.com " + puerto 
	comando = request.folder + "private/ejecuta_df_html.sh '" + clave + "' " + usuario+"@"+servidor.nombre + ".pdvsa.com " + 	ruta_origen + " " + home + " " + instancia
	proceso = subprocess.Popen(str(comando), shell=True, stdout = subprocess.PIPE, 	stderr = subprocess.PIPE,	stdin = subprocess.PIPE, universal_newlines=True)

	salida = subprocess.Popen(str(comando), 
		shell=True, 
		stdout = subprocess.PIPE, 
		stderr = subprocess.PIPE,
		stdin = subprocess.PIPE, 
		universal_newlines=True)
	salida = proceso.communicate()
	session.flash='Comando df Exitoso!'
	#session.flash=comando
	return salida

def sysinfoXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	import subprocess
	home=None
	comando=None
	ruta_origen = request.folder + 'private'
	comando = request.folder + "private/sysinfo.sh " 
	proceso = subprocess.Popen(str(comando), shell=True, stdout = subprocess.PIPE, 	stderr = subprocess.PIPE,	stdin = subprocess.PIPE, universal_newlines=True)

	salida = subprocess.Popen(str(comando), 
		shell=True, 
		stdout = subprocess.PIPE, 
		stderr = subprocess.PIPE,
		stdin = subprocess.PIPE, 
		universal_newlines=True)
	salida = proceso.communicate()
	session.flash='Comando sysinfo Exitoso!'
	#session.flash=comando
	return salida	

def ejecuta_procesos_bdXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	import subprocess
	home=None
	comando=None
	ruta_origen = request.folder + 'private'
	
	if request.vars and 'servidor' in request.vars and request.vars.servidor: 
		basedatos_id = request.vars.get('basedatos_id')
		session.basedatos_id = basedatos_id
		servidor_id = request.vars.get('servidor')
		session.servidor_id = servidor_id
		usuario = request.vars.get('usuario')
		clave = request.vars.get('clave')
		tipobd = request.vars.get('tipobd')
		home = request.vars.get('home')
		puerto = request.vars.get('puerto')
		instancia = request.vars.get('instancia')
		servidor=db.servidores[servidor_id] or redirect(error_page)
		
		
	else:
		# estos datos vienen desde monitor_graf
		basedato=request.args[0]
		servidor=request.args[1]
		
		id_servidor=func_id_servidor(request.args[1])
		#id_servidor=request.args[1]
		
		datos = datos_basedatos(basedato, id_servidor)
		
		if datos:
			basedatos_id = datos.nombre
			session.basedatos_id = basedatos_id
			servidor_id = datos.servidor
			session.servidor_id = servidor_id
			usuario = datos.usuario
			clave = datos.clave
			tipobd = nombre_tipobd(datos.tipobd_id)
			home = datos.home
			puerto = datos.puerto
			instancia = datos.nombre
			servidor=db.servidores[servidor_id] or redirect(error_page)
			ruta_origen = request.folder + 'private'
		

	
	session.flash='Listado de procesos Exitoso!'
	archivo_salida = open("/tmp/df.txt", "w")
	
	#comando = request.folder + "/private/ejecuta_df_html.sh '" + clave + "' " + usuario+"@"+servidor.nombre + ".pdvsa.com " + puerto 
	comando = request.folder + "private/ejecuta_procesos_bd_html.sh '" + clave + "' " + usuario+"@"+servidor.nombre + ".pdvsa.com " + 	ruta_origen + " " + home + " " + instancia.upper() + " " + usuario + " " + tipobd.upper()
	proceso = subprocess.Popen(str(comando), shell=True, stdout = subprocess.PIPE, 	stderr = subprocess.PIPE,	stdin = subprocess.PIPE, universal_newlines=True)

	salida = subprocess.Popen(str(comando), 
		shell=True, 
		stdout = subprocess.PIPE, 
		stderr = subprocess.PIPE,
		stdin = subprocess.PIPE, 
		universal_newlines=True)
	salida = proceso.communicate()
	session.flash='Comando ps Exitoso!'
	#session.flash=comando
	return salida



def abre_terminalXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	sh("ls -a")
	return dict(result=result, salida=salida)

def shXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX(cmd, input=""):
	import subprocess
	rst = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, input=input.encode("utf-8")) 
	assert rst.returncode == 0, rst.stderr.decode("utf-8")
	return rst.stdout.decode("utf-8")
	
def ejecuta_shellXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	import subprocess
	archivo_salida = open("/tmp/output.txt", "w")
	comando = request.folder + "/private/lista.sh" #son muchos asÃ­ que por eso los asigno a una variable
	#comando = "ssh postgres@metltq111.pd.com '/var/lib/postgresql/monitorbd/cron_monitorbd.sh'"
	#servidor_id=request.args(0)
	#servidor=db.servidores[servidor_id] or redirect(error_page)
	proceso = subprocess.Popen(str(comando), 
		shell=True, 
		stdout = subprocess.PIPE, 
		stderr = subprocess.PIPE,
		stdin = subprocess.PIPE, 
		universal_newlines=True)
	salida = proceso.communicate()
	print >> archivo_salida, salida
		#sal = run_comando('ls -l /home')
	return locals()

def run_comandoXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX(self, *args):
	import subprocess
	p = subprocess.Popen(str(args),	
		shell=False, 
		stdout = subprocess.PIPE, 
		stderr = subprocess.PIPE, 
		stdin = subprocess.PIPE, 
		universal_newlines=True)
	return p.communicate()

def lee_archivoXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX():
	import os
	os.system('ls -l > tmp')
	print (open('tmp', 'r').read())
	return locals()


def select_servidor():
	servidores=db(db.servidores.id>0).select(orderby=db.servidores.nombre)
	return dict(servidores=servidores)

#--------- servidores tipobd ------------------------------------------------------
   
def serv_bd():
	servidores=db(db.servidores.id>0).select(orderby=db.servidores.nombre)
	groups=db(db.tipobd.id>0).select(orderby=db.tipobd.descri)
	tiposbd = db(db.tipobd.id>0).select()
	return dict(servidores=servidores, groups=groups, tiposbd=tiposbd)


def select_basedatos_tipobd():
	tipobd_id=request.post_vars.tipobd
	basedatos=db(db.basedatos.tipobd_id==tipobd_id)\
	(db.basedatos.servidor==db.servidores.id)\
	(db.basedatos.clave != '')\
		.select(db.servidores.nombre, db.basedatos.usuario, \
	db.basedatos.clave, distinct = True,  orderby=db.servidores.nombre)
	return dict(basedatos=basedatos)

def lista_bd():
	tipobd_id=request.post_vars.tipobd

	print (os.system('pwd'))
	print ("Plataforma seleccionado: %s"% (tipobd_id))
	return dict(tipobd_id=tipobd_id)


#---------------------------------------------------------------------------------


	


@auth.requires_login()
@auth.requires_membership('DBA')
def list_claves():
	claves = db(db.t_claves.f_servidor>0 ).select(orderby=db.t_claves.f_servidor)
	#claves = db(db.t_claves.f_servidor>0 ).select(limitby=(0,10),orderby=db.t_claves.f_servidor)
	#form = crud.create(db.t_claves)
	form = crud.create(db.t_claves)
	return dict(form=form, claves=claves)

	
@auth.requires_login()
def consulta_claves():
	claves = db(db.t_claves.f_servidor>0 ).select(orderby=db.t_claves.f_servidor)
	#claves = db(db.t_claves.f_servidor>0 ).select(limitby=(0,10),orderby=db.t_claves.f_servidor)
	#form = crud.create(db.t_claves)
	form = SQLFORM(db.t_claves)
	return dict(form=form, claves=claves)





@auth.requires_login()
def edit_claves():
	clave_id=request.args(0)
	clave=db.t_claves[clave_id]  or redirect(error_page)
	#session.servidores_recientes = add2(session.servidores_recientes,servidor)
	if not clave.created_by==me: 
		crud.settings.update_deletable = False
	form=crud.update(db.t_claves,clave,next=url('claves_manage'))
	return dict(form=form)

@auth.requires_login()
def busqueda_avanzada_bd():
	form=FORM(INPUT(_name='keywords',requires=IS_NOT_EMPTY()),_method='GET')
	if form.accepts(request):
		keywords = form.vars.keywords.split()
		query1 = reduce(lambda a,b:a|b,[db.t_claves.f_servidor.like('%'+key+'%') for key in keywords])
		query2 = reduce(lambda a,b:a|b,[db.t_claves.f_tipobd.like('%'+key+'%') for key in keywords])
		query3 = reduce(lambda a,b:a|b,[db.t_claves.f_instancia.like('%'+key+'%') for key in keywords])
		books = db(query1|query2|query3).select()
	else:
		books=None
	if books and len(books)==1:
		redirect(URL('book',args=books.first().id))
	return dict(form=form,books=books)


@auth.requires_login()
def monitor2():
	form = SQLFORM.smartgrid(db.bdmon)
	#form=crud.create(db.basedatos_mon)
	mon= db(db.bdmon.f_corrida>=request.now.date()).select()
	#monitores= db(db.basedatos_mon.id>0).select()
	return dict(mon=mon,form=form)



@auth.requires_login()
def servidores_monitoreados():
	#servidores -----------------------------------------------------------------------------------------
	outx = []
	for servidor in db(db.servidores.status_mon.upper()=='SI').select(db.servidores.nombre,db.servidores.id):
		mon=db(db.bdmon.tx_servidor.lower()==servidor.nombre.lower())(db.bdmon.f_corrida>=request.now.date()).select(db.bdmon.ALL).first()
		if mon:
			outx.append( (servidor.nombre,  'SI', '', servidor.id) )
		else:   
			outx.append( (servidor.nombre,  'ERROR', 'Verifique conexion al servidor, crontab o procesos de monitoreo', servidor.id) )
	
	#servidores_mon=db(db.bdmon.id>0).select(db.bdmon.tx_servidor,db.bdmon.tx_tipobd, distinct=True) 
	servidores_mon=db(db.bdmon.id>0).select(db.bdmon.tx_servidor,db.bdmon.tx_tipobd, distinct=db.bdmon.tx_servidor) 
	servidores_st_mon=db(db.servidores.status_mon.upper()=='SI').select(db.servidores.nombre, distinct=True) 
		#servidores=db(db.bdmon.id>0)._select(db.bdmon.tx_servidor.count(distinct=True), db.bdmon.tx_tipobd, groupby=db.bdmon.tx_tipobd)
		# SELECT count(DISTINCT id_impressora), tests.data FROM tests WHERE (tests.id >0) GROUP BY tests.data
		#mon=db.executesql("SELECT distinct nombre,tx_servidor,case when tx_servidor is null then 'X' end FROM  public.bdmon full outer join servidores on bdmon.tx_servidor = servidores.nombre  where status_mon='SI' ;")
	#servidores=db.executesql('select distinct tx_servidor from bdmon;')	
	#return dict(mon=mon)
	#x=A(db().select(db.bdmon.tx_servidor,db.servidores.nombre,\
	#    left=db.servidores.on(db.bdmon.tx_servidor==db.servidores.nombre and db.servidores.status_mon=='SI')) )
	#return dict(servidores_mon=servidores_mon,servidores_st_mon=servidores_st_mon,mon=mon)
	#x = A(db((db.servidores.status_mon == 'SI') & (db.servidores.nombre == db.bdmon.tx_servidor)).select(db.servidores.ALL))

	#bases de datos ----------------------------------------------------------------------------------
		   
	
	return dict(servidores_mon=servidores_mon,servidores_st_mon=servidores_st_mon,yy=outx)


@auth.requires_login()
def basedatos_monitoreadas():
	#Â·basedatos  -----------------------------------------------------------------------------------------
	outdb = []
	for bd1 in db(db.basedatos.status_mon.upper()=='SI').select(db.basedatos.nombre,db.basedatos.servidor, db.basedatos.tipobd_id, distinct=True):
		bd_mon=db(db.bdmon.tx_instancia.lower()==bd1.nombre.lower())\
		(db.bdmon.tx_servidor.lower()==bd1.servidor.nombre.lower())\
		(db.bdmon.f_corrida>=request.now.date()).select(db.bdmon.ALL).first()
		#bd_mon=db(db.bdmon.tx_instancia==bd1.nombre).select(db.bdmon.ALL).first()
		if bd_mon:
			outdb.append( (bd1.nombre,  'SI', '', bd1.servidor, bd1.tipobd_id) )
		else:   
			outdb.append( (bd1.nombre,  'ERROR', 'Verifique conexion al servidor, crontab o procesos de monitoreo',bd1.servidor, bd1.tipobd_id) )
	
	basedatos_mon=db(db.bdmon.id>0).select(db.bdmon.tx_servidor,db.bdmon.tx_instancia,db.bdmon.tx_tipobd, distinct=True) 
	basedatos_st_mon=db(db.basedatos.status_mon.upper()=='SI').select(db.basedatos.nombre, distinct=True) 
	 
	
	return dict(basedatos_mon=basedatos_mon,basedatos_st_mon=basedatos_st_mon,bd=outdb)


@auth.requires_login()
def list_servidores():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_servidores').dataTable({"sPaginationType": "full_numbers"});
	});''')


	#,"oLanguage": {"sSearch": "Search all columns:"}, "bSortCellsTop": true,"bJQueryUI": true,
	servidor_id=request.args(0)
	session.servidor_aux=request.args(0)
	servidor=db.servidores[servidor_id]
	
	if servidor:
		servidores=db(db.servidores.id == servidor_id).select()	
	else:
		servidores=db(db.servidores).select(orderby="servidores.tipo_equipo, servidores.nombre")
			
	
	form=crud.create(db.servidores)
	
	return dict(servidores=servidores,form=form, script=script)



@auth.requires_login()
def list_servidores_MD():
	
	serv_id= request.args(0)
	ser=request.post_vars.servidor or request.vars.get("servidor")
	session.flash=request.args[:2]
	#session.flash=serv_id
	#serv=db.servidores[serv_id]  or redirect(error_page)
	
	#links = [lambda row: A('View Post',_href=URL("default","view",args=[row.id]))]
	links = [lambda row: A('BD',_href=URL(r=request,c='default',f='list_basedatos',args=[row.id]))]

	#links = URL(r=request,c='default',f='list_basedatos',args=[servidor.id])

	#FIELDS=(db.servidores.tipo_equipo,db.servidores.id,db.servidores.nombre,\
	#db.servidores.dominio,db.servidores.ip,db.servidores.rac, db.servidores.ambiente_id, db.servidores.so_id)
	
	#export_classes = dict(csv=True, json=False, html=False,
	#		tsv=False, xml=False, csv_with_hidden_cols=False,
		#                tsv_with_hidden_cols=False)	
	export_classes = dict(csv=(CSVExporter, 'CSV'), json=False, html=False,
					  tsv=False, xml=False, csv_with_hidden_cols=False,
					  tsv_with_hidden_cols=False)

	query=(db.servidores.id > 0)
	#form = SQLFORM.grid(db.servidores,left=db.basedatos.on(db.basedatos.servidor=db.servidores.id),
	form = SQLFORM.smartgrid(db.servidores,  
	linked_tables=['basedatos'],
	
	create = auth.has_membership('DBA'),
	editable = auth.has_membership('DBA'),
	deletable = auth.has_membership('DBA'),
	csv = auth.has_membership('DBA'),
	exportclasses=export_classes,showbuttontext=False,
	#links_in_grid=False, 
	#links=links,
	maxtextlength=20,
	paginate=10

	)
	#my_extra_element = TR(LABEL('Click to submit'),                      
	#	INPUT(_name='submit',value="Submit",_type='submit'))
	#form[0].insert(-1,my_extra_element)
	return locals()

#from cStringIO import StringIO
class CSVExporter(object):
	"""This class is used when grid's table contains foreign key () id of other table)
	   Exported CSV should contain reference key name not id"""
	file_ext = "csv"
	content_type = "text/csv"

	def __init__(self, rows):
		self.rows = rows

	def export(self):
		if self.rows:
			s = StringIO()
			self.rows.export_to_csv_file(s, represent=True)
			return s.getvalue()
		else:
			return ''


@auth.requires_login()
def list_servidoresx():
	form=crud.create(db.servidores)
	servidores=db(db.servidores).select(cache=(cache.ram,60))
	return dict(servidores=servidores,form=form)

@auth.requires_login()
def list_servidores2():
	form=crud.create(db.servidores)
	servidores=db(db.servidores).select(orderby=db.servidores.nombre)
	return dict(servidores=servidores,form=form)


@auth.requires_login()
def edit_servidor():                                
	servidor_id=request.args(0,cast=int)
	#servidor_id=request.args(0)
	db.servidores.id.writable=False
	db.servidores.id.readable=False
	db.servidores.nombre.writable=False
	#db.servidores.nombre.readable=False
	servidor=db.servidores[servidor_id]  or redirect(error_page)
	session.servidores_recientes = add2(session.servidores_recientes,servidor)

	# Guardar la validación original del campo nombre
	original_requires = db.servidores.nombre.requires

	form=crud.update(db.servidores,servidor,next=url('list_servidores'))
	
	return dict(form=form)


@auth.requires_login()
def list_guardias():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_guardias').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	#SafeLocale()
	form=crud.create(db.guardias)
	guardias_reg=db(db.guardias.id>0).select(orderby="guardias.f_fch_inicio")
	return dict(guardias_reg=guardias_reg,form=form, script=script)

@auth.requires_login()
def view_guardias():
	guardia_id=request.args(0)
	reg_guardias=db.guardias[guardia_id] or redirect(error_page)
	  
	return dict(reg_guardias=reg_guardias)

@auth.requires_login()
def edit_guardias():
	#now = datetime.datetime.now()
	#span = datetime.timedelta(days=7)
	guardia_id=request.args(0)
	guardias_reg=db.guardias[guardia_id] or redirect(error_page)
	#guardias.f_fch_fin=now+span
	#session.flash='done!'+str(guardias_reg)
	form=crud.update(db.guardias,guardias_reg.id,next=url('list_guardias'))
	return dict(form=form)

@auth.requires_login()
def reporte_guardias():

	actividades=''
	desde=''
	hasta=''
	ac = db.actividades
	actividades = [OPTION(actividad.id  ,_value=actividad.id) for actividad in
	db(ac.id>0).select(ac.ALL)]
	
	camposFechas = [
		###########################################
		# Fechas
		INPUT(_name='desde', _type='date'),
		INPUT(_name='hasta', _type='date'),
	]

	formaFE = FORM(*camposFechas)
	if formaFE.accepts(request.vars, formname='formaHTMLFE',  onvalidation=valida_fechas2, keepvalues=True):
		desde = request.vars.desde
		hasta = request.vars.hasta
	guardias_reg=db(db.guardias.id>0)(db.guardias.f_fch_inicio>=desde)\
	(db.guardias.f_fch_fin<=hasta)\
	.select(orderby=db.guardias.f_fch_inicio)
	return dict(guardias=guardias_reg)



@auth.requires_login()
def list_tasks_guardias():
	guardia_id=request.args(0)
	guardias=db.guardias[guardia_id] or redirect(error_page)
	db.task_guardias.guardia_id.default=guardias.id
	db.task_guardias.guardia_id.writable=db.task_guardias.guardia_id.readable=False
	
	form=crud.create(db.task_guardias,next='view_task_guardias/[id]')

	tareas=db(db.task_guardias.guardia_id==guardias.id).select(orderby=~db.task_guardias.created_on)
	return dict(guardias=guardias,tareas=tareas,form=form)


@auth.requires_login()
def view_task_guardias():
	task_guardia_id=request.args(0)
	task_guardias=db.task_guardias[task_guardia_id] or redirect(error_page)
	return dict(task_guardias=task_guardias)

@auth.requires_login()
def edit_task_guardias():
	task_guardia_id=request.args(0)
	task_guardias=db.task_guardias[task_guardia_id] or redirect(error_page)
	if not task_guardias.created_by==me: 
		crud.settings.update_deletable = False
	db.task_guardias.guardia_id.writable=db.task_guardias.guardia_id.readable=False
	form=crud.update(db.task_guardias,task_guardias,next=url('view_task_guardias',task_guardia_id))
	return dict(form=form)



@auth.requires_login()
@auth.requires_membership('ADMIN')
def list_rutina_status():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_rutina_status').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	form=crud.create(db.rutina_status)
	if form.accepts(request.vars, session):
		guarda_log_bdmon()

	rutina_status=db(db.rutina_status.id>0).select(orderby=db.rutina_status.rutina)
	return dict(rutina_status=rutina_status,form=form, script=script)

def list_rutinas():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_rutinas').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	form=crud.create(db.rutinas)
	rutinas=db(db.rutinas.id>0).select(orderby=db.rutinas.nombre)
	return dict(rutinas=rutinas,form=form, script=script)

@auth.requires_membership('ADMIN','SYSTEM')
def edit_rutinas():
	rutina_id=request.args(0)
	rutina=db.rutinas[rutina_id]  or redirect(error_page)
	
	if not rutina.created_by==me: 
		crud.settings.update_deletable = False
	form=crud.update(db.rutinas,rutina,next=url('list_rutinas'))
	return dict(form=form)

@auth.requires_login()
def view_rutinas():
	rutina_id=request.args(0)
	rutina=db.rutinas[rutina_id] or redirect(error_page)
	return dict(rutina=rutina)


@auth.requires_login()
def list_tipoequipo():
	form=SQLFORM.smartgrid(db.tipo_equipos, 
	details=True, 	create=True,	editable=True,	deletable=False,
	searchable=False,	csv = False,	links_in_grid=True)
	db.tipobd.id.readable = False
	return dict(form=form)

@auth.requires_login()
def list_tipobd():
	form=SQLFORM.smartgrid(db.tipobd, 
	details=True, 	create=True,	editable=True,	deletable=False,
	searchable=False,	csv = False,	links_in_grid=True)
	db.tipobd.id.readable = False
	return dict(form=form)

@auth.requires_login()
def list_ubicacion():
	form=SQLFORM.smartgrid(db.ubicacion, details=False, csv=False, 
	create=True,editable=True,deletable=False,searchable=False,)
	db.ubicacion.id.readable = False
	return dict(form=form)

@auth.requires_login()
@auth.requires_membership('ADMIN') 
def list_proyectos():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_servidores').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	form=SQLFORM.grid(db.proyectos, details=False, csv=False, 
	create=False,editable=False,deletable=False,searchable=True, maxtextlength = 200)
	db.proyectos.id.readable = False
	return dict(form=form, script=script)

@auth.requires_login()
@auth.requires_membership('ADMIN') 
def crear_proyectos():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_servidores').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	db.proyectos.status.default='POR REALIZAR'
	db.proyectos.status.writable=False
	db.proyectos.status.readable=False
	#db.proyectos.gerencia.writable=False
	#db.proyectos.gerencia.readable=False
	if auth.has_membership("ALM"):
		gerencia="ALM"
	elif auth.has_membership("DBA"):
		gerencia="DBA"
	elif auth.has_membership("CORE"):
		gerencia="CORE"
	else:
		gerencia="OTRO"	
	#db.proyectos.gerencia.default=gerencia
	
	form=SQLFORM.grid(db.proyectos, details=False, csv=False, 
	create=True,editable=False,deletable=False,searchable=False, maxtextlength = 200)
	db.proyectos.id.readable = False
	return dict(form=form, script=script)

@auth.requires_login()
@auth.requires_membership('ADMIN') 
def editar_proyectos():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_servidores').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	
	if auth.has_membership("ALM"):
		form=SQLFORM.grid(db.proyectos.gerencia=='ALM', details=False, csv=False, 
		create=False,	editable=True,	deletable=False,	searchable=True, 	maxtextlength = 200)
	elif auth.has_membership("DBA"):
		form=SQLFORM.grid(db.proyectos.gerencia=='DBA', details=False, csv=False, 
		create=False,	editable=True,	deletable=False,	searchable=True, 	maxtextlength = 200)	
	elif auth.has_membership("CORE"):
		form=SQLFORM.grid(db.proyectos.gerencia=='CORE', details=False, csv=False, 
		create=False,	editable=True,	deletable=False,	searchable=True, 	maxtextlength = 200)
	else:
		form=SQLFORM.grid(db.proyectos.id>0, details=False, csv=False, 
		create=False,	editable=True,	deletable=False,	searchable=True, 	maxtextlength = 200)	
	db.proyectos.id.readable = False
	return dict(form=form, script=script)

def valida_fechas(form):
	if form.vars.fecha_asig > form.vars.fecha_vcto:
		form.errors.start = 'Vencimiento debe ser mayor que Asignacion'


@auth.requires_login()
@auth.requires_membership('ADMIN')
def asignacion():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#asignacion').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	camposAsignacion = [
		###########################################
		# Asignacion
		SELECT(_name='cod_proyecto',requires=IS_IN_DB(db,db.proyectos.id,'%(descri)s')),
		SELECT(_name='analista',requires=IS_IN_DB(db,db.auth_user.id,'%(first_name)s')),
		INPUT(_name='fecha_asig', _type='date'),
		INPUT(_name='fecha_vcto', _type='date'),
		SELECT(_name='prioridad', _type='string'),
		SELECT(_name='status', _type='string'),
		SELECT(_name='porc_completado', _type='integer'),
			
	]

	formaOP = FORM(*camposAsignacion)
	if formaOP.accepts(request.vars,formname='formaOPHTML',  onvalidation=valida_fechas, keepvalues=True):
		datosOP = db.asignacion._filter_fields(formaOP.vars)
		proy=formaOP.vars.cod_proyecto
		#datosOP['fecha_asignacion'] = request.now
		#datosOP['fecha_vcto'] = request.now
		OPinsertado = db.asignacion.insert(**datosOP)
		
		st=db(db.proyectos.id==proy).select(db.proyectos.status).first()
		
		if st.status == 'POR REALIZAR':
			db(db.proyectos.id == proy).update(status = 'ASIGNADO')
			db.commit()
			response.flash = 'Primera asignacion al proyecto se realizó con Éxito' 
		else :
			analista=db.auth_user[formaOP.vars.analista]
			response.flash = 'Se asignó ' + str(analista.first_name.upper()) + ' al proyecto ..' 
		
	elif formaOP.errors:
		import copy
		myerrors=copy.copy(formaOP.errors)
		response.flash = myerrors
		#session.flash="Error al llenar la forma"
	else:
		
		pass	
	
	if auth.has_membership("ALM") and auth.has_membership("ADMIN"):
		listaProyectos = db(db.proyectos.id>0)(db.proyectos.status != 'COMPLETADO' )\
		(db.proyectos.gerencia=='ALM').select(orderby="proyectos.status, proyectos.descri")
		
		listaAnalista = db(db.auth_user.id>0)(db.auth_group.id == db.auth_membership.group_id)\
		(db.auth_user.id == db.auth_membership.user_id)(db.auth_group.role == 'ALM').select(orderby="auth_user.first_name")
		
	elif auth.has_membership("DBA") and auth.has_membership("ADMIN"):
		listaProyectos = db(db.proyectos.id>0)(db.proyectos.status != 'COMPLETADO' )\
		(db.proyectos.gerencia=='DBA').select(orderby="proyectos.status, proyectos.descri")
		
		listaAnalista = db(db.auth_user.id>0)(db.auth_group.id == db.auth_membership.group_id)\
		(db.auth_user.id == db.auth_membership.user_id)(db.auth_group.role == 'DBA').select(orderby="auth_user.first_name")
		
	elif auth.has_membership("CORE") and auth.has_membership("ADMIN"):
		listaProyectos = db(db.proyectos.id>0)(db.proyectos.status != 'COMPLETADO' )\
		(db.proyectos.gerencia=='CORE').select(orderby="proyectos.status, proyectos.descri")
		
		listaAnalista = db(db.auth_user.id>0)(db.auth_group.id == db.auth_membership.group_id)\
		(db.auth_user.id == db.auth_membership.user_id)(db.auth_group.role == 'CORE').select(orderby="auth_user.first_name")
		
	else:
		LISTA=['ALM','DBA','CORE']
		listaProyectos = db(db.proyectos.id>0)(db.proyectos.status != 'COMPLETADO' ).select(orderby="proyectos.status, proyectos.descri")
		listaAnalista = db(db.auth_user.id>0)(db.auth_group.id == db.auth_membership.group_id)\
		(db.auth_user.id == db.auth_membership.user_id)(db.auth_group.role.belongs(LISTA)).select(orderby="auth_user.first_name")
		
	#listaAnalista = db(db.auth_user.id>0).select(orderby="auth_user.first_name")
	asignaciones = db(db.asignacion.id>0).select(orderby="asignacion.analista")
	return dict(listaProyectos = listaProyectos, listaAnalista=listaAnalista, asignaciones=asignaciones, script=script, form=formaOP)



def valida_asignacion():
	proyectoID = request.vars.cod_proyecto
	analistaID = request.vars.analista
	proy=db(db.asignacion.cod_proyecto == proyectoID)(db.asignacion.analista == analistaID).select().first()
	#session.flash = proy
	if proy:
		return 'yes'
	else:
		return 'no'
	return locals()


def list_asignacion():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#asignacion').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	
	if auth.has_membership("ALM") and auth.has_membership("ADMIN"):
		
		session.flash='Gerencia Alamcenamiento'
		listaProyectos = db(db.proyectos.id>0)(db.proyectos.status != 'COMPLETADO' )\
		(db.proyectos.gerencia=='ALM').select(orderby="proyectos.status, proyectos.descri")
		
		asignaciones = db(db.asignacion.id>0)(db.asignacion.cod_proyecto==db.proyectos.id)(db.proyectos.gerencia=='ALM').select(orderby="asignacion.analista")
		
	elif auth.has_membership("DBA") and auth.has_membership("ADMIN"):
		
		session.flash='dba'
		listaProyectos = db(db.proyectos.id>0)(db.proyectos.status != 'COMPLETADO' )\
		(db.proyectos.gerencia=='DBA').select(orderby="proyectos.status, proyectos.descri")
		
		asignaciones = db(db.asignacion.id>0)(db.asignacion.cod_proyecto==db.proyectos.id)(db.proyectos.gerencia=='DBA').select(orderby="asignacion.analista")
		
	elif auth.has_membership("CORE") and auth.has_membership("ADMIN"):
		
		session.flash='Gerencia CORE'
		listaProyectos = db(db.proyectos.id>0)(db.proyectos.status != 'COMPLETADO' )\
		(db.proyectos.gerencia=='CORE').select(orderby="proyectos.status, proyectos.descri")
		
		asignaciones = db(db.asignacion.id>0)(db.asignacion.cod_proyecto==db.proyectos.id)(db.proyectos.gerencia=='CORE').select(orderby="asignacion.analista")
		
	else:
		listaProyectos = db(db.proyectos.id>0)(db.proyectos.status != 'COMPLETADO' )\
		.select(orderby="proyectos.status, proyectos.descri")
		asignaciones = db(db.asignacion.id>0).select(orderby="asignacion.analista")
		asignaciones = db(db.asignacion.id>0)(db.asignacion.cod_proyecto==db.proyectos.id).select(orderby="asignacion.analista")
		
	
	return dict(listaProyectos = listaProyectos, asignaciones=asignaciones, script=script)


@auth.requires_login()
def edit_asignacion():
	tb = db.asignacion
	ac = db.actividades
	
	asig_id = tb(request.vars.get('asignacion')) or redirect(URL('list_asingcacion'))
	
	rec = db(ac.cod_asig == asig_id).select().first() #verifico si hay actividades antes de borrar
	
	if rec: 
		crud.settings.update_deletable = False
		db.asignacion.cod_proyecto.writable=False
		db.asignacion.analista.writable=False
		
	form = crud.update(tb,asig_id,next=url('list_asignacion'))
	if form.accepts(request.vars, session):
		response.flash = 'Actualizado con exito'
	elif form.errors:
		response.flash = 'Error al actualizar'
	else:
		pass
	return locals()
#----------------------

def valida_fechas2(formaOP):
	if formaOP.vars.desde > formaOP.vars.hasta:
		formaOP.errors.desde = 'Fechas erradas'
		formaOP.errors.hasta = 'Fechas erradas'
		
@auth.requires_login()
def list_actividades():
	me = auth.user_id
	actividades=''
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_actividades').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	#SafeLocale()
	
	ac = db.actividades
	actividades = [OPTION(actividad.id  ,_value=actividad.id) for actividad in
	db(ac.id>0).select(ac.ALL)]
	
	camposActividades = [
		###########################################
		# Asignacion
		INPUT(_name='desde', _type='date'),
		INPUT(_name='hasta', _type='date'),
	]

	formaOP = FORM(*camposActividades)
	if formaOP.accepts(request.vars,formname='formaOPHTML',  onvalidation=valida_fechas2, keepvalues=True):
		desde = request.vars.desde
		hasta = request.vars.hasta
		
		
		desde = request.vars.desde
		hasta = request.vars.hasta
		
		
		from datetime import datetime
		import os
		import xlwt
		import uuid
		from xlwt import Workbook #xlwt.Utils 
		#import rowcol_to_cell
		#from xlwt import *
	
		tmpfilename=os.path.join(request.folder,'private','example.xls')
	
		font0 = xlwt.Font()
		font0.name = 'Times New Roman'
		font0.colour_index = 2
		font0.bold = True
		
		sty = xlwt.XFStyle()
		al = xlwt.Alignment()
		al.wrap = xlwt.Alignment.WRAP_AT_RIGHT
		sty.alignment = al
	
		style0 = xlwt.XFStyle()
		style0.font = font0

		style1 = xlwt.XFStyle()
		style1.num_format_str = 'DD-MM-YYYY'
	
		fnt = Font()
		fnt.name = 'Arial'
		fnt.colour_index = 4
		fnt.bold = True
		
		border = xlwt.Borders()  # Frame cells
		border.left = xlwt.Borders.THIN  # Left
		border.top = xlwt.Borders.THIN  # upper
		border.right = xlwt.Borders.THIN  # right
		border.bottom = xlwt.Borders.THIN  # lower
		border.left_colour = 0x40  # Border line color
		border.right_colour = 0x40
		border.top_colour = 0x40
		border.bottom_colour = 0x40
		
	
		pattern = xlwt.Pattern()
		pattern.pattern = xlwt.Pattern.SOLID_PATTERN
		pattern.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']
	
		encab = xlwt.easyxf('font: bold on; align: wrap on, vert center, horiz center')
		encab.borders = border
		encab.pattern = pattern
	
		style = XFStyle()
		style.font = fnt
		style.font.height = 180
		style.num_format_str = '#,##0'
		style.borders = border
	
		style2 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
		num_format_str='#,##0.00')
	
		texto = XFStyle()
		texto = xlwt.easyxf('align: wrap on, vert center, horiz left')
		texto.alignment.wrap = 1
		texto.borders = border
		
		textoC = XFStyle()
		textoC = xlwt.easyxf('align: wrap on, vert center, horiz center')
		textoC.alignment.wrap = 1
		textoC.borders = border
		
		fecha = xlwt.easyxf('align: wrap on, vert center, horiz center')
		fecha.num_format_str = 'DD-MM-YYYY'
		fecha.borders = border
		
		hora = xlwt.easyxf('align: wrap on, vert center, horiz center',num_format_str='#,##0.00')
		hora.borders = border
	
		wb = xlwt.Workbook(encoding="utf-8",style_compression=0)
		ws = wb.add_sheet('Actividades')
		En = wb.add_sheet('En Curso')
		Por = wb.add_sheet('Por Realizar')

		ws.normal_magn=110

		data = []
		act = ws.col(0)
		fec = ws.col(1)
		hor = ws.col(2)
		hor2 = ws.col(3)
		tipo = ws.col(4)
		ana = ws.col(5)
		# sec_col = worksheet.col(0)
		act.width = 1200*20
		fec.width = 150*20
		hor.width = 125*20
		hor2.width = 125*20
		tipo.width = 80*20
		ana.width = 300*20
		head = ['Actividades', 'Fecha', 'Hora de ejecución', 'Horas laboradas', 'Tipo', 'Analista']
		for index, value in enumerate(head):
			ws.write(0, index, value, encab)
		
		
		
		
		
		
		rows = db(db.actividades.cod_asig==db.asignacion.id)\
		(db.actividades.fecha_inicio >= desde)(db.actividades.fecha_inicio <= hasta)\
		(db.auth_user.id==db.asignacion.analista)(db.auth_user.id==me).\
		select(db.actividades.descripcion,db.actividades.fecha_inicio,db.actividades.hora_inicio,\
		db.actividades.horas_laboradas,db.actividades.tipo,(db.auth_user.first_name+' '+db.auth_user.last_name).with_alias("analista"), \
		orderby="actividades.fecha_inicio, actividades.hora_inicio, analista")

		row = 1
		col = 0
		
		for index, r in enumerate(rows):
			ws.row(index).height_mismatch = True
			ws.row(index).height = 50*20 #len(r.actividades.descripcion)*10 #50*20
			ws.set_panes_frozen(True) # frozen headings instead of split panes
			ws.set_horz_split_pos(1) # in general, freeze after last heading row
			ws.set_remove_splits(True)
			ws.write (row, 0, r.actividades.descripcion.replace('"',''), texto)
			ws.write (row, 1, r.actividades.fecha_inicio, fecha)
			ws.write (row, 2, r.actividades.hora_inicio, fecha)
			ws.write (row, 3, r.actividades.horas_laboradas, hora)
			ws.write (row, 4, r.actividades.tipo, textoC)
			ws.write (row, 5, r.analista, textoC)
			
			row +=1
			
		row +=2
		#ws.write(row, 2, 'Total Horas')
		#ws.write(row, 3, Formula("SUM($D$1:$D$100)"))
		#ws.write(row, 5, xlwt.Formula('= D{} - E[]'.format(row,  row)))
		
		
		
		#
		
		# actividades en curso --------------------------------------
		act = En.col(0)
		ana = En.col(1)
		st = En.col(2)
		# sec_col = worksheet.col(0)
		act.width = 1200*20
		ana.width = 300*20
		st.width = 300*20
		
		head = ['Actividades en curso', 'Analista', 'Estatus']
		for index, value in enumerate(head):
			En.write(0, index, value, encab)
		
		rows=db(db.proyectos.descri!='ACTIVIDADES SEMANAL')(db.proyectos.id == db.asignacion.cod_proyecto)\
		(db.auth_user.id==me)(db.auth_user.id==db.asignacion.analista).select(db.proyectos.id, db.proyectos.descri,\
		db.proyectos.status,(db.auth_user.first_name+' '+db.auth_user.last_name).with_alias("analista"), \
		orderby="proyectos.descri,analista")
		row = 1
		id_proy=0
		grupo_analista=''
		analista_anterior=''
		for index, r in enumerate(rows):
			En.row(index).height_mismatch = True
			En.row(index).height = 50*20
		
			En.set_panes_frozen(True) # frozen headings instead of split panes
			En.set_horz_split_pos(1) # in general, freeze after last heading row
			En.set_remove_splits(True)
			
			if id_proy == r.proyectos.id:
				reg =db(db.proyectos.id == db.asignacion.cod_proyecto)\
				(db.auth_user.id==db.asignacion.analista)(db.proyectos.id == id_proy)\
				.select((db.auth_user.first_name+' '+db.auth_user.last_name).with_alias("analista"), orderby="proyectos.descri,analista")
				#grupo_analista='[ '
				for grupo in reg:
					grupo_analista += grupo.analista + ','
			
				#grupo_analista += ' ]'	
				En.write (row - 1, 1, grupo_analista , textoC)
				grupo_analista=''
			else:	
				En.write (row, 0, r.proyectos.descri, texto)
				En.write (row, 1, r.analista, textoC)
				En.write (row, 2, r.proyectos.status, textoC)
				analista_anterior=r.analista
				row +=1
	
			id_proy = r.proyectos.id
		
		#En.write(row+1, 2, analistas)
		#En.write(row+1, 3, xlwt.Formula(sum(A1:A16)))
			
		# actividades por realizar
		act = Por.col(0)
		st = Por.col(1)
		# sec_col = worksheet.col(0)
		act.width = 1200*20
		st.width = 200*20
		head = ['Actividades por realizar', 'Estatus']
		for index, value in enumerate(head):
			Por.write(0, index, value, encab)
		
		#rows=db(db.proyectos.status == 'EN CURSO')(db.proyectos.descri!='ACTIVIDADES SEMANAL')(db.proyectos.id == db.asignacion.cod_proyecto)\
		rows=db(db.proyectos.status == 'POR REALIZAR').select(orderby="descri")
		
		row = 1
		col = 0
		
		for index, r in enumerate(rows):
			Por.row(index).height_mismatch = True
			Por.row(index).height = 50*20
			Por.set_panes_frozen(True) # frozen headings instead of split panes
			Por.set_horz_split_pos(1) # in general, freeze after last heading row
			Por.set_remove_splits(True)
			Por.write (row, 0, r.descri, texto)
			Por.write (row, 1, r.status, textoC)
			row +=1
		#
			
		nombre=db.auth_user[me]
		from datetime import datetime
		fecha=convert_date(hasta)
		
		response.headers['Content-Type']='application/vnd.ms-excel'
		response.headers['Content-disposition'] = 'attachment; filename=%s %s - %s - GL DyA.xls' % (nombre.first_name.upper(), nombre.last_name.upper().decode('utf-8'), fecha) 
		wb.save(tmpfilename)
		data = open(tmpfilename,"rb").read()
		os.unlink(tmpfilename)
		return data
		
		
	elif formaOP.errors:
		response.flash = 'Fechas erradas'
	else:
		response.flash = 'Exito!'
		
	mis_actividades = db(db.actividades.id>0)(db.actividades.cod_asig==db.asignacion.id)(db.asignacion.analista==me).select()
	return locals()
	


@auth.requires_login()
def crear_actividades_sd():
	fecha = request.vars.fecha_inicio;
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#act_abiertas').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')

	NO_MOSTRAR_BD = (2,3,4,7)
	me = auth.user_id
	cia = auth.user.Empresa
	pic = auth.user.picture
	
	proyectos = [OPTION(str(datos.descri),_value=datos.id) 
	for datos in db(db.proyectos.id>0)(db.proyectos.status == 'EN CURSO').select(db.proyectos.ALL)]
	
	formaPA = FORM(TABLE(TR('Proyectos ', SELECT(*proyectos,**dict(_name="cod_proy")))))
	
	camposActividades_sd = [
		###########################################
		# MovCtas
		###########################################
		SELECT(*proyectos,**dict(_name="cod_proy")),
		INPUT(_name='cod_subp', _type='integer'),
		INPUT(_name='cod_servidor', _type='integer'),
		INPUT(_name='cod_bd', _type='integer'),
		INPUT(_name='descripcion', _type='textarea'),
		INPUT(_name='fecha_inicio', _type='datetime'),
		INPUT(_name='fecha_fin', _type='datetime'),
		INPUT(_name='ambiente_id'),
		INPUT(_name='horas_laboradas', _type='double',  _default=0.00),
		INPUT(_name='horas_extras', _type='double',  _default=0.00),
		INPUT(_name='tipo', _type='string', _default='P', _requires=IS_IN_SET(TIPO_ACT)),
		INPUT(_name='producto', _type='list', _default='INFORME' ),
		INPUT(_name='completado', _type='string:list', _default='NO COMPLETADA' ),
		INPUT(_name='analista', _type='integer', _default=auth.user_id ),
		INPUT(_name='incid_bd', _type='boolean'),
		INPUT(_name='incid_otros', _type='boolean'),
		INPUT(_name='obs_otros', _type='boolean'),
		INPUT(_name='bd_afecta', _type='boolean'),
		INPUT(_name='otros_afecta', _type='boolean'),
		]

	formaAct = FORM(*camposActividades_sd)
	
	if formaAct.accepts(request.vars,formname='formaActHTML', keepvalues=False):
		datosActividades_sd = db.actividades_sd._filter_fields(formaAct.vars)
		datosActividades_sd['cod_proy'] = formaAct.vars.cod_proy
		datosActividades_sd['cod_subp'] = formaAct.vars.cod_subp
		datosActividades_sd['analista'] = me

		datosActividades_sd['cod_servidor'] = formaAct.vars.cod_servidor
		datosActividades_sd['cod_bd'] = formaAct.vars.cod_bd

		bd=db.basedatos[request.vars.cod_bd]
		datosActividades_sd['ambiente_id'] = wambiente=bd.ambiente_id
		
		if request.vars.incid_bd == 'on':
			datosActividades_sd['incid_bd'] = 'True'
		else:
			datosActividades_sd['incid_bd'] = 'False'
					
		if request.vars.incid_otros == 'on':
			datosActividades_sd['incid_otros'] = 'True'
		else:
			datosActividades_sd['incid_otros'] = 'False'

		if formaAct.vars.completado == 'CERRADA':
			datosActividades_sd['fecha_cierre'] = request.now
			datosActividades_sd['cerrada_por'] = me

		fecha1 = request.vars.get('fecha_inicio')
		fecha2 = request.vars.get('fecha_fin')
		bd     = request.vars.get('cod_bd')
		
		e_fch1_rango_act=db(fecha1 >= db.actividades_sd.fecha_inicio)(fecha1 <= db.actividades_sd.fecha_fin)\
		(db.actividades_sd.analista==me).count()
		e_fch2_rango_act=db(fecha2 >= db.actividades_sd.fecha_inicio)(fecha2 <= db.actividades_sd.fecha_fin)\
		(db.actividades_sd.analista==me).count()

		e_fch1_rango_sact=db(fecha1 >= db.subactividades_sd.fecha_inicio)(fecha1 <= db.subactividades_sd.fecha_fin)\
		(db.subactividades_sd.analista==me).count()
		e_fch2_rango_sact=db(fecha2 >= db.subactividades_sd.fecha_inicio)(fecha2 <= db.subactividades_sd.fecha_fin)\
		(db.subactividades_sd.analista==me).count()


		if formaAct.vars.completado == 'CERRADA' and formaAct.vars.horas_laboradas == '0.00' and formaAct.vars.horas_extras == '0.00':
			session.flash='Actividad sin horas laboradas, por favor verifique!'

		elif e_fch1_rango_act>0 or e_fch2_rango_act>0 or e_fch1_rango_sact>0 or e_fch2_rango_sact>0:
			session.flash='Existe actividad o subactividad cargadas en el mismo rango de horas! (' + str(fecha1) + ' -- ' + str(fecha2) + ')'

		else:

			existen_fechas_dentro_rango_act=db(db.actividades_sd.fecha_inicio>=fecha1)(db.actividades_sd.fecha_fin<=fecha2)\
			(db.actividades_sd.analista==me).count()

			existen_fechas_dentro_rango_subact=db(db.subactividades_sd.fecha_inicio>=fecha1)(db.subactividades_sd.fecha_fin<=fecha2)\
			(db.subactividades_sd.analista==me).count()

			if existen_fechas_dentro_rango_act>0 or existen_fechas_dentro_rango_subact>0:
				session.flash='Existe actividad o subActividad dentro del rango de horas indicadas!'

			else:

				ActividadesInsertado = db.actividades_sd.insert(**datosActividades_sd)
				db.commit()
				session.flash='Registro insertado'
				#session.flash= formaAct.vars.completado + ' ' + formaAct.vars.horas_laboradas
				redirect(URL('crear_actividades_sd')) #evita que se dupliquen los registros al refrescar la pagina
		
	proyectos = db(db.proyectos.id >0)(db.proyectos.status != 'COMPLETADO').select(db.proyectos.ALL, orderby=db.proyectos.descri)
	subproyectos=db(db.subproyectos.id>0).select(db.subproyectos.ALL, orderby=db.subproyectos.descri)
	servidores=db(db.servidores.id>0)(db.servidores.status=='OPERATIVO').select(db.servidores.ALL, orderby=db.servidores.nombre)
	ambiente=db(db.ambiente.id>0).select()

	if request.vars.cod_proy:
		subproyectos = db(db.subproyectos.proyecto==request.vars.cod_proy).select(db.subproyectos.ALL, orderby=db.subproyectos.descri)
	else:
		subproyectos = db(db.subproyectos.proyecto==1).select(db.subproyectos.ALL, orderby=db.subproyectos.descri)

	if request.vars.cod_servidor:
		
		basedatos = db((db.basedatos.servidor==request.vars.cod_servidor) & (db.basedatos.estado_id.belongs(NO_MOSTRAR_BD) ))\
		.select(db.basedatos.ALL, orderby=db.basedatos.nombre)
		#basedatos = db(db.basedatos.servidor==request.vars.cod_servidor)(db.basedatos.estado_id in (3,4)).select(db.basedatos.ALL, orderby=db.basedatos.nombre )
	else:
		
		basedatos = db((db.basedatos.servidor==1) & (db.basedatos.estado_id.belongs(NO_MOSTRAR_BD) ))\
		.select(db.basedatos.ALL, orderby=db.basedatos.nombre)
		#basedatos = db(db.basedatos.servidor==1)(db.basedatos.estado_id in (3,4)).select(db.basedatos.id, db.basedatos.nombre, orderby=db.basedatos.nombre)
	
	now = datetime.datetime.now()
	hoy = now.strftime("%Y-%m-%d")
	
	a=db.actividades_sd
	mis_actividades = db(a.id>0)(a.fecha_inicio==formaAct.vars.fecha_inicio).select(orderby="fecha_inicio")
	act_abiertas=db(a.id>0)(a.completado !='CERRADA').select(orderby=a.analista|a.fecha_inicio)

	appl = db(db.basedatos.id>0)(db.basedatos.appl != 'None').\
	select(db.basedatos.nombre, db.basedatos.appl, db.basedatos.servidor, distinct=True, orderby="nombre")
	return locals()


def subproyecto():
	#response.flash='Codigo del proyecto: ' + request.vars.cod_proy
	subproyectos = db(db.subproyectos.proyecto==request.vars.cod_proy).select(db.subproyectos.ALL, orderby=db.subproyectos.descri)
	result = ""
	for subproyecto in subproyectos:
		result += "<option value='" + str(subproyecto.id) + "'>" + subproyecto.descri + "</option>"  
	return XML(result)

def func_bd():
	NO_MOSTRAR_BD = (2,3,4,7)
	basedatos = db((db.basedatos.servidor==request.vars.cod_servidor) & (db.basedatos.estado_id.belongs(NO_MOSTRAR_BD) ))\
	.select(db.basedatos.ALL, orderby=db.basedatos.nombre)
	result = ""
	for datos in basedatos:
		result += "<option value='" + str(datos.id) + "'>" + datos.nombre + "</option>"  
	return XML(result)

def func_amb():
	if request.vars.cod_bd:
		bd=db.basedatos[request.vars.cod_bd] or redirect(error_page)
		wambiente=bd.ambiente_id
		ambiente = db(db.ambiente.id==wambiente).select(db.ambiente.ALL, orderby=db.ambiente.descri )
	else:
		ambiente = db(db.ambiente.id>0).select(db.ambiente.id, db.ambiente.descri, orderby=db.ambiente.descri)
	result = ""
	for datos in ambiente:
		result += "<option value='" + str(datos.id) + "'>" + datos.descri + "</option>"  
	return XML(result)

def func_mac_sd():
	from datetime import date, datetime
	from dateutil.parser import parse
	from gluon.html import XML
	
	try:
		# Validar autenticación
		if not auth.user:
			return XML("<div class='alert alert-danger'>Error: Usuario no autenticado</div>")
			
		me = auth.user_id
		total_horas = 0
		total_extra = 0
		cant_act = 0
		tablaHTML = ""
		
		# Validar parámetro fecha_inicio
		if not request.vars.fecha_inicio or len(request.vars.fecha_inicio) < 10:
			return XML("<div class='alert alert-danger'>Error: Parámetro fecha_inicio no proporcionado o inválido</div>")
			
		fecha = request.vars.fecha_inicio[0:10]
		
		try:
			start = parse('%s 00:00:00' % fecha)
			end = parse('%s 23:59:59' % fecha)
		except Exception as e:
			return XML("<div class='alert alert-danger'>Error al procesar fechas: %s</div>" % str(e))
		
		format_date = '%d-%m-%Y %H:%M%p'
		
		# Consulta actividades principales
		mis_actividades_sd = db((db.actividades_sd.id > 0) &
							  (db.actividades_sd.fecha_inicio >= start) &
							  (db.actividades_sd.fecha_inicio <= end) &
							  (db.actividades_sd.analista == me)
							 ).select(orderby=~db.actividades_sd.fecha_inicio)
		
		if mis_actividades_sd:
			tablaHTML = """
			   
			<table cellpadding='3' id='' style='max-width:100%; font-size: 12px;' class='table-bordered table-striped'>
				<col style='width:5%;'>
				<col style='width:15%'>
				<col style='width:20%'>
				<col style='width:10%'>
				<col style='width:34%'>
				<col style='width:8%'>
				<col style='width:8%'>
				<col style='width:5%'>
				<col style='width:5%'>
				<thead>
					<tr style='background-color: #c1edd6;' rowspan='1'>
						<th colspan='5' style='color: black; font-weight: bold; font-size: 14px;'>Descripción de actividades realizadas</th>
						<th colspan='2' style='text-align: center;'>Fechas</th>
						<th colspan='1' style='text-align: center;'>Total</th>
						<th colspan='1' style='text-align: center;'>Extra</th>
						<th colspan='2' style='text-align: center;'>Tipo</th>
					</tr>
				</thead>
				<tbody>
			"""
			
			for datos in mis_actividades_sd:
				# Validar campos relacionales
				ambiente = str(show_status(datos.ambiente_id.descri)) if datos.ambiente_id else ''
				proyecto = str(datos.cod_proy.descri) if datos.cod_proy else ''
				subproyecto = str(datos.cod_subp.descri) if datos.cod_subp else ''
				basedatos = str(datos.cod_bd.nombre) if datos.cod_bd and datos.cod_bd > 0 else ''
				
				# Determinar estilo según tipo de incidencia
				if datos.incid_bd:
					desc_style = "color: red; font-weight: bold; font-size: 16px;"
					desc_text = "** BD **: " + str(datos.descripcion)
				elif datos.incid_otros:
					desc_style = "color: red; font-weight: bold; font-size: 16px;"
					desc_text = "** Otros **: " + str(datos.descripcion) + " (" + str(datos.obs_otros or '') + ")"
				else:
					desc_style = "color: black; font-weight: bold; font-size: 16px;"
					desc_text = str(datos.descripcion)
				
				# Validar fechas
				fecha_inicio = datos.fecha_inicio.strftime(format_date) if datos.fecha_inicio else ''
				fecha_fin = datos.fecha_fin.strftime(format_date) if datos.fecha_fin else ''
				
				tablaHTML += f"""
				<tr>
					<td style='background-color: rgb(51,255,153)'>{ambiente}</td>
					<td>{proyecto}</td>
					<td>{subproyecto}</td>
					<td>{basedatos}</td>
					<td><a style='{desc_style}' href='editar_actividades3?act={datos.id}'>{desc_text}</a></td>
					<td colspan='1'>{fecha_inicio}</td>
					<td colspan='1'>{fecha_fin}</td>
					<td style='color: red; font-weight: bold; font-size: 12px;'>{datos.horas_laboradas or 0}</td>
					<td style='color: red; font-weight: bold; font-size: 12px;'>{datos.horas_extras or 0}</td>
					<td>{datos.tipo or ''}</td>
				</tr>
				"""
				total_horas += datos.horas_laboradas or 0
				total_extra += datos.horas_extras or 0
				cant_act += 1
			
			tablaHTML += f"""
				</tbody>
				<tfoot>
					<tr>
						<th style='font-size: 14px; color: #40b5e1;' id='total' colspan='7'>Total horas:</th>
						<td colspan='' style='color: red; font-weight: bold; font-size: 14px;'>{total_horas}</td>
						<td colspan='' style='color: red; font-weight: bold; font-size: 14px;'>{total_extra}</td>
						<td style='color: black; font-weight: bold; font-size: 18px;'>{cant_act}</td>
					</tr>
				</tfoot>
			</table>
			
			"""
		
		# Consulta subactividades
		mis_subactividades_sd = db((db.subactividades_sd.id > 0) &
								 (db.subactividades_sd.fecha_inicio >= start) &
								 (db.subactividades_sd.fecha_fin <= end) &
								 (db.subactividades_sd.analista == me)
								).select(orderby=~db.subactividades_sd.fecha_inicio)
		
		if mis_subactividades_sd:
			tablaHTML += """
			<table cellpadding='3' id='' style='max-width:100%; font-size: 12px; margin-top: 20px;' class='table-bordered'>
				<col style='width:5%;'>
				<col style='width:15%'>
				<col style='width:20%'>
				<col style='width:10%'>
				<col style='width:34%'>
				<col style='width:8%'>
				<col style='width:8%'>
				<col style='width:5%'>
				<col style='width:5%'>
				<thead>
					<tr style='background-color: #c1edd6;' rowspan='1'>
						<th colspan='5' style='color: black; font-weight: bold; font-size: 14px;'>Descripción actividades de Bitácora</th>
						<th colspan='2' style='text-align: center;'>Fechas</th>
						<th colspan='1' style='text-align: center;'>Total</th>
						<th colspan='1' style='text-align: center;'>Extra</th>
						<th colspan='2' style='text-align: center;'>Tipo</th>
					</tr>
				</thead>
				<tbody>
			"""
			
			total_horas = 0
			total_extra = 0
			cant_act = 0
			
			for datos in mis_subactividades_sd:
				proyecto = str(datos.cod_proy.descri) if datos.cod_proy else ''
				subproyecto = str(datos.cod_subp.descri) if datos.cod_subp else ''
				basedatos = str(datos.cod_bd.nombre) if datos.cod_bd and datos.cod_bd > 0 else ''
				
				fecha_inicio = datos.fecha_inicio.strftime(format_date) if datos.fecha_inicio else ''
				fecha_fin = datos.fecha_fin.strftime(format_date) if datos.fecha_fin else ''
				
				tablaHTML += f"""
				<tr>
					<td></td>
					<td>{proyecto}</td>
					<td>{subproyecto}</td>
					<td>{basedatos}</td>
					<td>{datos.descripcion or ''}</td>
					<td colspan='1'>{fecha_inicio}</td>
					<td colspan='1'>{fecha_fin}</td>
					<td style='color: red; font-weight: bold; font-size: 12px;'>{datos.horas_laboradas or 0}</td>
					<td style='color: red; font-weight: bold; font-size: 12px;'>{datos.horas_extras or 0}</td>
					<td>{datos.tipo or ''}</td>
				</tr>
				"""
				total_horas += datos.horas_laboradas or 0
				total_extra += datos.horas_extras or 0
				cant_act += 1
			
			tablaHTML += f"""
				</tbody>
				<tfoot>
					<tr>
						<th style='font-size: 14px; color: #40b5e1;' id='total' colspan='7'>Total horas:</th>
						<td colspan='' style='color: red; font-weight: bold; font-size: 14px;'>{total_horas}</td>
						<td colspan='' style='color: red; font-weight: bold; font-size: 14px;'>{total_extra}</td>
						<td style='color: black; font-weight: bold; font-size: 18px;'>{cant_act}</td>
					</tr>
				</tfoot>
			</table>
			"""
		
		return XML(tablaHTML if tablaHTML else "<div class='alert alert-info'>No se encontraron actividades para esta fecha</div>")
		
	except Exception as e:
		import traceback
		tb = traceback.format_exc()
		return XML(f"<div class='alert alert-danger'>Error inesperado: {str(e)}<br><pre>{tb}</pre></div>")


#====================== prueba


@auth.requires_login()
def crear_actividades_sd2():
	fecha = request.vars.fecha_inicio;
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#act_abiertas').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	
	NO_MOSTRAR_BD = (2,3,4,7)
	me = auth.user_id
	
	proyectos = [OPTION(str(datos.descri),_value=datos.id) 
	for datos in db(db.proyectos.id>0)(db.proyectos.status == 'EN CURSO').select(db.proyectos.ALL)]

	
	formaPA = FORM(TABLE(TR('Proyectos ', SELECT(*proyectos,**dict(_name="cod_proy")))))
	
	camposActividades_sd = [
		###########################################
		# MovCtas
		###########################################
		SELECT(*proyectos,**dict(_name="cod_proy")),
		INPUT(_name='cod_subp', _type='integer'),
		INPUT(_name='cod_servidor', _type='integer'),
		INPUT(_name='cod_bd', _type='integer'),
		INPUT(_name='descripcion', _type='textarea'),
		INPUT(_name='fecha_inicio', _type='datetime'),
		INPUT(_name='fecha_fin', _type='datetime'),
		INPUT(_name='ambiente_id'),
		INPUT(_name='horas_laboradas', _type='double',  _default=0.00),
		INPUT(_name='horas_extras', _type='double',  _default=0.00),
		INPUT(_name='tipo', _type='string', _default='P', _requires=IS_IN_SET(TIPO_ACT)),
		INPUT(_name='producto', _type='list', _default='INFORME' ),
		INPUT(_name='completado', _type='string:list', _default='NO COMPLETADA' ),
		INPUT(_name='analista', _type='integer', _default=auth.user_id ),
		INPUT(_name='incid_bd', _type='boolean'),
		INPUT(_name='incid_otros', _type='boolean'),
		INPUT(_name='obs_otros', _type='boolean'),
		INPUT(_name='bd_afecta', _type='boolean'),
		INPUT(_name='otros_afecta', _type='boolean'),
		]

	formaAct = FORM(*camposActividades_sd)
	
	if formaAct.accepts(request.vars,formname='formaActHTML', keepvalues=False):
		datosActividades_sd = db.actividades_sd._filter_fields(formaAct.vars)
		datosActividades_sd['cod_proy'] = formaAct.vars.cod_proy
		datosActividades_sd['cod_subp'] = formaAct.vars.cod_subp
		datosActividades_sd['analista'] = me

		datosActividades_sd['cod_servidor'] = formaAct.vars.cod_servidor
		datosActividades_sd['cod_bd'] = formaAct.vars.cod_bd


		bd=db.basedatos[request.vars.cod_bd]
		datosActividades_sd['ambiente_id'] = wambiente=bd.ambiente_id
		
		if request.vars.incid_bd == 'on':
			datosActividades_sd['incid_bd'] = 'True'
		else:
			datosActividades_sd['incid_bd'] = 'False'
					
		if request.vars.incid_otros == 'on':
			datosActividades_sd['incid_otros'] = 'True'
		else:
			datosActividades_sd['incid_otros'] = 'False'

		#if request.vars.cod_bd:
		#	bd=db.basedatos[request.vars.cod_bd] or redirect(error_page)
		#	wambiente=bd.ambiente_id
		#	ambiente = db(db.ambiente.id==wambiente).select(db.ambiente.ALL, orderby=db.ambiente.descri )
		#else:
		#	ambiente = db(db.ambiente.id>0).select(db.ambiente.id, db.ambiente.descri, orderby=db.ambiente.descri)

		if formaAct.vars.completado == 'CERRADA':
			datosActividades_sd['fecha_cierre'] = request.now
			datosActividades_sd['cerrada_por'] = me

		fecha1 = request.vars.get('fecha_inicio')
		fecha2 = request.vars.get('fecha_fin')
		bd     = request.vars.get('cod_bd')
		
		
		e_fch1_rango_act=db(fecha1 >= db.actividades_sd.fecha_inicio)(fecha1 <= db.actividades_sd.fecha_fin)\
		(db.actividades_sd.analista==me).count()
		e_fch2_rango_act=db(fecha2 >= db.actividades_sd.fecha_inicio)(fecha2 <= db.actividades_sd.fecha_fin)\
		(db.actividades_sd.analista==me).count()

		e_fch1_rango_sact=db(fecha1 >= db.subactividades_sd.fecha_inicio)(fecha1 <= db.subactividades_sd.fecha_fin)\
		(db.subactividades_sd.analista==me).count()
		e_fch2_rango_sact=db(fecha2 >= db.subactividades_sd.fecha_inicio)(fecha2 <= db.subactividades_sd.fecha_fin)\
		(db.subactividades_sd.analista==me).count()


		#existen_fechas_act=db(db.actividades_sd.fecha_inicio==fecha1)(db.actividades_sd.fecha_fin==fecha2)\
		#(db.actividades_sd.analista==me).count()
		
		#existen_fechas_subact=db(db.subactividades_sd.fecha_inicio==fecha1)(db.subactividades_sd.fecha_fin==fecha2)\
		#(db.subactividades_sd.analista==me).count()

		if formaAct.vars.completado == 'CERRADA' and formaAct.vars.horas_laboradas == '0.00' and formaAct.vars.horas_extras == '0.00':
			session.flash='Actividad sin horas laboradas, por favor verifique!'

		elif e_fch1_rango_act>0 or e_fch2_rango_act>0 or e_fch1_rango_sact>0 or e_fch2_rango_sact>0:
			session.flash='Existe actividad o subactividad cargadas en el mismo rango de horas! (' + str(fecha1) + ' -- ' + str(fecha2) + ')'

		else:

			existen_fechas_dentro_rango_act=db(db.actividades_sd.fecha_inicio>=fecha1)(db.actividades_sd.fecha_fin<=fecha2)\
			(db.actividades_sd.analista==me).count()

			existen_fechas_dentro_rango_subact=db(db.subactividades_sd.fecha_inicio>=fecha1)(db.subactividades_sd.fecha_fin<=fecha2)\
			(db.subactividades_sd.analista==me).count()

			if existen_fechas_dentro_rango_act>0 or existen_fechas_dentro_rango_subact>0:
				session.flash='Existe actividad o subActividad dentro del rango de horas indicadas!'

			else:

				ActividadesInsertado = db.actividades_sd.insert(**datosActividades_sd)
				db.commit()
				session.flash='Registro insertado'
				#session.flash= formaAct.vars.completado + ' ' + formaAct.vars.horas_laboradas
				redirect(URL('crear_actividades_sd2')) #evita que se dupliquen los registros al refrescar la pagina
		
						
		
	proyectos = db(db.proyectos.id >0)(db.proyectos.status != 'COMPLETADO').select(db.proyectos.ALL, orderby=db.proyectos.descri)
	subproyectos=db(db.subproyectos.id>0).select(db.subproyectos.ALL, orderby=db.subproyectos.descri)
	servidores=db(db.servidores.id>0)(db.servidores.status=='OPERATIVO').select(db.servidores.ALL, orderby=db.servidores.nombre)
	ambiente=db(db.ambiente.id>0).select()
	

	if request.vars.cod_proy:
		subproyectos = db(db.subproyectos.proyecto==request.vars.cod_proy).select(db.subproyectos.ALL, orderby=db.subproyectos.descri)
	else:
		subproyectos = db(db.subproyectos.proyecto==1).select(db.subproyectos.ALL, orderby=db.subproyectos.descri)

	if request.vars.cod_servidor:
		basedatos = db((db.basedatos.servidor==request.vars.cod_servidor) & (db.basedatos.estado_id.belongs(NO_MOSTRAR_BD) ))\
		.select(db.basedatos.ALL, orderby=db.basedatos.nombre)

	else:
		basedatos = db((db.basedatos.servidor==1) & (db.basedatos.estado_id.belongs(NO_MOSTRAR_BD) ))\
		.select(db.basedatos.ALL, orderby=db.basedatos.nombre)

	#if request.vars.cod_bd:
	#	bd=db.basedatos[request.vars.cod_bd] or redirect(error_page)
	#	wambiente=bd.ambiente_id
	#	ambiente = db(db.ambiente.id==wambiente).select(db.ambiente.ALL, orderby=db.ambiente.descri )
	#else:
	#	ambiente = db(db.ambiente.id>0).select(db.ambiente.id, db.ambiente.descri, orderby=db.ambiente.descri)

	
	now = datetime.datetime.now()
	hoy = now.strftime("%Y-%m-%d")
	
	a=db.actividades_sd
	mis_actividades = db(a.id>0)(a.fecha_inicio==formaAct.vars.fecha_inicio).select(orderby="fecha_inicio")
	act_abiertas=db(a.id>0)(a.completado !='CERRADA').select(orderby=a.analista|a.fecha_inicio)

	appl = db(db.basedatos.id>0)(db.basedatos.appl != 'None').\
	select(db.basedatos.nombre, db.basedatos.appl, db.basedatos.servidor, distinct=True, orderby="nombre")
	return locals()


#====================== prueba


def editar_actividades3():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#mis_actividades').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')

	act_id=request.args(0)
	fecha = request.vars.fecha_inicio;
	act=request.vars.act
	query = (db.actividades_sd.id==request.vars.act)
	actividad_id=request.vars.act
	actividad_reg=db.actividades_sd[actividad_id] or redirect(error_page)
	db.actividades_sd.cod_proy.writable=False
	db.actividades_sd.cod_proy.readable=False
	db.actividades_sd.cod_subp.writable=False
	db.actividades_sd.cod_subp.readable=False

	#actividad = db.actividades_bdv[actividad_id] 
	#editable = actividad.completado not in ("CERRADA") 
	#if editable:
	#form=crud.update(db.actividades_bdv, actividad_reg.id, deletable=editable, next=url('crear_actividades_bdv'))
	form=crud.update(db.actividades_sd, actividad_reg.id, next=url('crear_actividades_sd'))
	#else:
	#	#session.flash= "Esta actividad está cerrada"
	#	#redirect(URL(r=request, c='default', f='crear_actividades_bdv'))
	#	form=crud.read(db.actividades_bdv, actividad_reg.id )
	return 	locals()

@auth.requires_login()
def list_actividades_sd():
	
	form=crud.create(db.actividades_sd)
	query = db.actividades_sd.id>0
	rows = db(query).select(orderby=db.actividades_sd.analista|db.actividades_sd.fecha_inicio)

	if db._lastsql:
		session.flash='1ra vez o no almacenado en cache'
	else:
		session.flash='En cache'

	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_actividades_sd').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	session.flash='Bienvenido'
	return dict(form=form, rows=rows, script=script)



def editar_actividades_sd():
	actividad_id = db.actividades_sd(request.vars.get('actividad')) or redirect(URL('list_actividades_sd'))
	form = crud.update(db.actividades_sd,actividad_id,next='list_actividades_sd')
	return locals()



# --------------------- solutor delta -------------------------------------------------------

@auth.requires_login()
def crear_actividades2():
	fecha = request.vars.fecha_inicio;
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#basedatos').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	
	me = auth.user_id
	
	proyectos_asignados = [OPTION(str(datos.proyectos.descri),_value=datos.asignacion.id) 
	for datos in db(db.asignacion.analista==me)(db.proyectos.id == db.asignacion.cod_proyecto)(db.proyectos.status=='EN CURSO').select(db.proyectos.ALL, db.asignacion.ALL)]

	
	formaPA = FORM(TABLE(TR('Proyectos ', SELECT(*proyectos_asignados,**dict(_name="cod_asig")))))
	
	camposActividades = [
		###########################################
		# MovCtas
		###########################################
		SELECT(*proyectos_asignados,**dict(_name="cod_asig")),
		INPUT(_name='descripcion', _type='textarea'),
		INPUT(_name='fecha_inicio', _type='datetime'),
		INPUT(_name='hora_inicio', _type='sting', _requires=IS_TIME(error_message='Hora no valida')	, default='08:00'),
		INPUT(_name='hora_fin', _type='sting', _requires=IS_TIME(error_message='Hora no valida')	, default='12:30'),
		INPUT(_name='horas_diurnas', _type='double', _requires=IS_NOT_EMPTY(error_message='No puede ser nulo'), _notnull=True, _default=0.00),
		INPUT(_name='horas_nocturnas', _type='double',  _default=0.00),
		INPUT(_name='horas_diurnas_r', _type='double'),
		INPUT(_name='horas_nocturnas_r', _type='double',  _default=0.00),
		
		INPUT(_name='tipo', _type='string', _default='P', _requires=IS_IN_SET(TIPO_ACT)),
		INPUT(_name='producto', _type='list', _default='INFORME' ),
		INPUT(_name='completado', _type='string:list', _default='CERRADA' ),
		]

	formaAct = FORM(*camposActividades)
	
	if formaAct.accepts(request.vars,formname='formaActHTML', keepvalues=False):
		datosActividades = db.actividades._filter_fields(formaAct.vars)
		datosActividades['cod_asig'] = formaAct.vars.cod_asig
		if formaAct.vars.tipo=="R":
			datosActividades['horas_diurnas_r']=formaAct.vars.horas_diurnas;
			datosActividades['horas_nocturnas_r']=formaAct.vars.horas_nocturnas;
			datosActividades['horas_diurnas'] = 0.00;
			datosActividades['horas_nocturnas'] = 0.00;
		else:
			datosActividades['horas_diurnas_r']=0.00;
			datosActividades['horas_nocturnas_r']=0.00;
			
		ActividadesInsertado = db.actividades.insert(**datosActividades)
		session.flash='Registro insertado'
		
		proy_id=db(db.proyectos.id==db.asignacion.cod_proyecto)(db.actividades.cod_asig==db.asignacion.id)(db.actividades.id==ActividadesInsertado)\
		.select(db.proyectos.id).first()
		

			
		db(db.asignacion.id==formaAct.vars.cod_asig).update(status='INICIADO')
		db(db.proyectos.id == proy_id).update(status = 'EN CURSO')
		asignacion_id=formaAct.vars.cod_asig
		asignacion=db.asignacion[asignacion_id]
		calcula_porcentaje(asignacion)
		#reinicia_asignacion(asignacion)
		#----
		db.commit()
		redirect(URL('crear_actividades')) #evita que se dupliquen los registros al refrescar la pagina
		
		
		
		
	LISTA=['POR REALIZAR','COMPLETADO']
	proyectos_asignados = db(db.asignacion.analista==me)\
	(db.proyectos.id == db.asignacion.cod_proyecto)\
	(~db.proyectos.status.belongs(LISTA)).select(db.proyectos.ALL, db.asignacion.ALL)
	now = datetime.datetime.now()
	hoy = now.strftime("%Y-%m-%d")
	#mis_actividades = db(db.actividades.id>0)(db.actividades.fecha_inicio==hoy)\
	mis_actividades = db(db.actividades.id>0)(db.actividades.fecha_inicio==formaAct.vars.fecha_inicio)\
	(db.actividades.cod_asig==db.asignacion.id)(db.asignacion.analista==me).select(orderby="hora_inicio")
	appl = db(db.basedatos.id>0)(db.basedatos.appl != 'None').select(db.basedatos.nombre, db.basedatos.appl, db.basedatos.servidor, distinct=True, orderby="nombre")
	return locals()



def func_mac():
	import math
	fecha = request.vars.fecha_inicio;
	#session.flash=fecha;
	total_horas=0;
	mis_actividades = db(db.actividades.id>0)\
	(db.actividades.fecha_inicio==fecha)\
	(db.actividades.cod_asig==db.asignacion.id)(db.asignacion.analista==me).select(orderby="hora_inicio")
	
	# cambia a 100% para que el detalle quede bien 
	tablaHTML = "<table id='' style='max-width:80%; font-size: 12px;' class='texto table table-bordered '>"
	tablaHTML +="<col style='width:80%'>"
	tablaHTML +="<col style='width:10%'>"
	tablaHTML +="<col style='width:5%'>"
	tablaHTML +="<col style='width:5%'>"
	tablaHTML +="<col style='width:5%'>"
	tablaHTML +="<col style='width:5%'>"
	tablaHTML +="<col style='width:5%'>"
	tablaHTML +="<col style='width:5%'>"
	tablaHTML +="<col style='width:5%'>"
	tablaHTML +="<thead> <tr rowspan='1'><th>Descripción</th><th>Fecha</th><th colspan='2' style='text-align: center;' >Hora</th><th colspan='2' style='text-align: center;'>Horas remotas</th> <th colspan='2' style='text-align: center;'>Horas presenciales</th></tr>"
	tablaHTML +=" <tr><th></th><th></th><th>Inicio</th><th>Fin</th><th>Diurnas</th><th>Nocturnas</th> <th>Diurnas</th><th>Nocturnas</th> </tr></thead>"
	tablaHTML +="<tbody>"
	
	sumHDR = 0;
	sumHNR = 0;
	sumHD  = 0;
	sumHN  = 0;

	for datos in mis_actividades:
		tablaHTML +="<tr>"
		tablaHTML +="<td>" + "<a style='color: black;  font-weight: bold; ont-size: 16px;' href='editar_actividades2?act=" + str(datos.actividades.id) +  " '>"  + str(datos.actividades.descripcion) + "</a>" + "</td>"
		tablaHTML +="<td>" + str(datos.actividades.fecha_inicio.strftime('%d/%m/%Y')) + "</td>"
		tablaHTML +="<td>" + str(datos.actividades.hora_inicio) + "</td>"
		tablaHTML +="<td>" + str(datos.actividades.hora_fin) + "</td>"
		
		#remotas
		tablaHTML +="<td>" + str(datos.actividades.horas_diurnas_r) + "</td>"
		tablaHTML +="<td>" + str(datos.actividades.horas_nocturnas_r) + "</td>"
		#presenciales
		tablaHTML +="<td>" + str(datos.actividades.horas_diurnas) + "</td>"
		tablaHTML +="<td>" + str(datos.actividades.horas_nocturnas) + "</td>"

		sumHDR = sumHDR + (datos.actividades.horas_diurnas_r);
		sumHNR = sumHNR + (datos.actividades.horas_nocturnas_r);
		
		#sumHD = sumHD + round(datos.actividades.horas_diurnas); # redondeo hacia arriba
		sumHD = sumHD + (datos.actividades.horas_diurnas); 
		sumHN = sumHN + (datos.actividades.horas_nocturnas);
		
		tablaHTML +="</tr>"
		#total_horas = total_horas + atos.actividades.horas_laboradas;


	tablaHTML +="</tbody>"
	tablaHTML +="<tfoot>"
	tablaHTML +="<tr>"
	tablaHTML +="<th style='font-size: 14px; font-color=#40b5e1' id='total' colspan='4' >Total horas:</th>"

	tablaHTML +='<td style="font-weight: bold; font-size: 14px;">' + str(sumHDR) + '</td>''<td style="font-weight: bold; font-size: 14px;">' + str(sumHNR) + '</td>''<td style="font-weight: bold; font-size: 14px;">' + str(sumHD) + '</td>''<td style="font-weight: bold; font-size: 14px;">' + str(sumHN) + '</td>' 
	tablaHTML +="</tr>"
	tablaHTML +="</tfoot>"

	tablaHTML +="</table>"
	return XML(tablaHTML)
	
def editar_actividades2():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#mis_actividades').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')

	fecha = request.vars.fecha_inicio;
	act=request.vars.act
	query = (db.actividades.id==request.vars.act)
	actividad_id=request.vars.act
	actividad_reg=db.actividades[actividad_id] or redirect(error_page)
	db.actividades.cod_asig.writable=False
	db.actividades.cod_asig.readable=False
	form=crud.update(db.actividades, actividad_reg.id, next=url('crear_actividades'))


	return 	locals()




def editar_actividades4():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#mis_actividades').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	
	db.actividades_sd.cod_proy.writable=False
	db.actividades_sd.cod_proy.readable=False
	db.actividades_sd.cod_subp.writable=False
	db.actividades_sd.cod_subp.readable=False

	act_id=request.args(0,cast=int)
	#actividad_reg=db.actividades_sd[act_id]  or redirect(error_page)

	actividad = db.actividades_sd[act_id] or redirect(error_page) 
	editable = actividad.completado not in ("CERRADA") 
	#if editable:
	form=crud.update(db.actividades_sd, actividad.id, deletable=editable, next=url('list_actividades_sd'))
	#else:
	#	form=crud.read(db.actividades_sd, actividad.id )

	#form=crud.update(db.actividades_sd, actividad_reg.id, next=url('crear_actividades_sd'))
	return 	form


def valida_actividad():
	descri = request.vars.descripcion
	act=db(db.actividades.descripcion == descri).select().first()
	
	if act:
		return 'yes'
	else:
		return 'no'
	return locals()



@auth.requires_login()
def editar_actividades():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#mis_actividades').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	
	mis_actividades = db(db.actividades.id>0)(db.actividades.cod_asig==db.asignacion.id)(db.asignacion.analista==me).select()

	db.actividades.cod_asig.writable=False
	db.actividades.cod_asig.readable=False
	
	#crud.settings.update_onaccept = calcula_porcentaje(asig)
	return locals()

@auth.requires_login()
def edita():
	actividad_id=request.args(0)
	actividad_reg=db.actividades[actividad_id] or redirect(error_page)
	asignacion_id=request.args(1)
	asig = db.asignacion[request.args(1)]
	db.actividades.cod_asig.writable=False
	db.actividades.cod_asig.readable=False
	
	datos = db.proyectos[request.args(2)]
	#datos=db(db.asignacion.id == asig)(db.proyectos.id==db.asignacion.cod_proyecto).select(db.proyectos.ALL)
	if datos.status == 'COMPLETADO':
		crud.settings.update_deletable = False
		db.actividades.descripcion.writable=False
		db.actividades.fecha_inicio.writable=False
		db.actividades.hora_inicio.writable=False
		db.actividades.hora_fin.writable=False
		db.actividades.horas_diurnas.writable=False
		db.actividades.tipo.writable=False
		db.actividades.completado.writable=False
		db.actividades.producto.writable=False
		
		session.flash ='El proyecto está completado...'
		
	#crud.settings.update_onaccept = disminuye_horas(asig, actividad_reg.horas_laboradas)	
	#form=crud.update(db.actividades, ondelete = disminuye_horas(asig, actividad_reg.horas_laboradas)	, actividad_reg.id, next=url('editar_actividades'))
	#ondelete = disminuye_horas_ejecutadas(asig, actividad_reg.id),
	form=crud.update(db.actividades, actividad_reg.id,  next=url('editar_actividades'))
	crud.messages.record_updated = 'Record Updated' 
	crud.messages.record_deleted = 'Registro Borrado' 
	if form.accepts(request):
		horas = form.vars.horas_diurnas
		heje = db.asignacion[asig.id].horas_ejecutadas
		dif = heje - horas
		db(db.asignacion.id == asig.id).update(horas_ejecutadas=dif)
		db.commit
		response.flash = 'Actualizado con exito'
	elif form.errors:
		response.flash = 'Error al actualizar'
	else:
		#response.flash = 'Error al actualizarxxxxxx'
		pass
	return dict(form=form, asignacion_id=asignacion_id)	

def disminuye_horas_ejecutadas(asig, act):
	hlab = 0.00
	heje = 0.00
	por  = 0.00
	dif  = 0.00
			
	heje = db.asignacion[asig.id].horas_ejecutadas
	hlab = db.actividades[act].horas_diurnas
	dif = heje - hlab
	asig.update_record(horas_ejecutadas = dif)
	session.flash ='El proyecto estÃ¡ completado...'
	return dict(resultado=dif)
	


def proyectos_asginados():
	#cliente = request.vars.f_cedula_titular
	proyectos_asignados = db(db.asignacion.analista==me)(db.proyectos.id == db.asignacion.cod_proyecto)(db.proyectos.status=='EN CURSO').select(db.proyectos.ALL, db.asignacion.ALL)
	
	dropdownHTML =	"<label for='cod_asig'>Proyectos </label>"
	dropdownHTML += "<select class='generic-widget' name='cod_asig' id='cod_asig'>"
	for datos in proyectos_asignados:
		dropdownHTML += "<option value='" + str(datos.asignacion.cod_asig) + "'>"  + str(datos.proyectos.descri) + "</option>"  
	dropdownHTML += "</select>"
	return XML(dropdownHTML)


@auth.requires_login()
def resumen():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#resumen').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	#PMs=db(db.auth_user.id>0 and db.auth_user.username != 'otro' and db.asignacion.analista==db.auth_user.id).select(distinct=True)
	dbas=db(db.auth_user.id>0 and db.auth_user.username != 'otro').select(distinct=True)
	return dict(dbas=dbas, script=script)

def buscar_detalle1():
	analista = request.vars.analista
	asig=db.asignacion
	acti=db.actividades
	print ("x = ", request.vars.analista)
	session.flash=analista
	detalleActividades=db(asig.analista == 1)(asig.id == acti.cod_asig).select(acti.descripcion, acti.fecha_inicio)
	
	tablaHTML  ="<div> " + str(analista) + " no hay"
	tablaHTML +="<table id='resumen' class='smarttable' >"
	tablaHTML +="<col style='width:30%'>"
	tablaHTML +="<col style='width:5%'>"
	tablaHTML +="<thead><tr><th>Descripcion</th><th>Fecha Actividad</th></tr></thead>"

	for datos in detalleActividades:
		tablaHTML += "<tr>"
		tablaHTML += "<td>" + str(datos.descripcion) + " </td>" 
		tablaHTML += "<td>" + str(datos.fecha_inicio) + " </td>" 
		tablaHTML += "</tr>"
	tablaHTML += "</tbody>"
	tablaHTML += "</table>"
	tablaHTML += "</div>"
	return XML(tablaHTML)
	

def convert_date(date_time): 
	import datetime
	format = '%Y-%m-%d' # The format 
	datetime_str = datetime.datetime.strptime(date_time, format) 
	return datetime_str.strftime('%m%d%Y')

@auth.requires_login()
def detalle_actividad():
	me = auth.user_id
	form=None
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#ver_actividades').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	
	asignacion_id=request.args(0) or session.asignacion_id
	asignacion=db.asignacion[asignacion_id]
	
	if asignacion:
		
		session.asignacion_id=asignacion.id
		db.actividades.cod_asig.default=asignacion_id
		db.actividades.cod_asig.writable=False
		db.actividades.cod_asig.readable=False
		
		form=crud.create(db.actividades)
		actividades = db(db.actividades.cod_asig==asignacion).select()
		if actividades:
			calcula_porcentaje(asignacion)
		else:
			reinicia_asignacion(asignacion)
			
		actividades_reg=db(db.actividades.cod_asig==asignacion.id).select()
	else:
		actividades_reg=db(db.actividades).select(orderby="actividades.fecha_inicio")

	return dict(actividades_reg=actividades_reg, script=script, form=form, asignacion=asignacion, asignacion_id=session.asignacion_id)




@auth.requires_login()
def ver_actividades():
	me = auth.user_id
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#ver_actividades').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	
	mis_actividades=db(db.actividades.id>0)(db.actividades.cod_asig == db.asignacion.id)\
	(db.asignacion.analista==me).select(orderby="actividades.fecha_inicio,actividades.hora_inicio")

	return dict(mis_actividades=mis_actividades, script=script)


def calcula_porcentaje(asig):
	actividades = db(db.actividades.cod_asig==asig).select()
	cant  = 0
	suma  = 0.00
	horas = 0.00
	por   = 0.00
	c     = 0
	
	for a in actividades:
		cant  += 1
		#suma  += a.porc_completado
		horas += a.horas_diurnas
		if a.completado == 'COMPLETADA':
			c += 1
	
	#por = suma 
	asig.update_record(status='INICIADO', porc_completado = c*100/cant , horas_ejecutadas = horas)
	#db(db.asignacion.id == asig).update(status = 'INICIADO', )
	#db(db.asignacion.id == asig).update(porc_completado = por)
	#db(db.asignacion.id == asig).update(horas_ejecutadas = horas)
	#db.commit
	return por

def reinicia_asignacion(asig):
	asig.update_record(status='NO INICIADO', porc_completado = 0.00, horas_ejecutadas = 0.00)
	return True

@auth.requires_login()
def edit_actividad():
	actividad_id=request.args(0)
	actividad_reg=db.actividades[actividad_id] or redirect(error_page)
	asignacion_id=request.args(1)
	asig = db.asignacion[request.args(1)]
	db.actividades.cod_asig.writable=False
	db.actividades.cod_asig.readable=False

	#session.flash='Asignacion id = '+str(asig.id)
	
	crud.settings.update_onaccept = calcula_porcentaje(asig)
	form=crud.update(db.actividades,actividad_reg.id,next=url('detalle_actividad'))
	form.element(_id='delete_record__row')['_class']='hidden' # To hide the "check to delete boolean"
	
	return dict(form=form, asignacion_id=asignacion_id)
	
@auth.requires_membership('ADMIN')
def list_detalle_act():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_custodios_bd_appl').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	asignaciones=db(db.asignacion.id>0).select(orderby=db.asignacion.id)
	actividades = db(db.actividades.id>0).select()
	todas=db(db.asignacion.id==db.actividades.cod_asig).select()
	return dict(asignaciones=asignaciones, actividades=actividades, todas=todas, script=script)

@auth.requires_membership('ADMIN')
def list_detalle_act2():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_custodios_bd_appl').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	asignaciones=db(db.asignacion.id>0).select(orderby=db.asignacion.id)
	actividades = db(db.actividades.id>0).select()
	todas=db(db.asignacion.id==db.actividades.cod_asig).select()
	return dict(asignaciones=asignaciones, actividades=actividades, todas=todas, script=script)
	
@auth.requires_membership('ADMIN')
def list_detalle_act3():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_custodios_bd_appl').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	asignaciones=db(db.asignacion.id>0).select(db.asignacion.id, db.asignacion.cod_proyecto,\
	db.asignacion.porc_completado, db.asignacion.horas_ejecutadas, db.asignacion.analista,distinct=True, orderby="asignacion.id")
	actividades = db(db.actividades.id>0).select()
	todas=db(db.asignacion.id==db.actividades.cod_asig).select()
	return dict(asignaciones=asignaciones, actividades=actividades, todas=todas, script=script)

@auth.requires_membership('ADMIN') 
def list_detalle_act4():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_detalle_act4').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	
	camposActividades = [
		###########################################
		# Asignacion
		INPUT(_name='desde', _type='date'),
		INPUT(_name='hasta', _type='date'),
	]

	formaOP = FORM(*camposActividades)
	if formaOP.accepts(request.vars,formname='formaOPHTML',  onvalidation=valida_fechas2, keepvalues=True):
		desde = request.vars.desde
		hasta = request.vars.hasta
		
		
		from datetime import datetime
		import os
		import xlwt
		import uuid
		from xlwt import Workbook #xlwt.Utils 
		#import rowcol_to_cell
		#from xlwt import *
	
		tmpfilename=os.path.join(request.folder,'private','example.xls')
	
		font0 = xlwt.Font()
		font0.name = 'Times New Roman'
		font0.colour_index = 2
		font0.bold = True

		style0 = xlwt.XFStyle()
		style0.font = font0

		style1 = xlwt.XFStyle()
		style1.num_format_str = 'DD-MM-YYYY'
	
		fnt = Font()
		fnt.name = 'Arial'
		fnt.colour_index = 4
		fnt.bold = True
		
		border = xlwt.Borders()  # Frame cells
		border.left = xlwt.Borders.THIN  # Left
		border.top = xlwt.Borders.THIN  # upper
		border.right = xlwt.Borders.THIN  # right
		border.bottom = xlwt.Borders.THIN  # lower
		border.left_colour = 0x40  # Border line color
		border.right_colour = 0x40
		border.top_colour = 0x40
		border.bottom_colour = 0x40
		
	
		pattern = xlwt.Pattern()
		pattern.pattern = xlwt.Pattern.SOLID_PATTERN
		pattern.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']
	
		encab = xlwt.easyxf('font: bold on; align: wrap on, vert center, horiz center')
		encab.borders = border
		encab.pattern = pattern
	
		style = XFStyle()
		style.font = fnt
		style.font.height = 180
		style.num_format_str = '#,##0'
		style.borders = border
	
		style2 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
		num_format_str='#,##0.00')
	
		texto = XFStyle()
		texto = xlwt.easyxf('align: wrap on, vert center, horiz left')
		#texto.alignment.wrap = 1
		texto.borders = border
		
		textoC = XFStyle()
		textoC = xlwt.easyxf('align: wrap on, vert center, horiz center')
		textoC.alignment.wrap = 1
		textoC.borders = border
		
		fecha = xlwt.easyxf('align: wrap on, vert center, horiz center')
		fecha.num_format_str = 'DD-MM-YYYY'
		fecha.borders = border
		
		hora = xlwt.easyxf('align: wrap on, vert center, horiz center',num_format_str='#,##0.00')
		hora.borders = border
	
		wb = xlwt.Workbook(encoding="utf-8",style_compression=0)
		ws = wb.add_sheet('Todas las Actividades')
		En = wb.add_sheet('En Curso', cell_overwrite_ok = True)
		Por = wb.add_sheet('Por Realizar')

		ws.normal_magn=110

		data = []
		act = ws.col(0)
		fec = ws.col(1)
		hor = ws.col(2)
		hor2 = ws.col(3)
		tipo = ws.col(4)
		ana = ws.col(5)
		# sec_col = worksheet.col(0)
		act.width = 1200*20
		fec.width = 150*20
		hor.width = 125*20
		hor2.width = 125*20
		tipo.width = 80*20
		ana.width = 300*20
		head = ['Actividades', 'Fecha', 'Hora de ejecución', 'Horas diurnas', 'Tipo', 'Analista']
		for index, value in enumerate(head):
			ws.write(0, index, value, encab)
		
		rows = db(db.actividades.cod_asig==db.asignacion.id)\
		(db.actividades.fecha_inicio >= desde)(db.actividades.fecha_inicio <= hasta)\
		(db.auth_user.id==db.asignacion.analista).\
		select(db.actividades.descripcion,db.actividades.fecha_inicio,db.actividades.hora_inicio,\
		db.actividades.horas_diurnas,db.actividades.tipo,(db.auth_user.first_name+' '+db.auth_user.last_name).with_alias("analista"), \
		orderby="analista, actividades.fecha_inicio, actividades.hora_inicio")

		row = 1
		col = 0
		
		for index, r in enumerate(rows):
			ws.row(index).height_mismatch = True
			ws.row(index).height = 50*20
			ws.set_panes_frozen(True) # frozen headings instead of split panes
			ws.set_horz_split_pos(1) # in general, freeze after last heading row
			ws.set_remove_splits(True)
			ws.write (row, 0, r.actividades.descripcion.replace('"',''), texto)
			ws.write (row, 1, r.actividades.fecha_inicio, fecha)
			ws.write (row, 2, r.actividades.hora_inicio, fecha)
			ws.write (row, 3, r.actividades.horas_diurnas, hora)
			ws.write (row, 4, r.actividades.tipo, textoC)
			ws.write (row, 5, r.analista, textoC)
			row +=1
			
		row +=2
		#ws.write(row, 2, 'Total Horas')
		#ws.write(row, 3, Formula("SUM($D$1:$D$100)"))
		#ws.write(row, 5, xlwt.Formula('= D{} - E[]'.format(row,  row)))
		
		# actividades en curso --------------------------------------
		
		act = En.col(0)
		ana = En.col(1)
		st = En.col(2)
		# sec_col = worksheet.col(0)
		act.width = 1200*20
		ana.width = 300*20
		st.width = 300*20
		
		head = ['Actividades en curso', 'Analista', 'Estatus']
		for index, value in enumerate(head):
			En.write(0, index, value, encab)
		
		
		
		#LISTA=['COMPLETADO']
		#(~db.proyectos.status.belongs(LISTA))
		
		rows=db(db.proyectos.descri!='ACTIVIDADES SEMANAL')(db.proyectos.id == db.asignacion.cod_proyecto)\
		(db.auth_user.id==db.asignacion.analista).select(db.proyectos.id, db.proyectos.descri,\
		db.proyectos.status,(db.auth_user.first_name+' '+db.auth_user.last_name).with_alias("analista"), \
		orderby="proyectos.descri,analista")
		row = 1
		id_proy=0
		grupo_analista=''
		analista_anterior=''
		for index, r in enumerate(rows):
			En.row(index).height_mismatch = True
			En.row(index).height = 50*20
			
			En.set_panes_frozen(True) # frozen headings instead of split panes
			En.set_horz_split_pos(1) # in general, freeze after last heading row
			En.set_remove_splits(True)
			
			if id_proy == r.proyectos.id:
				reg =db(db.proyectos.id == db.asignacion.cod_proyecto)\
				(db.auth_user.id==db.asignacion.analista)(db.proyectos.id == id_proy)\
				.select((db.auth_user.first_name+' '+db.auth_user.last_name).with_alias("analista"), orderby="proyectos.descri,analista")
				#grupo_analista='[ '
				for grupo in reg:
					grupo_analista += grupo.analista + ','
				
				#grupo_analista += ' ]'	
				En.write (row - 1, 1, grupo_analista , textoC)
				grupo_analista=''
			else:	
				En.write (row, 0, r.proyectos.descri, texto)
				En.write (row, 1, r.analista, textoC)
				En.write (row, 2, r.proyectos.status, textoC)
				analista_anterior=r.analista
				row +=1
	
			id_proy = r.proyectos.id
			
		
			
		#En.write(row+1, 2, "A3+B3")
		#En.write(row+1, 3, xlwt.Formula(sum(A1:A16)))
			
		# actividades por realizar
		act = Por.col(0)
		st = Por.col(1)
		# sec_col = worksheet.col(0)
		act.width = 1200*20
		st.width = 200*20
		head = ['Actividades por realizar', 'Estatus']
		for index, value in enumerate(head):
			Por.write(0, index, value, encab)
		
		#rows=db(db.proyectos.status == 'EN CURSO')(db.proyectos.descri!='ACTIVIDADES SEMANAL')(db.proyectos.id == db.asignacion.cod_proyecto)\
		rows=db(db.proyectos.status == 'POR REALIZAR').select(orderby="descri")
		
		row = 1
		col = 0
		
		for index, r in enumerate(rows):
			Por.row(index).height_mismatch = True
			Por.row(index).height = 50*20
			Por.set_panes_frozen(True) # frozen headings instead of split panes
			Por.set_horz_split_pos(1) # in general, freeze after last heading row
			Por.set_remove_splits(True)
			Por.write (row, 0, r.descri, texto)
			Por.write (row, 1, r.status, textoC)
			row +=1
			
		nombre=db.auth_user[me]
		from datetime import datetime
		fecha=convert_date(hasta)
		
			
		#ws.write(row, 2, xlwt.Formula("sum(D$)"))
		#ws.write(row, 0, Formula("SUM(R[C:R[-1]C)"))
			
		response.headers['Content-Type']='application/vnd.ms-excel'
		response.headers['Content-disposition'] = 'attachment; filename=TODAS LAS ACTIVIDADES - %s - GL DyA.xls' % (fecha) 
		wb.save(tmpfilename)
		data = open(tmpfilename,"rb").read()
		os.unlink(tmpfilename)
			
		return data
	
	
	
	asignaciones=db(db.asignacion.id>0).select(db.asignacion.id, db.asignacion.cod_proyecto,\
	db.asignacion.porc_completado, db.asignacion.horas_ejecutadas, db.asignacion.analista,distinct=True, orderby="asignacion.analista")
	actividades = db(db.actividades.id>0).select(orderby="actividades.fecha_inicio")
	todas=db(db.asignacion.id==db.actividades.cod_asig).select()
	return locals()

def csvExport2(desde, hasta):
	scriptId = 'actividades'

	rows = db(db.actividades.cod_asig==db.asignacion.id)(db.asignacion.analista==me).\
	select(db.actividades.descripcion,db.actividades.fecha_inicio,db.actividades.hora_inicio,\
	db.actividades.horas_diurnas,db.actividades.tipo)
	if rows:
		session.flash = 'f1' 
	from gluon.contenttype import contenttype
	response.headers['Content-Type'] = contenttype('.csv')
	response.headers['Content-disposition'] = 'attachment; filename=export_%s.csv' % (scriptId) 

	import csv, cStringIO
	s = cStringIO.StringIO()
	rows.export_to_csv_file(s, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
	return s.getvalue()

def csvExport():
	scriptId = 'actividades'
	
	#rows = db(db.actividades.cod_asig==db.asignacion.id)(db.asignacion.analista==me)(db.actividades.fecha_inicio>=desde)(db.actividades.fecha_inicio<=hasta).\
	#select(db.actividades.descripcion,db.actividades.fecha_inicio,db.actividades.hora_inicio,\
	#db.actividades.horas_laboradas,db.actividades.tipo)
	
	rows = db(db.actividades.cod_asig==db.asignacion.id)(db.asignacion.analista==me).\
	select(db.actividades.descripcion,db.actividades.fecha_inicio,db.actividades.hora_inicio,\
	db.actividades.horas_laboradas,db.actividades.tipo)
	if rows:
		session.flash = 'f1' 
	from gluon.contenttype import contenttype
	response.headers['Content-Type'] = contenttype('.csv')
	response.headers['Content-disposition'] = 'attachment; filename=export_%s.csv' % (scriptId) 

	import csv, cStringIO
	s = cStringIO.StringIO()
	rows.export_to_csv_file(s, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
	#rows.export_to_csv_file(open(s, 'test.csv', 'w', encoding='latin1', newline=''))
	#rows.as_csv()
	return s.getvalue()

def csvExport_aut():
	
	scriptId = 'actividades'
		
	now = datetime.datetime.now()
	span = datetime.timedelta(days=0)
	dif= now-span
	hoy = now.strftime("%d-%m-%Y")
	nombre=None
	analista=None
	query = (db.actividades.cod_asig==db.asignacion.id)&(db.actividades.fecha_inicio==request.now.date())
	
	rows=db(query).select(db.asignacion.analista,db.actividades.descripcion,db.actividades.fecha_inicio,db.actividades.hora_inicio,\
	db.actividades.horas_laboradas,db.actividades.tipo, orderby='asignacion.analista')
	
	#---
	q=(db.asignacion.id>0)
	asig=db(q).select(db.asignacion.id)
	for a in asig:
		analista = a.id
		for act in db(db.actividades.cod_asig == a.id).select():
			analista=act
	#---
	
	
	for datos in rows:
		nombre=datos.asignacion.analista.first_name.upper()+' '+datos.asignacion.analista.last_name.upper()
		#nombre=db.auth_user[rows.analista].id
	
	import csv, cStringIO
	s = cStringIO.StringIO()
	rows.export_to_csv_file(s, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
	
	return locals()

def importCSV():
	file = r'/datos/actividad.csv'
	db.actividades_tmp.import_from_csv_file(open(file,'r'))
	db.commit
	return locals()
	
def reporte_actividades2():
	
	rows = db(db.actividades.cod_asig==db.asignacion.id)(db.asignacion.analista==me).\
	select(db.actividades.cod_asig, db.actividades.descripcion,db.actividades.fecha_inicio,db.actividades.hora_inicio,\
	db.actividades.horas_laboradas,db.actividades.tipo)
	detalle=[]
	detalle.append("<table id='reporte_actividades' class='TablaDetalles'>")
	for det  in rows:
		detalle.append("<tr>")
		detalle.append("<th></th>")
		detalle.append("</tr>")
		detalle.append("<tr>")
		detalle.append("<td class='Centrar '><input class='Estaticocm' name='productox' id='productox' type='text' value=' " +str(det.descripcion)+   "' readonly/></td>")
		detalle.append("<td class='Centrar '><input class='Estatico35cm' name='productox' id='productox' type='text' value=' " +str(det.fecha_inicio)+   "' readonly/></td>")
		detalle.append("<td class='Centrar '><input class='Estatico35cm' name='productox' id='productox' type='text' value=' " +str(det.hora_inicio)+   "' readonly/></td>")
		detalle.append("<td class='Centrar '><input class='Estatico35cm' name='productox' id='productox' type='text' value=' " +str(det.horas_laboradas)+   "' readonly/></td>")
		detalle.append("<td class='Centrar '><input class='Estatico35cm' name='productox' id='productox' type='text' value=' " +str(det.tipo)+   "' readonly/></td>")
		detalle.append("<td class='Centrar '><input class='Estatico35cm' name='productox' id='productox' type='text' value=' " +str(det.cod_asig.analista.first_name)+   "' readonly/></td>")
		detalle.append("</tr>")
	detalle.append("</table>")
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#reporte_actividades').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	r = (detalle)
	return r

@auth.requires_login()
def list_ambiente():
	form=SQLFORM.grid(db.ambiente, details=False, create=True,
	editable=True,deletable=False,searchable=False,
	csv = False,
	links_in_grid=False)
	db.ambiente.id.readable = False
	return dict(form=form)

@auth.requires_login()
def list_estados():
	form=SQLFORM.grid(db.estadobd, details=False, create=True,
	editable=True,deletable=False,searchable=False,
	csv = False,
	links_in_grid=False)
	db.estadobd.id.readable = False
	return dict(form=form)
	
@auth.requires_login()
def list_so():
	form=SQLFORM.smartgrid(db.so, details=False, create=True,editable=True,deletable=False,searchable=False,
	csv = False	)
	db.so.id.readable = False
	return dict(form=form)

	
@auth.requires_login()
def list_version():
	form=SQLFORM.smartgrid(db.ver, details=False, create=True,editable=True,deletable=False,searchable=False,
	csv = False)
	db.ver.id.readable = False
	return dict(form=form)

@auth.requires_login()
def list_custodios():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_servidores').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')

	form=SQLFORM.grid(db.custodios_appl, details=False, create=True,
	editable=True,deletable=True,searchable=True,
	fields=[db.custodios_appl.nombres,
							db.custodios_appl.cargo,
							db.custodios_appl.extension
							],
	maxtextlength = 100,
	csv = False,
	links_in_grid=False)
	db.custodios_appl.id.readable = False

	return dict(form=form, script=script)



@auth.requires_membership('ADMIN')
def edit_rutina_status():
	
	rutina_id=request.args(0)
	rutina=db.rutina_status[rutina_id]  or redirect(error_page)
	
	if not rutina.created_by==me: 
		crud.settings.update_deletable = False
	form=crud.update(db.rutina_status,rutina,next=url('list_rutina_status'))
	
	guarda_log_bdmon();

	h=db.executesql('select rutina, status from rutina_status;')	
	
	return dict(form=form,h=h)



@auth.requires_login()
@auth.requires_membership('DBA')
def list_basedatos():
	
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_basedatos').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	basedatos=[]
	servidor_id=request.args(0)
	session.servidor_aux=request.args(0)
	servidor=db.servidores[servidor_id]
	session.flash='Exito';
	if servidor:
		
		db.basedatos.servidor.default=servidor_id
		db.basedatos.servidor.writable=False
		db.basedatos.servidor.readable=False
		form=crud.create(db.basedatos)
		#basedatos=db(db.basedatos.servidor==servidor.id).select(cache=(cache.ram,120), cacheable=True)
		#basedatos=db(db.basedatos.servidor==servidor.id).select(cache=(cache.ram, -1))
		basedatos=db(db.basedatos.servidor==servidor.id).select()
		#if db._lastsql:
		#	session.flash='1ra vez o no almacenado en cache'
		#else:
		#	session.flash='En cache'
	else:
		basedatos=db(db.basedatos).select()
		#if db._lastsql:
		#	session.flash='1ra vez o no almacenado en cache'
		#else:
		#	session.flash='En cache'
		form=None
	return dict(servidor=servidor,basedatos=basedatos,form=form, script=script)

def export_to_csv():
	import gluon.contenttype
	tabla=request.args(0)
	response.headers['Content-Type'] = gluon.contenttype.contenttype('.csv')
	session.flash=tabla
	response.headers['Content-disposition'] = 'attachment; filename=' + tabla + '.csv'
	#query = (db.basedatos.id > 0)
	query = db[tabla]
	#query = '(db.'+ tabla + '.id > 0)'
	return str(db(query).select())


@auth.requires_login()
def list_matriz_respaldo():
	
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_matriz_respaldo').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	basedatos_id=request.args(0)
	servidor_id=request.args(1)
	basedato=db.basedatos[basedatos_id]
	session.flash= 'Exito';
	if basedato:
		
		db.matriz_respaldo.basedatos_id.default=basedatos_id
		db.matriz_respaldo.basedatos_id.writable=False
		db.matriz_respaldo.basedatos_id.readable=False
		
		db.matriz_respaldo.servidor_id.default=servidor_id
		db.matriz_respaldo.servidor_id.writable=False
		db.matriz_respaldo.servidor_id.readable=False

		form=crud.create(db.matriz_respaldo)
		matriz_respaldo=db(db.matriz_respaldo.basedatos_id==basedato.id)(db.matriz_respaldo.servidor_id==servidor_id).select()
	else:
		matriz_respaldo=db(db.matriz_respaldo).select()
			
		form=None
	return dict(basedato=basedato,matriz_respaldo=matriz_respaldo,form=form,  script=script)

@auth.requires_login()
def edit_matriz_respaldo():
	matriz_id=request.args(0)
	session.matriz_id = matriz_id
	matriz=db.matriz_respaldo[matriz_id] or redirect(error_page)
	session.basedatos_id = matriz.basedatos_id
	crud.settings.update_deletable = False
	#db.matriz_respaldo.basedatos_id.default=basedatos_id
	db.matriz_respaldo.basedatos_id.writable=False
	db.matriz_respaldo.basedatos_id.readable=False
		
	#db.matriz_respaldo.servidor_id.default=servidor_id
	db.matriz_respaldo.servidor_id.writable=False
	db.matriz_respaldo.servidor_id.readable=False
	form=crud.update(db.matriz_respaldo,matriz,next=url('edit_matriz_respaldo', args=matriz_id))
	return dict(form=form)

def list_matriz_politica_resp():
	form2 = SQLFORM.grid(db.per)
	
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_matriz_politica_resp').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	basedatos_id=request.args(0)
	session.basedatos_aux=request.args(0)
	basedato=db.basedatos[basedatos_id]
	session.flash='Exito';
	if basedato:
		
		db.matriz_politica_resp.servidor_id.default=basedato.servidor
		db.matriz_politica_resp.servidor_id.writable=False
		db.matriz_politica_resp.servidor_id.readable=False

		db.matriz_politica_resp.basedatos_id.default=basedatos_id
		db.matriz_politica_resp.basedatos_id.writable=False
		db.matriz_politica_resp.basedatos_id.readable=False
		form=crud.create(db.matriz_politica_resp)
		matriz_respaldo=db(db.matriz_politica_resp.basedatos_id==basedato.id).select()
	else:
		if session.basedatos_id:
			matriz_respaldo=db(db.matriz_politica_resp.basedatos_id==session.basedatos_id).select()
		else:	
			matriz_respaldo=db(db.matriz_politica_resp).select()
			
		form=form2
	return dict(basedato=basedato,matriz_respaldo=matriz_respaldo,form=form, script=script)

@auth.requires_login()
def edit_matriz_politica_resp():
	matriz_id=request.args(0)
	session.matriz_id = matriz_id

	db.matriz_politica_resp.servidor_id.writable=False
	db.matriz_politica_resp.servidor_id.readable=False

	db.matriz_politica_resp.basedatos_id.writable=False
	db.matriz_politica_resp.basedatos_id.readable=False

	matriz=db.matriz_politica_resp[matriz_id] or redirect(error_page)
	session.basedatos_id = matriz.basedatos_id
	form=crud.update(db.matriz_politica_resp,matriz,next=url('list_matriz_politica_resp'))
	return dict(form=form)


@auth.requires_login()
def list_basedatos_alter_user():
	servidor_id=request.args(0)
	session.servidor_aux=request.args(0)
	servidor=db.servidores[servidor_id]
	
	if servidor:
		db.basedatos.servidor.default=servidor_id
		db.basedatos.servidor.writable=False
		db.basedatos.servidor.readable=False
		form=crud.create(db.basedatos)
		basedatos=db(db.basedatos.servidor==servidor.id)(db.basedatos.permite_alter_user=='SI').select()
	else:
		form=None
		basedatos=db(db.basedatos.permite_alter_user=='SI').select()
	return dict(servidor=servidor,basedatos=basedatos,form=form)


@auth.requires_login()
def list_bd_online():
	form=None
	#query = (db.person.id==1)|((db.person.id==2)&(db.person.name=='Max'))
	#query = (db.person.id==db.friendship.person)&(db.dog.id==db.friendship.dog)
	#query = db.person.name.lower().like('m%')
	#query = db.person.id.belongs(('max','Max','MAX'))
	#query = db.person.birth.year()+1==2008
	#rows = db(query).select()
	basedatos=db(db.basedatos.id>0)(db.basedatos.home != '').\
	select(db.basedatos.id,db.basedatos.servidor,db.basedatos.tipobd_id, db.basedatos.nombre,\
	db.basedatos.ver_id,db.basedatos.puerto,db.basedatos.usuario,db.basedatos.clave,db.basedatos.home,
	db.basedatos.status_mon,
	orderby=db.basedatos.tipobd_id | db.basedatos.servidor)
	return dict(basedatos=basedatos,form=form)


@auth.requires_login() 
def lista_bd_servidores():
	form=None
	
	servidores=db(db.servidores.id>0).select()
	return dict(servidores=servidores, form=form)


@auth.requires_login()
def list_bd_online_grafica():
	form=None
	busqueda=False
	bd=db.basedatos
	form = SQLFORM.factory(
		Field('tiposo', requires =  IS_EMPTY_OR(IS_IN_DB(db,'so.id','%(descri)s'))),
		Field('servidor', 'string'),
		Field('tipobd', requires =  IS_EMPTY_OR(IS_IN_DB(db,'tipobd.id','%(descri)s'))),
		Field('base', 'string'),
		Field('mon', 'string', requires=IS_EMPTY_OR(IS_IN_SET(['SI','NO']))),
		formstyle='table3cols', #'inline',
		submit_button="Search",
		buttons=[   TAG.button(T('Search'), _type="submit", _class="btn btn-primary"),
					TAG.button(T('Limpiar'), _type="button", _class="btn btn-primary", _onClick="limpiar")
				,   TAG.button(T('Cancel'), _type="button",_onClick="parent.location='%s' ;return false" % URL('default', 'index'))
				 ])
		#TAG.button(T('Cancel'), _type="button",_onClick="parent.location='%s' ;return false" % URL('default', 'form_test'))
	if form.accepts(request.vars, session, keepvalues = True):
		busqueda=True
		# conservar los valores del form
		pass
	else:
		if form.errors:
			response.flash = "Hay errores en la consulta"
	def limpiar():
		form.vars.tiposo = 0
		form.vars.tipobd = 0
		form.vars.servidor = ""
		form.vars.base = ""
		form.vars.mon = ""
	
	tiposo = form.vars.tiposo
	tipobd = form.vars.tipobd
	servidores = form.vars.servidor
	bases = form.vars.base
	mon = form.vars.mon
	query = (bd.id>0)&(bd.servidor==db.servidores.id)
	
	if tiposo:
		query &= db.servidores.so_id == tiposo
	
	if tipobd:
		query &= db.basedatos.tipobd_id == tipobd
		#tipo=tipobd
	if servidores:
		query &= db.servidores.nombre.like("%%%s%%" % servidores)
	if bases:
		query &= db.basedatos.nombre.like("%%%s%%" % request.vars.base)
	if mon:
		query &= db.basedatos.status_mon == mon
	#bases = (db.basedatos.nombre.startswith(request.vars.base))
	msg=""
	if busqueda:
		basedatos=db(query).\
			select(db.basedatos.id,db.basedatos.servidor,db.basedatos.tipobd_id, db.basedatos.nombre,\
			db.basedatos.version_id,db.basedatos.puerto,db.basedatos.usuario,db.basedatos.clave,db.basedatos.home,
			db.basedatos.status_mon,
			orderby=db.servidores.so_id | db.servidores.nombre | db.basedatos.tipobd_id | db.basedatos.servidor)
		if len(basedatos):
			msg="No hay datos"
	else:
		basedatos=db(db.basedatos.id <=0).select()
		msg=""
	return dict(basedatos=basedatos,form=form, msg=msg)


@auth.requires_login()
def list_admin_basedatos():
	#form=crud.create(db.admin_basedatos)
	form=SQLFORM(db.admin_basedatos)  
	admin=db(db.admin_basedatos.id>0).select()
	return dict(admin=admin,form=form)


@auth.requires_login()
def list_esquemas():
	basedatos_id=request.args(0)
	basedatos=db.basedatos[basedatos_id]
	session.basedatos_id = basedatos_id
	session.servidor_id = basedatos.servidor
	if basedatos:
		db.esquemas.basedatos_id.default=basedatos_id
		db.esquemas.basedatos_id.writable=False
		db.esquemas.basedatos_id.readable=False
		form=crud.create(db.esquemas)
		esquemas=db(db.esquemas.basedatos_id==basedatos.id)\
			.select(orderby=db.esquemas.nombre, cacheable=True)
	else:
		form=None
		#esquemas=db(db.esquemas.id>0).select(orderby=db.esquemas.nombre, cache=(cache.ram,120), cacheable=True)
		esquemas=db(db.esquemas.id>0).select(orderby=db.esquemas.nombre)
	return dict(basedatos=basedatos,esquemas=esquemas,form=form)

@auth.requires_login()
def view_esquema():
	esquema_id=request.args(0)
	reg_esquema=db.esquemas[esquema_id] or redirect(error_page)
	return dict(reg_esquema=reg_esquema)

@auth.requires_login()
def edit_esquema():
	esquema_id=request.args(0)
	reg_esquema=db.esquemas[esquema_id] or redirect(error_page)
	crud.settings.update_deletable = True
	form=crud.update(db.esquemas,reg_esquema,next=url('view_esquema', args=reg_esquema.id))
	return dict(form=form)



@auth.requires_login()
def query_esquemas():
	query = (db.esquemas.basedatos_id == db.basedatos.id) & (db.basedatos.servidor == db.servidores.id)
	#query = (db.esquemas.basedatos_id == db.basedatos.id) 
	rows = db(query).select()
	#query = (db.person.id==1)|((db.person.id==2)&(db.person.name=='Max'))
	#query = (db.person.id==db.friendship.person)&(db.dog.id==db.friendship.dog)
	#query = db.person.name.lower().like('m%')
	#query = db.person.id.belongs(('max','Max','MAX'))
	#query = db.person.birth.year()+1==2008
	#rows = db(query).select()
	
	
	return dict(rows=rows)

#------------------------------------------------------------------------------------------------------

@auth.requires_login()
def list_custodios_bd_appl():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_custodios_bd_appl').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	basedatos_id=request.args(0)
	basedatos=db.basedatos[basedatos_id]
	if basedatos:
		db.custodios_bd_appl.basedatos_id.default=basedatos_id
		db.custodios_bd_appl.basedatos_id.writable=False
		db.custodios_bd_appl.basedatos_id.readable=False
		form=crud.create(db.custodios_bd_appl)
		custodios=db(db.custodios_bd_appl.basedatos_id==basedatos.id)\
			.select(orderby=db.custodios_bd_appl.basedatos_id, cacheable=True)
	else:
		form=None
		#esquemas=db(db.esquemas.id>0).select(orderby=db.esquemas.nombre, cache=(cache.ram,120), cacheable=True)
		custodios=db(db.custodios_bd_appl.id>0).select(orderby=db.custodios_bd_appl.basedatos_id)
	form2=crud.create(db.custodios_appl)
	return dict(basedatos=basedatos,custodios=custodios,form=form, form2=form2, script=script)


@auth.requires_login()
def view_custodio_bd_appl():
	custodio_id=request.args(0)
	reg_custodio=db.custodios_bd_appl[custodio_id] or redirect(error_page)
	return dict(reg_custodio=reg_custodio)

@auth.requires_login()
def edit_custodio_bd_appl():
	custodio_id=request.args(0)
	reg_custodio=db.custodios_bd_appl[custodio_id] or redirect(error_page)
	db.custodios_bd_appl.basedatos_id.writable=False
	db.custodios_bd_appl.basedatos_id.readable=True
	crud.settings.update_deletable = True
	form=crud.update(db.custodios_bd_appl,reg_custodio,next=url('list_custodios_bd_appl', args=reg_custodio.basedatos_id))
	return dict(form=form)



#------------------------------------------------------------------------------------------------------

@auth.requires_login()
def view_admin_basedatos():
	admin_bd_id=request.args(0)
	reg_admin_bd=db.admin_basedatos[admin_bd_id] or redirect(error_page)
	return dict(reg_admin_bd=reg_admin_bd)

@auth.requires_login()
def edit_admin_basedatos():
	admin_bd_id=request.args(0)
	reg_admin_bd=db.admin_basedatos[admin_bd_id] or redirect(error_page)
	crud.settings.update_deletable = True
	form=crud.update(db.admin_basedatos,reg_admin_bd,next=url('list_admin_basedatos'))
	return dict(form=form)


@auth.requires_login()
def edit_basedatos():
	basedatos_id=request.args(0)
	session.basedatos_id = basedatos_id
	basedatos=db.basedatos[basedatos_id] or redirect(error_page)
	session.servidor_id = basedatos.servidor
	#session.basedatos_recientes = add2(session.basedatos_recientes,basedatos)
	session.basedatos_recientes = add3(session.basedatos_recientes,basedatos)
	#db.basedatos.servidor.writable=False
	#db.basedatos.nombre.writable=False
	#db.basedatos.servidor.readable=False
	#if not basedatos.created_by==me: 
		#crud.settings.update_deletable = False
	form=crud.update(db.basedatos,basedatos,next=url('list_basedatos', session.servidor_aux))
	return dict(form=form)

@auth.requires_login()
def edit_cuentas_so():
	cuentas_so_id=request.args(0)
	cuentas_so=db.cuentas_so[cuentas_so_id] or redirect(error_page)
	session.servidor_id = cuentas_so.servidor_id
	form=crud.update(db.cuentas_so,cuentas_so,next=url('list_cuentas_so', session.servidor_id))
	return dict(form=form)

@auth.requires_login()
def list_cuentas_so():
	
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_cuentas_so').dataTable({"bStateSave": true,"sPaginationType": "full_numbers","iDisplayLength": 10});
	});''')
	
	servidor_id=request.args(0)
	session.servidor_aux=request.args(0)
	servidor=db.servidores[servidor_id]
	session.flash='Exito';
	if servidor:
		
		db.cuentas_so.servidor_id.default=servidor_id
		db.cuentas_so.servidor_id.writable=False
		db.cuentas_so.servidor_id.readable=False
		form=crud.create(db.cuentas_so)
		#basedatos=db(db.basedatos.servidor==servidor.id).select(cache=(cache.ram,120), cacheable=True)
		cuentas_so=db(db.cuentas_so.servidor_id==servidor.id).select()
	else:
		cuentas_so=db(db.cuentas_so).select()
			
		form=None
	return dict(servidor=servidor,cuentas_so=cuentas_so,form=form, script=script)


@auth.requires_login()
def Generar_clave():
	key=keygen()
	cuentas_so_id=request.args(0)
	cuentas_so=db.cuentas_so[cuentas_so_id] or redirect(error_page)
	session.servidor_id = cuentas_so.servidor_id
	response.flash=session.servidor_id
	db(db.cuentas_so.id == request.args(0)).update(clave_anterior = db.cuentas_so.clave)
	db(db.cuentas_so.id == request.args(0)).update(clave = key)
	db.commit()
	session.flash='Clave Generada con  exito!';
	#redirect(URL('default','list_cuentas_so', vars=dict(servidor=session.servidor_id)))
	redirect(URL('default','list_cuentas_so', args=session.servidor_id))
	#return locals()
	pass

@auth.requires_login()
def list_companies():
	form=crud.create(db.company)
	companies=db(db.company.id>0).select(orderby=db.company.name)
	return dict(companies=companies,form=form)

@auth.requires_login()
def view_company():
	company_id=request.args(0)
	company=db.company[company_id] or redirect(error_page)
	session.recent_companies = add(session.recent_companies,company)
	return dict(company=company)

@auth.requires_login()
def view_rutina_status():
	rutina_id=request.args(0)
	rutina=db.rutina_status[rutina_id] or redirect(error_page)
	return dict(rutina=rutina)


@auth.requires_login()
def edit_company():
	company_id=request.args(0)
	company=db.company[company_id]  or redirect(error_page)
	session.recent_companies = add(session.recent_companies,company)
	if not company.created_by==me: 
		crud.settings.update_deletable = False
	form=crud.update(db.company,company,next=url('list_companies'))
	return dict(form=form)
	
#------------------------------------------------------------
def options_widget(field,value,**kwargs):
	""" Use web2py's intelligence to set up the right HTML for the select field
	the widgets knows about the database model """
	w = SQLFORM.widgets.options.widget
	xml = w(field,value,**kwargs)
	return xml
	 
# there is no need to be so verbose. This works as well.
def options_widget(field,value,**kwargs):
	return SQLFORM.widgets.options.widget(field,value,**kwargs)
	 
def string_widget(field,value,**kwargs):
	return SQLFORM.widgets.string.widget(field,value,**kwargs)
	 
def boolean_widget(field,value,**kwargs):
	#be careful using this; checkboxes on forms are tricky. see notes below.
	return SQLFORM.widgets.boolean.widget(field,value,**kwargs)


def editable_grid():
	#process submitted form
	if len(request.post_vars) > 0:
		for key, value in request.post_vars.iteritems():   
			(field_name,sep,row_id) = key.partition('_row_') #name looks like home_state_row_99
			if row_id:
				db(db.person2.id == row_id).update(**{field_name:value})
	 
	# the name attribute is the method we know which row is involved
	
	db.person2.home_state.represent = lambda value,row:  options_widget(db.person2.home_state,value,
		**{'_name':'home_state_row_%s' % row.id})
		
	db.person2.first_name.represent = lambda value,row:  string_widget(db.person2.first_name,value,
		**{'_name':'first_name_row_%s' % row.id})
		
	db.person2.second_name.represent = lambda value,row:  string_widget(db.person2.second_name,value,
		**{'_name':'second_name_row_%s' % row.id})
	 
	#look out for the special way we deal with booleans: we provide a requires
	#db.person2.is_happy.requires = IS_IN_SET(['True','False'])
	#db.person2.is_happy.represent = lambda value,row:  options_widget(db.person2.is_happy,value,
	#	**{'_name':'is_happy_row_%s' % row.id})
	 
	grid = SQLFORM.grid(db.person2, maxtextlength = 40,  maxtextlengths={'person2.first_name':10},
		selectable= lambda ids : redirect(URL('default','editable_grid',vars=request._get_vars)),
		)  #preserving _get_vars means user goes back to same grid page, same sort options etc
	grid.elements(_type='checkbox',_name='records',replace=None)  #remove selectable's checkboxes
	return dict(grid=grid)


#-----------------------------------------------------------------------

#@auth.requires_membership('ADMIN')
auth.add_permission(1, 'edit', db.auth_user)
@auth.requires(auth.has_membership('ADMIN'))
@auth.requires_login()
def list_dba():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_dba').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	dbas=db(db.auth_user.id>0 and db.auth_user.username != 'otro').select()
	return dict(dbas=dbas, script=script)
	

auth.add_permission(1, 'edit', db.auth_user)
@auth.requires(auth.has_membership('ADMIN'))
@auth.requires_login()
def edit_dba():
	dba_id=request.args(0)
	create = auth.has_membership('ADMIN'),
	editable = auth.has_membership('ADMIN'),
	deletable = auth.has_membership('ADMIN'),
	dba=db.auth_user[dba_id] or redirect(error_page)
	form=crud.update(db.auth_user,dba, next=url('list_dba'))
	return dict(form=form)


@auth.requires_login()
def list_persons():
	company_id=request.args(0)
	company=db.company[company_id]
	if company:
		session.recent_companies = add(session.recent_companies,company)
		db.person.company.default=company_id
		db.person.company.writable=False
		db.person.company.readable=False
		form=crud.create(db.person)
		persons=db(db.person.company==company.id)\
			.select(orderby=db.person.name)
	else:
		form=None
		persons=db(db.person.id>0).select(orderby=db.person.name)
	return dict(company=company,persons=persons,form=form)

@auth.requires_login()
def view_person():
	person_id=request.args(0)
	person=db.person[person_id] or redirect(error_page)
	session.recent_persons = add(session.recent_persons,person)
	return dict(person=person)

@auth.requires_login()
def view_basedatos():
	basedatos_id=request.args(0)
	session.basedatos_id = basedatos_id
	basedatos=db.basedatos[basedatos_id] or redirect(error_page)
	session.servidor_id = basedatos.servidor
	session.basedatos_recientes = add3(session.basedatos_recientes,basedatos)
	#session.recent_persons = add(session.recent_persons,person)
	return dict(basedatos=basedatos)


@auth.requires_login()
def info_basedatos():
	basedatos_id=request.args(0)
	session.basedatos_id = basedatos_id
	basedatos=db.basedatos[basedatos_id] or redirect(error_page)
	return dict(basedatos=basedatos)

@auth.requires_login()
def info_custodios():
	basedatos_id=request.args(0)
	bd=db.basedatos[basedatos_id]
	custodios=db(db.custodios_bd_appl.basedatos_id==bd).select()
	return dict(custodios=custodios)

@auth.requires_login()
def info_appl():
	appl = crud.select(db.basedatos, fields=['nombre','appl'],
						 headers={'basedatos.nombre':'Nombre', 'basedatos.appl':'Appl'})
	#appl="1"
	return dict(appl=appl)

@auth.requires_login()
def view_documentos():
	documento_id=request.args(0)
	documento=db.documentos[documento_id] or redirect(error_page)
	#session.recent_persons = add(session.recent_persons,person)
	return dict(documento=documento)


@auth.requires_login()
def view_servidor():
	servidor_id=request.args(0)
	servidor=db.servidores[servidor_id] or redirect(error_page)
	session.servidores_recientes = add2(session.servidores_recientes,servidor)
	return dict(servidor=servidor)



@auth.requires_login()
def list_documentos():
	basedatos_id=request.args(0)
	session.basedatos_id = basedatos_id
	basedatos=db.basedatos[basedatos_id] or redirect(error_page)
	session.servidor_id = basedatos.servidor
	#session.recent_persons = add(session.recent_persons,person)
	db.documentos.basedatos.default=basedatos.id
	db.documentos.basedatos.writable=False
	db.documentos.basedatos.readable=False
	form=crud.create(db.documentos)
	docs=db(db.documentos.basedatos==basedatos.id).select(orderby=db.documentos.estructura)
	return dict(basedatos=basedatos,docs=docs,form=form)



@auth.requires_login()
def list_logs():
	person_id=request.args(0)
	person=db.auth_user[person_id] or redirect(error_page)
	#session.recent_persons = add(session.recent_persons,person)
	db.log.person.default=person.id
	db.log.person.writable=False
	db.log.person.readable=False
	form=crud.create(db.log)
	logs=db(db.log.person==person.id).select(orderby=~db.log.created_on)
	return dict(person=person,logs=logs,form=form)

@auth.requires_login()
def list_logs_basedatos():
	basedatos_id=request.args(0)
	session.basedatos_id = basedatos_id
	basedatos=db.basedatos[basedatos_id] or redirect(error_page)
	session.servidor_id = basedatos.servidor
	#session.bd=basedatos_id
	#session.recent_persons = add(session.recent_persons,person)
	db.log_basedatos.basedatos.default=basedatos.id
	db.log_basedatos.basedatos.writable=False
	db.log_basedatos.basedatos.readable=False
	form=crud.create(db.log_basedatos)
	logs=db(db.log_basedatos.basedatos==basedatos.id).select(orderby=~db.log_basedatos.created_on)
	return dict(basedatos=basedatos,logs=logs,form=form)


@auth.requires_login()
def edit_logs_basedatos():
	logs_id=request.args(0)
	logs_basedatos=db.log_basedatos[logs_id] or redirect(error_page)
	form=crud.update(db.log_basedatos,logs_basedatos, next=url('list_basedatos'))
	return dict(form=form)


@auth.requires_login()
def list_logs_cuentas_so():
	cuenta_so_id=request.args(0)
	session.cuenta_so_id = cuenta_so_id
	cuenta=db.cuentas_so[cuenta_so_id] or redirect(error_page)
 
	db.log_cuentas_so.cuenta_so_id.default=cuenta.id
	db.log_cuentas_so.cuenta_so_id.writable=False
	db.log_cuentas_so.cuenta_so_id.readable=False
	form=crud.create(db.log_cuentas_so)
	logs=db(db.log_cuentas_so.cuenta_so_id==cuenta.id).select(orderby=~db.log_cuentas_so.created_on)
	return dict(cuenta=cuenta,logs=logs,form=form)


@auth.requires_login()
def edit_logs_cuentas_so():
	logs_id=request.args(0)
	db.log_cuentas_so.cuenta_so_id.writable=False
	db.log_cuentas_so.cuenta_so_id.readable=False
	logs_cuentas_so=db.log_cuentas_so[logs_id] or redirect(error_page)
	form=crud.update(db.log_cuentas_so,logs_cuentas_so, next=url('list_logs_cuentas_so'))
	return dict(form=form)


@auth.requires_login()
def edit_person():
	person_id=request.args(0)
	person=db.person[person_id] or redirect(error_page)
	session.recent_persons = add(session.recent_persons,person)
	db.person.company.writable=False
	db.person.company.readable=False
	if not person.created_by==me: 
		crud.settings.update_deletable = False
	form=crud.update(db.person,person,next=url('list_persons',person_id))
	return dict(form=form)




@auth.requires_login()
def edit_documentos():
	documento_id=request.args(0)
	documento=db.documentos[documento_id]  or redirect(error_page)
	#session.recent_servidor = add(session.recent_servidor,servidor)
	db.documentos.basedatos.writable=False
	db.documentos.basedatos.readable=False
	if not documento.created_by==me: 
		crud.settings.update_deletable = False
	form=crud.update(db.documentos,documento,next=url('view_documentos',documento_id))
	return dict(form=form,basedatos=documento.basedatos)
	
@auth.requires_login()
def edit_task():
	task_id=request.args(0)
	task=db.task[task_id] or redirect(error_page)
	person=db.auth_user[task.person]
	db.task.person.writable=db.task.person.readable=False
	if not task.created_by==me: 
		crud.settings.update_deletable = False
	#form=crud.update(db.task,task,next='read_task/[id]')
	form=crud.update(db.task,task,next='list_dba')
	return dict(form=form, person=person)

@auth.requires_login()
def read_task():
	record = db.task(request.args(0)) or redirect(URL('error'))
	form=crud.read(db.task,record)
	return dict(form=form)


@auth.requires_login()
def view_task():
	task_id=request.args(0)
	task=db.task[task_id] or redirect(error_page)
	person=db.auth_user[task.person]
	db.task.person.writable=db.task.person.readable=False
	form=crud.read(db.task,task)
	return dict(form=form, person=person, task=task)

@auth.requires_login()
def list_tasks():
	dba_id=request.args(0)
	persona=db.auth_user[dba_id]
	db.task.title.represent = lambda title,row:\
		A(title,_href=URL('view_task',args=row.id))
	#session.flash='done!'+str(person_id)
	if dba_id:
		#session.flash='done!'
		tasks=db(db.task.persona==dba_id)\
			(db.task.created_by==me).select()
			#(db.task.created_by==auth.user.id)(db.task.start_time>=request.now).select()
	else:
		#session.flash='else!'
		#tasks=db(db.task.created_by==auth.user.id)(db.task.start_time<=request.now).select()
		tasks=db(db.task.created_by==me).select()
	db.task.persona.default=dba_id
	db.task.persona.writable=db.task.persona.readable=False
	form=crud.create(db.task,next='list_dba/[id]')
	return dict(tasks=tasks,persona=persona,form=form)

@auth.requires_login()
def calendar():
	
	dba_id=request.args(0)
	persona=db.auth_user[dba_id]
	if dba_id:
		tasks=db(db.task.persona==dba_id)\
			(db.task.created_by==me).select()
					#(db.task.created_by==auth.user.id).select()
				#(db.task.created_by==auth.user.id)(db.task.start_time>=request.now).select()
	else:
		#tasks=db(db.task.created_by==auth.user.id)(db.task.start_time<=request.now).select()
		#tasks=db(db.task.created_by==auth.user.id).select()
		tasks=db(db.task.created_by==me).select()
	guardias=db(db.guardias).select()
	return dict(tasks=tasks,persona=persona,guardias=guardias)



@auth.requires(auth.user and auth.user.email=='fd1968.1@gmail.com')
def reset():
	for table in db.tables:
		if table=='auth_user':
			db(db[table].email!='fd1968.1@gmail.com').delete()
		else:
			db(db[table].id>0).delete()
	session.flash='done!'
	redirect('index')

def envia_correox():
	task_id=request.args(0)
	tarea=db.task_guardias[task_id]
	#mail.send(tarea.created_by.email, #request.vars.email,
	#	'Message subject',
	#'<html>Plain text body of the message</html>')
	return locals()

def envia_correo():
	task_id=request.args(0)
	tarea=db.task_guardias[task_id]
	response.view = 'list_task_guardias.html'
	form = SQLFORM.factory(
	Field('Frist_Name',type='string',requires=IS_NOT_EMPTY(),label=T('Your First Name')),
	Field('Last_Name',type='string',requires=IS_NOT_EMPTY(), label=T('Your Last Name')),
	Field('email',type='string',requires=IS_EMAIL(), label=T('Your Email Address')),
	Field('body',type='list:string'),
	#Field('password',type='password',requires = [IS_STRONG()\
	#,CRYPT(key='sha512:thisisthekey')],label=T('password')),
	#Field('confirm_password',type='password',\
	#requires=IS_EQUAL_TO(request.vars.password),label=T('confirm-password')),
	Field('Gender',type='string', requires=IS_IN_SET(['male','female ']),label=T('Your Sex')))
	form.body=tarea.body
	if form.process().accepted:
		if mail:
			if mail.send(to=['duranfs@bdv.com'], subject='welcome', message='welcome to web2py'):
				response.flash = T('mail send successful')
			else :
				response.flash = T('mail not send')
		else :
			response.flash = T('unable o send mail')
	elif form.errors:
		response.flash = 'form error'
	return locals()



def error():
	return dict(message="Error algo esta equivocado o no hay datos")


#def login_upper(form):
#    form.vars.username = form.vars.username.upper()
#    return form

#auth.settings.login_onvalidation = login_upper
#auth.settings.profile_onvalidation = login_upper



def persona():
		import json
		# Select all the records, to show how
		# datatables.net paginates.
		# Rows can't be serialized because they contain a reference to
		# an open basedatos connection. Use as_list()
		# to serialize the query result.
		people = json.dumps(db(db.persona).select().as_list())
		# Convert to XML for DataTable
		return dict(results=XML(people))




def download():
	"""
	allows downloading of uploaded files
	http://..../[app]/default/download/[filename]
	"""
	return response.download(request,db)


def call():
	"""
	exposes services. for example:
	http://..../[app]/default/call/jsonrpc
	decorate with @services.jsonrpc the functions to expose
	supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
	"""
	session.forget()
	return service()


def editItem(item):
	item = db(db.bdmon.id==request.args(0)).select().first()
	
	if not item:
		session.flash = T("Item not found")
		redirect( URL('default','index') )
	
	form = SQLFORM(db.bdmon, item)#, deletable = auth.has_membership("delete_inventory"))
	
	if form.accepts(request.vars, session):
		response.flash = T("Item Edited")
		#db.item_log.insert(item=item.id, msg=T("Item Edited"))
	elif form.errors:
		response.flash = T("Form Has Errors, Item Not Edited")
	return dict(form=form)

@auth.requires_login() 
def hist_mon():
	rows = db(db.bdmon.f_corrida < request.now.date())\
	.select(db.bdmon.f_corrida, orderby=~db.bdmon.f_corrida,  distinct=True)
	return dict(rows=rows)

#consulta compleja ---------------------------------------------------------
#query = (db.person.id==1)|((db.person.id==2)&(db.person.name=='Max'))
#query = (db.person.id==db.friendship.person)&(db.dog.id==db.friendship.dog)
#query = db.person.name.lower().like('m%')
#query = db.person.id.belongs(('max','Max','MAX'))
#query = db.person.birth.year()+1==2008
#rows = db(query).select()
#---------------------------------------------------------------------------
# aggregate select
#rows=db(friends).select(db.person.name,db.dog.id.count(),groupby=db.dog.id)
#----------------------------------------------------------------------------
# import CSV
#db.person.import_from_csv_file(open(filename,'rb'))


#----  wiki ----------------------------------------------------
#----  wiki ----------------------------------------------------

def list_program():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_program').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	form=crud.create(db.program, message=T("Registro Creado"))
	programs=db(db.program).select()
	return dict(programs=programs, form=form, script=script)

@auth.requires_login()
def edit_program():
	program_id=request.args(0)
	programs=db.program[program_id]  or redirect(error_page)
	form=crud.update(db.program,programs,next=url('list_program'))
	return dict(form=form)




@auth.requires_login()
def program():
	#guardia_id=request.args(0)
	#guardias=db.t_guardias[guardia_id] or redirect(error_page)
	#    if not guardias.created_by==me: 
	#	crud.settings.update_deletable = False
	#form=crud.update(db.t_guardias,guardias,next=url('list_guardias'))
	
	program=db.program(request.args(0)) or redirect(URL('index'))
	db.learning_goal.program.default=program.id
	

	form=crud.update(db.learning_goal,request.args(1))
	rows=db(db.learning_goal).select()
	return dict(form=form,rows=rows,program=program)


@auth.requires_login()
def list_learning():
	program_id=request.args(0)
	programs=db.program[program_id] or redirect(error_page)
	
	db.learning_goal.program.default=programs.id
	form=crud.create(db.learning_goal)
	rows=db(db.learning_goal.program==programs.id).select()
	return dict(form=form,rows=rows,programs=programs)

@auth.requires_login()
def read_learning():
	record = db.learning_goal(request.args(0)) or redirect(URL('error'))
	form=crud.read(db.learning_goal,record)
	return dict(form=form)


@auth.requires_login()
def edit_learning():
	program_id=request.args(0)
	learning_id=request.args(1)
	learning=db.learning_goal[learning_id] or redirect(error_page)
	
	#session.flash='learning_id'
	
	#crud.messages.record_updated='Registro Actualizado'
	crud.messages.create_log='Registro %(id)s actualizado'

	#if not learning.created_by==me: 
	#	crud.settings.update_deletable = False
	form=crud.update(db.learning_goal,learning,next=url('list_program'))
	#form=crud.update(db.learning_goal,learning,next='list_learning', args=program_id)
	return dict(form=form)



def busqueda():
   form2,results = busqueda_dinamica(db.tipobd)
   return dict(form2 = form2,results = results)

def select_tipobd():
	tipobd = db(db.tipobd.ALL).select()
	return dict(tipobd=tipobd)


def reporte_servidores():
	ambiente=db(db.ambiente.id>0).select()
	return dict(servidor = db(db.servidores.id > 0).select(orderby=db.servidores.tipo_equipo|db.servidores.nombre), ambiente=ambiente )


def rep_novedades_pantalla():
	rows = db(db.task_guardias.id > 0).select()
	return dict(rows=rows)

@auth.requires_login() 
def rep_logs_basedatos_pantalla():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#rep_logs_basedatos_pantalla').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	#query = (db.log_basedatos.id>0)&(db.log_basedatos.basedatos==db.basedatos.id)
	rows = db(db.log_basedatos.id>0).select()
	return dict(rows=rows, script=script)

@auth.requires_login() 
def rep_logs_cuentas_so_pantalla():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#rep_logs_cuentas_so_pantalla').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	#query = (db.log_basedatos.id>0)&(db.log_basedatos.basedatos==db.basedatos.id)
	rows = db(db.log_cuentas_so.id>0).select()
	return dict(rows=rows, script=script)





def reporte_novedadesxx():
	id_elegido=request.vars.get('ID')
	if id_elegido:
		rows= db(db.task_guardias.id==id_elegido).select() 
	return dict(novedades=rows)
# ---- reporte pdf -----


def reporte_novedades_prueba():
	id_elegido=request.vars.get('ID')
	if id_elegido:
		
		querysql = (""" Select 
					first_name,
					title, 
					start_time,
					end_time, 
					duracion, body, solucion, username, extension
				from task_guardias, guardias, auth_user
				where  task_guardias.guardia_id = guardias.id
				and    guardias.f_quien_toca = auth_user.id and task_guardias.id = """ + id_elegido)
	else:
		querysql = (""" Select first_name,title, start_time,end_time, duracion,
				body,solucion
				from task_guardias, guardias, auth_user
				where  task_guardias.guardia_id = guardias.id
				and    guardias.f_quien_toca = auth_user.id """)
				
	response.title = "Reporte de Novedades"
	head = THEAD(TR(
			TH("NOMBRE",_width="15%"),
			TH("CORREO",_width="10%"),
			TH("EXTENSION",_width="12%"),
			TH("GRUPO BASE DE DATOS",_width="63%"),
			_bgcolor="#A0A0A0"))
	#head = THEAD(TR(TH("INFORMACION DE LA NOVEDAD",_width="100%", _bgcolor="#E0E0E0")))
	foot = TFOOT(TR(TH("PLATAFORMA MEDIA", _width="100%"), _bgcolor="#E0E0E0"))
	
	try:
		allissues = db.executesql(querysql)
	except: pass
	rows = []
	for issue in allissues:
		mycounter = []
		mycounter.append(issue)
		i = len(mycounter)
		col = i % 2 and "#F0F0F0" or "#FFFFFF"
		quien=issue[0].encode("latin_1","replace")[:20]
		user=issue[7].encode("latin_1","replace")[:10]
		extension=issue[8].encode("latin_1","replace")[:10]
		body=issue[5].encode("latin_1","replace")[:1000]
		rows.append(TR(TD(quien + '      ' +  user + '           ' + extension)))
	bod=[]
	for bod in body.split("\n"):
		rows.append(TR(bod))
	
	
		
			
			
		# make the table object
	body = TBODY(*rows)
	table = TABLE(*[head,foot, body],
		_border="1", _align="center", _width="100%" )
	
	if request.extension!="pdf":
		from gluon.contrib.pyfpdf import FPDF, HTMLMixin
		
		# define our FPDF class (move to modules if it is reused  frequently)
		class MyFPDF(FPDF, HTMLMixin):
			def header(self):
				self.set_font('Arial','B',10)
				self.cell(0,10, response.title.upper() ,1,0,'C')
				self.ln(20)
			   
			def footer(self):
				self.set_y(-15)
				self.set_font('Arial','I',8)
				txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
				self.cell(0,10,txt,0,0,'C')
				   
		pdf=MyFPDF()
		# first page:
		pdf.add_page()
		#pdf.write_html('<font size="12">' + str(HTML(table, sanitize=False)) + '</font>' )
		pdf.set_font('Arial','',10)
		pdf.write_html('<font size="10">' + table.xml().decode('utf-8') + '</font>' )
		#pdf.write_html(table.xml().decode('utf-8'))
		response.headers['Content-Type']='application/pdf'
		return  pdf.output(dest='S')
	else:
		# normal html view:
		return dict(novedades=table)



@auth.requires_login() 
def report():
	response.title = "Reporte de Novedades"
	head = THEAD(TR(TH("Quien Reporta",_width="20%"),
			TH("Titulo",_width="27%"),
			TH("Inicio",_width="22%"),
			TH("Fin",_width="22%"),
			TH("Duracion",_width="15%"),
			_bgcolor="#A0A0A0"))

	foot = TFOOT(TR(TH("PLATAFORMA MEDIA",_width="100%"), _bgcolor="#E0E0E0"))
	querysql = (""" Select first_name,title, start_time,end_time, duracion
			from task_guardias, guardias, auth_user
			where  task_guardias.guardia_id = guardias.id
			and    guardias.f_quien_toca = auth_user.id """)
	try:
		allissues = db.executesql(querysql)
	except: pass
	rows = []
	for issue in allissues:
		mycounter = []
		mycounter.append(issue)
		i = len(mycounter)
		col = i % 2 and "#F0F0F0" or "#FFFFFF"
		quien=issue[0].encode("latin_1","replace")[:20]
	rows.append(quien)

	# make the table object
	body = TBODY(*rows)
	table = TABLE(*[head,foot, body],
			_border="1", _align="center", _width="100%", _font="7px")

	if request.extension!="pdf":
		from gluon.contrib.pyfpdf import FPDF, HTMLMixin

		# define our FPDF class (move to modules if it is reused  frequently)
		class MyFPDF(FPDF, HTMLMixin):
			def header(self):
				self.set_font('Arial','B',10)
				self.cell(0,10, response.title ,1,0,'C')
				self.ln(20)
			   
			def footer(self):
				self.set_y(-15)
				self.set_font('Arial','I',8)
				txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
				self.cell(0,10,txt,0,0,'C')
				   
		pdf=MyFPDF()
		# first page:
		pdf.add_page()
		pdf.write_html(str(XML(table, sanitize=False)))
		response.headers['Content-Type']='application/pdf'
		return pdf.output(dest='S')
	else:
		# normal html view:
		return dict(table=table)



def reporte_novedades_old():
	id_elegido=request.vars.get('ID')
	if id_elegido:
		
		querysql = (""" Select 
					first_name,
					title, 
					start_time,
					end_time, 
					duracion, body, solucion
				from task_guardias, guardias, auth_user
				where  task_guardias.guardia_id = guardias.id
				and    guardias.f_quien_toca = auth_user.id and task_guardias.id = """ + id_elegido)
	else:
		querysql = (""" Select first_name,title, start_time,end_time, duracion,
				body,solucion
				from task_guardias, guardias, auth_user
				where  task_guardias.guardia_id = guardias.id
				and    guardias.f_quien_toca = auth_user.id """)
				
	response.title = "Reporte de Novedades"
	head = THEAD(TR(
			TH("Quien Reporta",_width="10%"),
			TH("Titulo",_width="18%"),
			TH("Inicio",_width="14%"),
			TH("Fin",_width="14%"),
			TH("Duracion",_width="6%"), 
			TH("",_width="60%"),
			_bgcolor="#A0A0A0"))
	head = THEAD(TR(TH("Descripcion",_width="100%", _bgcolor="#E0E0E0")))
	foot = TFOOT(TR(TH("PLARAFORMA MEDIA"), _bgcolor="#E0E0E0"))
	try:
		allissues = db.executesql(querysql)
	except: pass
	rows = []
	for issue in allissues:
		mycounter = []
		mycounter.append(issue)
		i = len(mycounter)
		col = i % 2 and "#F0F0F0" or "#FFFFFF"
		
		quien='Quien Reporta: ' + issue[0].encode("latin_1","replace")[:20]
		
		body=issue[5].encode("latin_1","replace")[:1000]
		solucion=issue[6].encode("latin_1","replace")[:1000]
		
		
		rows.append(TR(TD(quien), _align="center", _style="font-size: 14px;"))
		rows.append(TD('Titulo              : ' + issue[1]))
		rows.append(TD('Hora de Inicio : ' + str(issue[2])))
		rows.append(TD('Hora de Fin     : ' + str(issue[3])))
		rows.append(TD('Tiempo            : ' + str(issue[4])))
		rows.append(TD('--------------------------------------------- DETALLE DE LA NOVEDAD --------------------------------------------' ))
		
	for ds in body.split("\n"):
		rows.append(TD(ds))
		
	for ds in solucion.split("\n"):
		rows.append(TD(ds))
		
		# make the table object
	body = TBODY(*rows)
	table = TABLE(*[head,foot, body],
		_border="1", _align="center", _width="100%" )
	html = """
		<H1 align="center">html2fpdf</H1>
		<h2>Basic usage</h2>
		<p>You can now easily print text mixing different
		styles : <B>bold</B>, <I>italic</I>, <U>underlined</U>, or
		<B><I><U>all at once</U></I></B>!<BR>You can also insert links
		on text, such as <A HREF="http://www.fpdf.org">www.fpdf.org</A>,
		or on an image: click on the logo.<br>
		<center>
				<A HREF="http://www.fpdf.org">"Hola"</A>
		</center>
		<h3>Sample List</h3>
		<ul><li>option 1</li>
		<ol><li>option 2</li></ol>
		<li>option 3</li></ul>

		<table border="0" align="center" width="50%">
		<thead><tr><th width="30%">Header 1</th><th width="70%">header 2</th></tr></thead>
		<tbody>
		<tr><td>cell 1</td><td>cell 2</td></tr>
		<tr><td>cell 2</td><td>cell 3</td></tr>
		</tbody>
		</table>
		"""

	if request.extension!="pdf":
		from gluon.contrib.pyfpdf import FPDF, HTMLMixin
		
		# define our FPDF class (move to modules if it is reused  frequently)
		class MyFPDF(FPDF, HTMLMixin):
			def header(self):
				self.set_font('Arial','B',10)
				self.cell(0,10, response.title.upper() ,1,0,'C')
				self.ln(20)
			   
			def footer(self):
				self.set_y(-15)
				self.set_font('Arial','I',8)
				txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
				self.cell(0,10,txt,0,0,'C')
				   
		pdf=MyFPDF()
		# first page:
		pdf.add_page()
		
		pdf.set_font('Arial','',10)
		pdf.write_html('<font size="10">' + table.xml().decode('utf-8') + '</font>' )
		response.headers['Content-Type']='application/pdf'
		return  pdf.output(dest='S')
	else:
		# normal html view:
		return dict(novedades=table)



@auth.requires_login() 
def reporte_novedades():
	dt = str(request.now.date().strftime("%d-%b-%Y"))
	
	id_elegido=request.vars.get('ID')
	if id_elegido:
		
		querysql = (""" Select 
					first_name,
					title, 
					start_time,
					end_time, 
					duracion, body, solucion
				from task_guardias, guardias, auth_user
				where  task_guardias.guardia_id = guardias.id
				and    guardias.f_quien_toca = auth_user.id and task_guardias.id = """ + id_elegido)
	else:
		querysql = (""" Select first_name,title, start_time,end_time, duracion,
				body,solucion
				from task_guardias, guardias, auth_user
				where  task_guardias.guardia_id = guardias.id
				and    guardias.f_quien_toca = auth_user.id """)
				
	response.title = "Reporte de Novedades"
	head = THEAD(TR(TH("DescripciÃ³n",_width="100%", _bgcolor="#E0E0E0")))
	foot = TFOOT(TR(TH("FLATAFORMA MEDIA"), _bgcolor="#E0E0E0"))
	
	try:
		allissues = db.executesql(querysql)
	except: pass
	rows = []
	for i, issue in enumerate(allissues):
		mycounter = []
		mycounter.append(issue)
		col = i % 2 and "#F0F0F0" or "#FFFFFF"
		
		quien='Quien reporta : ' + str(issue[0].decode().encode('utf-8')[:200])
		body=issue[5].decode().encode('latin_1')[:1000]
		solucion=issue[6].decode().encode('utf-8')[:1000]
		
		rows.append(TR(TD(MARKMIN(str('####') + quien), _bgcolor="#F0F0F0"), _align="center", _style="font-size: 14px;"))
		rows.append(TD('Titulo              : ' + issue[1], _bgcolor="#FFFFFF"))
		rows.append(TD('Hora de Inicio : ' + str(issue[2]), _bgcolor="#F0F0F0"))
		rows.append(TD('Hora de Fin     : ' + str(issue[3]), _bgcolor="#FFFFFF"))
		rows.append(TD('Tiempo            : ' + str(issue[4]), _bgcolor="#F0F0F0"))
		rows.append(TD('------------------------------------------------- DETALLE DE LA NOVEDAD ------------------------------------------------' ))
		
	for i,body in enumerate(body.split("\n")):
		col = i % 2 and "#F0F0F0" or "#FFFFFF"
		rows.append(TR(MARKMIN(body), _bgcolor=col))
		
	for i,sol in enumerate(solucion.split("\n")):
		col = i % 2 and "#F0F0F0" or "#FFFFFF"
		rows.append(TR((MARKMIN(sol)),_bgcolor=col))
		
		# make the table object
	body = TBODY(*rows)
	table = TABLE(*[head,foot, body],
		_border="0", _align="center", _width="100%" )
	
	if request.extension!="pdf":
		from gluon.contrib.pyfpdf import FPDF, HTMLMixin
		import os
		
		# define our FPDF class (move to modules if it is reused  frequently)
		class MyFPDF(FPDF, HTMLMixin):
			def header(self):
				"""
				Header on each page
				"""
				# insert my logo
				logo = os.path.join(request.env.web2py_path, "applications", \
				request.folder , "static", "images",   "logo-banco-vnzla.png")
				self.image(logo, x=10, y=8, w=23)
				self.set_font('helvetica','',8)
				self.cell(0,5, 'Fecha: ' + dt  ,0,1,'R')
				self.set_font('helvetica','',10)
				self.cell(0,5, response.title.upper() ,0,1,'C')
				
				self.ln(2)
			   
			def footer(self):
				self.set_y(-15)
				self.set_font('helvetica','I',8)
				txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
				self.cell(0,10,txt,0,0,'C')
				   
		pdf=MyFPDF(format='letter')
		# first page:
		pdf.add_page()
		pdf.set_font("helvetica", size=7)
		pdf.write_html('<font size="12" >' + table.xml().decode('utf-8') + '</font>' )
		response.headers['Content-Type']='application/pdf'
		pdf.output("novedades.pdf")
		return  pdf.output(dest='S')
	else:
		# normal html view:
		return dict(novedades=table)


@auth.requires_login() 
def reporte_logs_basedatos():
	
	dt = str(request.now.date().strftime("%d-%b-%Y"))

	id_elegido=request.vars.get('ID')
	if id_elegido:
		
		querysql = (""" Select basedatos.nombre, body, auth_user.first_name||', '||auth_user.last_name,
						log_basedatos.created_on, servidores.nombre
						from log_basedatos, basedatos, auth_user, servidores
						where log_basedatos.basedatos = basedatos.id
						and   basedatos.servidor = servidores.id 
						and   log_basedatos.created_by = auth_user.id  
						and   log_basedatos.id = """ + id_elegido)
	else:
		querysql = (""" Select basedatos, body from log_basedatos
						""")
	response.title = "Reporte de logs de Base de Datos "
	head = THEAD(TR(TH("Resumen".decode("latin-1"),_width="100%", _bgcolor="#E0E0E0")))
	foot = TFOOT(TR(TH("PLATAFORMA MEDIA"), _bgcolor="#E0E0E0"))
	try:
		allissues = db.executesql(querysql)
	except: pass
	rows = []
	for i, issue in enumerate(allissues):
		
		col = i % 2 and "#F0F0F0" or "#FFFFFF"
		body=issue[1].encode("latin-1","replace")[:1000]
		rows.append(TD(MARKMIN('####CREADO POR      :  ' + str(issue[2]).encode("latin-1") + '  EL   '      + str(issue[3])),_bgcolor="#FFFFFF0"))
		rows.append(TD(MARKMIN('####BASE DE DATOS: '     + str(issue[0]) + '     SERVIDOR: '  + str(issue[4])),_bgcolor="#FFFFFF0"))
		
		rows.append(TD('-------------------------------------------------------------------------- DETALLE  --------------------------------------------------------------------------' ))
		
		for i,body in enumerate(body.split("\n")):
			col = i % 2 and "#F0F0F0" or "#FFFFFF"
			rows.append(TR(TD((body)), _bgcolor=col))
		
		# make the table object
	body = TBODY(*rows)
	table = TABLE(*[head,foot, body],
		_border="0", _align="center", _width="100%" )
	
	if request.extension!="pdf":
		from gluon.contrib.pyfpdf import FPDF, HTMLMixin
		import os
		# define our FPDF class (move to modules if it is reused  frequently)
		class MyFPDF(FPDF, HTMLMixin):
			def header(self):
				"""
				Header on each page
				"""
				logo = os.path.join(request.env.web2py_path, "applications", request.folder , "static", "images",   "logo-banco-vnzla.png")
				self.image(logo, x=10, y=8, w=23)
				self.set_font('helvetica','',8)
				self.cell(0,5, 'Fecha: ' + dt  ,0,1,'R')
				self.set_font('helvetica','',10)
				self.cell(0,5, response.title.upper() ,0,1,'C')
				
				self.ln(2)
			   
			def footer(self):
				self.set_y(-15)
				self.set_font('helvetica','I',8)
				txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
				self.cell(0,10,txt,0,0,'C')
				   
		pdf=MyFPDF(format='letter')
		# first page:
		pdf.add_page()
		pdf.set_font("helvetica", size=12)
		pdf.write_html('<font size="10" >' + table.xml().decode('latin-1').encode("utf-8") + '</font>' )
		response.headers['Content-Type']='application/pdf'
		pdf.output("novedades.pdf")
		return  pdf.output(dest='S')
	else:
		return dict(novedades=table)

#--------------------------------------------------------------------




#--------------------------------------------------------------------

"""
 Simple web2py controller to generate PDF documents with ReportLab.
 
 Author: H.C. v. Stockhausen <hc at vst.io>
 Date:   2012-10-14
 
 Also see http://www.reportlab.com
 
"""
 
#import cStringIO
 
#from reportlab.platypus.doctemplate import SimpleDocTemplate
#from reportlab.platypus import Paragraph, Spacer
#from reportlab.lib.styles import getSampleStyleSheet
#from reportlab.lib.units import inch
 
 
def generatex():
	"""
	To display the generated PDF in your browser go to:
	 http://.../<app>/<controller>/generate
	 
	To download it as hello.pdf, for example, instead, use:
	 http://.../<app>/<controller>/generate/hello.pdf
	"""
	
	styles = getSampleStyleSheet()
	story = [
		Paragraph("Hello World", styles['Heading1']),
		Paragraph("The quick brown fox", styles['Normal']),
		Spacer(1, 0.25*inch),
		Paragraph("jumps over the lazy dog.", styles['Normal'])]
	buffer = cStringIO.StringIO()   
	doc = SimpleDocTemplate(buffer)
	doc.build(story)
	pdf = buffer.getvalue()
	buffer.close()
   
	filename = request.args(0)
	if filename:
		header = {'Content-Disposition': 'attachment; filename=' + filename}
	else:
		header = {'Content-Type': 'application/pdf'}
	response.headers.update(header)
	return pdf

def generate():
	#from reportlab.platypus import *
	from reportlab.platypus.doctemplate import SimpleDocTemplate
	from reportlab.lib.styles import getSampleStyleSheet
	from reportlab.rl_config import defaultPageSize
	from reportlab.lib.units import inch, mm
	from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER,TA_JUSTIFY
	from reportlab.lib import colors
	from uuid import uuid4
	from cgi import escape
	import os

	title="This The Doc Title"

	heading="First Paragraph"

	styles=getSampleStyleSheet()

	tmpfilename=os.path.join(request.folder,'private',str(uuid4()))

	doc=SimpleDocTemplate(tmpfilename)
	story=[]
	story.append(Paragraph(escape(title),styles["Title"]))
	story.append(Paragraph(escape(heading),styles["Heading2"]))
	story.append(Paragraph(escape('text'),styles["Normal"]))
	story.append(Spacer(1,2*inch))
	doc.build(story)
	data=open(tmpfilename,"rb").read()
	os.unlink(tmpfilename)
	response.headers['Content-Type'] ='application/pdf'
	return data


	
# this is a helper in my controller
# it takes the divecentre (dc) record and the shopping cart
def confirmation_pdf(dc, cart):
	# Let's import the wrapper
	import pdf
	from pdf.theme import colors, DefaultTheme
	# and define a constant
	TABLE_WIDTH = 540 # this you cannot do in rLab which is why I wrote the helper initially

	# then let's extend the Default theme. I need more space so I redefine the margins
	# also I don't want tables, etc to break across pages (allowSplitting = False)
	# see http://www.reportlab.com/docs/reportlab-userguide.pdf
	class MyTheme(DefaultTheme):
		doc = {
			'leftMargin': 25,
			'rightMargin': 25,
			'topMargin': 20,
			'bottomMargin': 25,
			'allowSplitting': False
			}

	# let's create the doc and specify title and author
	doc = pdf.Pdf('Booking Confirmation', 'unlogged.co.uk')

	# now we apply our theme
	doc.set_theme(MyTheme)

	# time to add the logo at the top right
	logo_path = request.folder + 'static/unlogged/images/logo-2.png'
	doc.add_image(logo_path, 180, 67, pdf.RIGHT)

	# give me some space
	doc.add_spacer()

	# this header defaults to H1
	doc.add_header('Booking confirmation')

	# here's how to add a paragraph
	doc.add_paragraph("We are pleased to confirm your reservation with <b>%s</b>...")

	doc.add_spacer()

	# a subheader - H2
	doc.add_header("Divecenter details", pdf.H2)

	# as in pre-css days we wrap the address and the Google Map Image in a table
	# my wrapper module just reexposes the reportlab Paragraph and Table classes. 
	# See __init__.py in the source section below 
	address = pdf.Paragraph("""
		<b>%(name)s</b><br/>
		%(hotelname)s<br/>
		%(region)s<br/>
		%(name)s<br/>
		%(country)s<br/><br/>
		GPS: %(latitude)s, %(longitude)s<br/><br/>
		Tel: %(tel)s<br/>
		%(web)s<br/>
		""" % dc, MyTheme.paragraph) # when we use the Paragraph class directly we have to specify a
									# style. Here we a using one from the underlying DefaultTheme.

	# let's get the map image
	gps = "%(latitude)s,%(longitude)s" % dc
	gmap = pdf.Image("http://maps.google.com/maps/api/staticmap?center=" +
		gps + "&zoom=13&markers=color:orange|" + gps +
		"&size=250x150&sensor=false", 250,150)

	# and add both the address and the map wrapped in a table to our doc
	doc.add(pdf.Table([[address,gmap]], style=[('VALIGN', (0,0), (-1,-1), 'TOP')])) # UGLY inline stuff

	doc.add_spacer()

	doc.add_header('Diver details', pdf.H2)

	# let's move on to the divers table

	diver_table = [['Name', 'Qualification', 'Last dive']] # this is the header row 

	for diver in cart.get_divers():

		diver_table.append([diver.name, diver.qualification, diver.last_dive]) # these are the other rows

		doc.add_table(diver_table, TABLE_WIDTH)
	
	# all the rest I omitted here but you get the picture.

	# read the reportLab docs and the source below to figure out how to tewak things.

	# again, see http://www.reportlab.com/docs/reportlab-userguide.pdf

	# ...

	# ...
	return doc.render()
	
	
	
##Controller
def chart():
	datos_chart="[{name: 'Tablespace 90%', y: 12},{name: 'Export fail', y: 8},{name: 'Objects invalid', y: 12}]" #Change this dynamically
	datos_map={}
	datos_map["datos"]=datos_chart
	chart="""
	<script type="text/javascript">
	Highcharts.setOptions({
		lang:{
		downloadJPEG: "Download em imagem JPG",
		downloadPDF: "Download em documento PDF",
		downloadPNG: "Download em imagem PNG",
		downloadSVG: "Download em vetor SVG",
		loading: "Lendo...",
		noData: "no hay datos para mostrar",
		printChart: "Imprimir GrÃ¡fico",
		}
		});

			// Build the chart
			$('#chart').highcharts({
				chart: {
					plotBackgroundColor: null,
					plotBorderWidth: null,
					plotShadow: false,
					type: 'pie'
				},
				title: {
					text: 'Menu GrÃ¡fico'
	},
	tooltip: {
		pointFormat: '{series.name}: <b>{point.percentage:.1f}%%</b>'
	},
	plotOptions: {
		pie: {
			allowPointSelect: true,
			cursor: 'pointer',
			dataLabels: {
				enabled: false
			},
			showInLegend: true
		}
	},
	credits:{enabled:false},
	series: [{
		name: 'Porcentaje de fallas',
		colorByPoint: true,
			data: %(datos)s
			}]
		});
	</script>
	""" %datos_map
	return dict(chart=XML(chart))


#import calendar
import datetime
import json

def chart_bars():
	import calendar
	year = 2020
	month = 3
	dias_totales = calendar.monthrange(year, month)[1]
	# Esto genera todos los dÃ­as del mes de febrero como texto
	categorias = [datetime.date(year, month, day).strftime('%d/%m/%y') for day in range(1, dias_totales+1)]

	# Esto lo vamos a llenar mÃ¡s abajo 
	series = []
	mes = []
	
	
	# El query con los filtros que le apliques para Febrero 2016
	datos = db(db.bdmon.tx_rutina=='TRANS_DISTRIBUIDAS')(db.bdmon.tx_instancia.upper()=='INFI')(db.bdmon.f_corrida>='2020-01-01').\
	select(db.bdmon.f_corrida, db.bdmon.tx_instancia, db.bdmon.tx_resultado) 
	
	fecha = db(db.bdmon.f_corrida.year() == 2020).select(db.bdmon.f_corrida.month(), distinct=True,  groupby='bdmon.f_corrida')
	
	
	#select(db.bdmon.tx_instancia, db.bdmon.tx_resultado, groupby='bdmon.tx_instancia,bdmon.f_corrida,bdmon.tx_resultado') 

	datos_por_instancia = {}
	# Iteramos los registros para luego armar las series
	for dato in datos:
		instancia = dato.tx_instancia.upper()
		if dato.tx_instancia not in datos_por_instancia:
			# Inicializamos el usuario con 0 documentos en cada dÃ­a
			datos_por_instancia[instancia] = [0] * dias_totales
			# Aumentamos en 1 la cantidad de documentos
		#datos_por_instancia[instancia][dato.fecha_registro.day-1] += 1
		datos_por_instancia[instancia][dato.f_corrida.month-1] += 1

	# Hay que convertir los datos al formato aceptado para las series
	for instancia, cantidades in datos_por_instancia.items():
		series.append({
		'name': instancia, # Cesar
		'data': cantidades # [2, 0, 7, 0, ... 10, 2]
			})
	# Hay que convertir los datos al formato aceptado para las series
	series2=[dato.tx_resultado for dato in datos]
				
	#meses_chart="['Janeiro', 'Fevereiro', 'MarÃ§o']" #Change this dynamically
	dates = ["2018-01-01", "2019-01-07"]
	
	#meses_chart = [calendar.month_name[i] for i in range(1,13) ]
	meses_chart = [calendar.month_abbr[i] for i in range(1,13) ]
	
	datos_chart="[3.5, 4, 5]" #Change this dynamically
	
	
	
	title="Grafico de Parametros BD"
	stitle="web2py end highchats powered"
	
	datos_map={}
	#datos_map["datos"]=datos_chart
	
	datos_map["datos"]=series
	
	datos_map["meses"]=meses_chart
	
	#datos_map["meses"]="['Enero','Febrero','Marzo','Abril','Mayo']"
	datos_map["datos1"]="[100,200,100,30,40,100,1001]"
	
	#datos_map["datos1"]=series2
	
	#datos_map["datos2"]="[10,2,10,30,40]"
	
	datos_map['titulo']=title
	datos_map['subtitulo']=stitle
	chart="""
	<script type="text/javascript">
	Highcharts.setOptions({
		lang:{
		downloadJPEG: "Download en imagen JPG",
		downloadPDF: "Download en documento PDF",
		downloadPNG: "Download en imagen PNG",
		downloadSVG: "Download en vetor SVG",
		loading: "Leyendo...",
		noData: "Enviar datos para mostrar",
		printChart: "Imprimir GrÃ¡fico",
		}
		});

			// Build the chart
			$('#chart').highcharts({
		chart: {
			type: 'column'
		},
		title: {
			text: '%(titulo)s'
		},
		subtitle: {
			text: '%(subtitulo)s'
		},
		xAxis: {
			categories: %(meses)s,
			crosshair: true
		},
		yAxis: {
			min: 0,
			title: {
				text: 'Procesos en Ejecucion'
			}
		},
		tooltip: {
			headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
			pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
				'<td style="padding:0"><b> {point.y:.0f} </b></td></tr>',
			footerFormat: '</table>',
			shared: true,
			useHTML: true
		},
		plotOptions: {
			column: {
				pointPadding: 0.2,
				borderWidth: 0
			}
		},
		credits:{enabled:false},
		series: [{
			name: 'Parametro: Procesos',
			data: %(datos1)s

		}]
	});
	</script>
	""" %datos_map
	fecha=XML(fecha)
	#fecha=fecha.as_list()
	
	return dict(chart=XML(chart), fecha=fecha,meses_chart=meses_chart, serie=series2, datos=datos)


def chart_barsxx():
	year = 2019
	month = 2
	dias_totales = calendar.monthrange(year, month)[1]
	# Esto genera todos los dÃ­as del mes de febrero como texto
	categorias = [datetime.date(year, month, day).strftime('%d/%m/%y') for day in range(1, dias_totales+1)]

	# Esto lo vamos a llenar mÃ¡s abajo 
	series = []
	
	# El query con los filtros que le apliques para Febrero 2016
	datos = db(db.bdmon.tx_rutina=='TRANS_DISTRIBUIDAS')(db.bdmon.tx_instancia.upper()=='infi')(db.bdmon.f_corrida>='2020-01-01').\
	select(db.bdmon.f_corrida, db.bdmon.tx_instancia,  groupby='bdmon.f_corrida, bdmon.tx_instancia') 
	
	#select(db.bdmon.tx_instancia, db.bdmon.tx_resultado, groupby='bdmon.tx_instancia,bdmon.f_corrida,bdmon.tx_resultado') 

	datos_por_instancia = {}
	# Iteramos los registros para luego armar las series
	for dato in datos:
		instancia = dato.tx_instancia.upper()
		if dato.tx_instancia not in datos_por_instancia:
			# Inicializamos el usuario con 0 documentos en cada dÃ­a
			datos_por_instancia[instancia] = [0] * dias_totales
			# Aumentamos en 1 la cantidad de documentos
		#datos_por_instancia[instancia][dato.fecha_registro.day-1] += 1
		datos_por_instancia[instancia][dato.f_corrida.month-1] += 1

	# Hay que convertir los datos al formato aceptado para las series
	for instancia, cantidades in datos_por_instancia.items():
		series.append({
		'name': instancia, # Cesar
		'data': cantidades # [2, 0, 7, 0, ... 10, 2]
			})
		
	meses_chart="['Janeiro', 'Fevereiro', 'MarÃ§o']" #Change this dynamically
	dates = ["2018-01-01", "2019-01-07"]
	
	#meses_chart = [calendar.month_name[i] for i in range(1,13) ]
	meses_chart = [calendar.month_abbr[i] for i in range(1,13) ]
	
	datos_chart="[3.5, 4, 5]" #Change this dynamically
	title="Grafico de Parametros BD"
	stitle="web2py end highchats powered"
	datos_map={}
	datos_map["datos"]=datos_chart
	
	datos_map["datos"]=series
	
	datos_map["meses"]=meses_chart
	
	datos_map["meses"]="['Enero','Febrero','Marzo','Abril','Mayo']"
	datos_map["datos1"]="[100,200,100,30,40]"
	datos_map["datos2"]="[10,2,10,30,40]"
	
	datos_map['titulo']=title
	datos_map['subtitulo']=stitle
	chart="""
	<script type="text/javascript">
	Highcharts.setOptions({
		lang:{
		downloadJPEG: "Download en imagen JPG",
		downloadPDF: "Download en documento PDF",
		downloadPNG: "Download en imagen PNG",
		downloadSVG: "Download en vetor SVG",
		loading: "Leyendo...",
		noData: "Enviar datos para mostrar",
		printChart: "Imprimir GrÃ¡fico",
		}
		});

			// Build the chart
			$('#chart').highcharts({
		chart: {
			type: 'column'
		},
		title: {
			text: '%(titulo)s'
		},
		subtitle: {
			text: '%(subtitulo)s'
		},
		xAxis: {
			categories: %(meses)s,
			crosshair: true
		},
		yAxis: {
			min: 0,
			title: {
				text: 'Procesos en Ejecucion'
			}
		},
		tooltip: {
			headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
			pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
				'<td style="padding:0"><b>R$ {point.y:.1f} </b></td></tr>',
			footerFormat: '</table>',
			shared: true,
			useHTML: true
		},
		plotOptions: {
			column: {
				pointPadding: 0.2,
				borderWidth: 0
			}
		},
		credits:{enabled:false},
		series: [{
			name: 'Parametro: Procesos',
			data: %(datos1)s

		}]
	});
	</script>
	""" %datos_map
	return dict(chart=XML(chart))




def plot_pygal2():
	#Please serve pygal-tooltips.min.js from your local server: http://kozea.github.com/pygal.js/latest/pygal-tooltips.min.js
	response.files.append(URL('default','static/js/pygal-tooltips.min.js'))
	response.headers['Content-Type']='image/svg+xml'
	import pygal
	from pygal.style import CleanStyle    
	bar_chart = pygal.Bar(style=CleanStyle)                            # Then create a bar graph object
	bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])  # Add some values    
	return bar_chart.render()

def plot_pygal(): #crecimiento mensual con parametro
	import calendar
	import pygal
	from pygal.style import CleanStyle
	from pygal.style import Style
	from pygal import Config
	from pygal.style import DefaultStyle
	from pygal.style import RedBlueStyle
	basedatos_id=request.args(0)
	servidor_nombre=request.args(1) 
	basedato=db.basedatos[basedatos_id] or redirect(error_page)
	session.flash='BD id: %s' %basedatos_id;
	if basedato:
		datos = db(db.bdmon.tx_rutina=='CRECIMIENTO_BD')(db.bdmon.f_corrida>='2020-01-01')\
		(db.bdmon.tx_instancia.upper()==basedato.nombre.upper())\
		(db.bdmon.tx_servidor.upper()==servidor_nombre)\
		(db.bdmon.tx_resultado != '0')\
		.select(db.bdmon.tx_instancia, db.bdmon.f_corrida,  db.bdmon.tx_resultado, \
		orderby='bdmon.tx_instancia, bdmon.f_corrida' ) 
		
		
		#sum_bdmon=db.bdmon.n_resultado.sum()
		#datos=db().select(db.bdmon.tx_instancia, sum_bdmon, groupby = db.bdmon.tx_instancia)
		
	else:
		datos=None

	custom_style = Style(
		width=600,
		height=300, 
		spacing=50,
		margin=50,
		background='transparent',
		plot_background='transparent',
		foreground='#53E89B',
		foreground_strong='#53A0E8',
		foreground_subtle='#630C0D',
		opacity='.9',
		opacity_hover='.9',
		transition='400ms ease-in',
		colors=('#E853A0', '#E8537A', '#E95355', '#E87653', '#E89B53')
		)
	
	response.headers['Content-Type']='image/svg+xml'
	Config = pygal.Config()
	Config.js = ["http://localhost:8000/siapobd/static/js/svg.jquery.js",
				 "http://localhost:8000/siapobd/static/js/pygal-tooltips.min.js"]
	Config.tooltip_border_radius=10
	Config.show_legend = True
	Config.human_readable = True
	Config.fill = False
	Config.value_font_size = 7
	Config.print_values=False
	Config.print_values_position='top'
	Config.print_zeroes=False
	Config.include_x_axis=True
	Config.no_data_text='No hay datos'
	Config.style=CleanStyle#custom_style
	Config.print_labels=True
	Config.min_scale=6
	Config.max_scale=20
	Config.label_font_size=5
	Config.print_labels=True
	Config.font_family=None
	Config.value_colors=('white')
	bar_chart = pygal.Bar(Config)
	bar_chart.title = 'Crecimiento Mensual de la base de datos %s del servidor %s' % (basedato.nombre, servidor_nombre) 
	
	meses_chart = [calendar.month_abbr[i] for i in range(1,13) ]
	bar_chart.x_labels = map(str, (meses_chart))
	
	meses=12
	semanas=53
	dias=365
	datos_por_instancia = {}
	
		
	for dato in datos:
		instancia = dato.tx_instancia.upper()
		mes_aux = dato.f_corrida.month
		dia_aux = dato.f_corrida.day
		if instancia not in datos_por_instancia:
			datos_por_instancia[instancia] = [0] * meses
		datos_por_instancia[instancia][mes_aux-1] = int(dato.tx_resultado)
		I=+1
	
	#series2=[int(dato.tx_resultado) for dato in datos]
	#bar_chart.add(basedato.nombre,series2, dot=False)
	
	for instancia, cantidad in datos_por_instancia.items():
		bar_chart.add(instancia, cantidad, dot=False)
	bar_chart.value_formatter = lambda x: '%.2f MB' % x if x is not None else '0'	
	#bar_chart.add('line', [
		#0,
		#{'value': 12, 'label': 'Twelve'},
		#31,
		#{'value': 8, 'label': 'eight'},
		#28,
		#0
	#])
	#session.flash=series2
	return bar_chart.render()



def data_bdmon():
	import calendar
	import pygal
	from pygal.style import CleanStyle
	from pygal.style import Style
	from pygal import Config
	from pygal.style import DefaultStyle

	datos_por_instancia = {}
	series=[]
	
	now = datetime.datetime.now()
	span = datetime.timedelta(days=0)

	fecha_hoy = now.strftime("%m")
	response.headers['Content-Type']='image/svg+xml'
	Config = pygal.Config()
	Config.js = ["http://localhost:8000/siapobd/static/js/svg.jquery.js",
				"http://localhost:8000/siapobd/static/js/pygal-tooltips.min.js"]
	Config.tooltip_border_radius=10
	Config.show_legend = True
	Config.human_readable = True
	Config.fill = False
	Config.value_font_size = 7
	Config.print_values=True
	Config.print_values_position='top'
	Config.print_zeroes=False
	Config.include_x_axis=True
	Config.no_data_text='No hay datos'
	Config.style=CleanStyle#custom_style
	Config.print_labels=True
	Config.min_scale=6
	Config.max_scale=20
	Config.label_font_size=5
	Config.print_labels=True
	Config.font_family=None
	Config.value_colors=('blue')
	
	bar_chart = pygal.Pie(style=CleanStyle, fill=True, print_values=True,  
	value_formatter = lambda x: '%.0f MB' % x if x is not None else '0', interpolate='cubic')
	bar_chart.title = 'Crecimiento SEMANAL de las bases de datos '
	
	fecha_hoy = now.strftime("%m")
	semana = now.strftime("%W")
	
	#meses_chart = [calendar.month_abbr[i] for i in range(1,int(fecha_hoy)+2 ) ]
	meses_chart = [calendar.month_abbr[i] for i in range(1,13 ) ]
	
	semanas_chart = [sem for sem in range(1,int(semana)+1)]
	bar_chart.x_labels = map(str, (semanas_chart))
	
	datos = db(db.bdmon.tx_rutina=='CRECIMIENTO_BD')(db.bdmon.f_corrida>='2020-01-01')(db.bdmon.tx_resultado != '0')\
		.select(db.bdmon.tx_instancia, db.bdmon.f_corrida,  db.bdmon.tx_resultado, \
		orderby='bdmon.tx_instancia, bdmon.f_corrida') 
	
	
	mes_aux=0
	dia_aux=0
	sem_aux=0
	I=0
	fecha_hoy = now.strftime("%m")
	#datos_por_instancia[instancia] = [0] * meses	
	# Inicializamos el usuario con 0 documentos en cada dÃ­a
	meses=12
	semanas=int(semana)
	for dato in datos:
		instancia = dato.tx_instancia.upper()
		mes_aux = dato.f_corrida.month
		dia_aux = dato.f_corrida.day
		sem_aux = dato.f_corrida.strftime("%W")
		
		if instancia not in datos_por_instancia:
			datos_por_instancia[instancia] = [0] * int(semanas)
		datos_por_instancia[instancia][int(sem_aux)-1] = int(dato.tx_resultado)
		I=+1

	#datos_por_instancia['INFI'][0] = 100
	#datos_por_instancia['INFI'][1] = 200
	#datos_por_instancia['INFI'][2] = 300
	#datos_por_instancia['INFI'][3] = 400
	#datos_por_instancia['INFI'][4] = 500
	#datos_por_instancia['INFI'][5] = 600
	#datos_por_instancia['SIPA'][6] = 700

	for instancia, cantidad in datos_por_instancia.items():
		bar_chart.add(instancia, cantidad, dot=False)
		
	
	#bar_chart.add(series, dot=False)
	
	session.flash=datos_por_instancia
	session.flash=semana
	return bar_chart.render()


def g_crecimiento_diario():
	response.files.append(URL('default','static/js/pygal-tooltips.min.js'))  
	response.headers['Content-Type']='image/svg+xml'
	import calendar
	import pygal
	from pygal.style import CleanStyle
	from pygal.style import Style
	from pygal import Config
	from pygal.style import DefaultStyle
	
	year=datetime.datetime.now().year
	mes=datetime.datetime.now().month
	dias_totales = calendar.monthrange(year, mes)[1]
	# Esto genera todos los dÃ­as del mes actual
	categoria = [datetime.date(year, mes, day).strftime('%d') for day in range(1, dias_totales+1)]
	cantidad=len(categoria)
	
	datos_por_instancia = {}
	series=[]
	
	now = datetime.datetime.now()
	span = datetime.timedelta(days=0)
	
	dif= now-span

	fecha_hoy = now.strftime("%m")
	
	custom_style = Style(
		width=600,
		height=300, 
		spacing=50,
		margin=50,
		background='transparent',
		plot_background='transparent',
		foreground='1#53E89B',
		foreground_strong='red',#'#53A0E8',
		foreground_subtle='#630C0D',
		opacity='.10',
		opacity_hover='.9',
		transition='400ms ease-in',
		colors=('green','red','#E853A0', '#E8537A', '#E95355', '#E87653', '#E89B53')
		)
	Config = pygal.Config()
	Config.js = ["http://localhost:8000/nodos/static/js/svg.jquery.js",
				"http://localhost:8000/nodos/static/js/pygal-tooltips.min.js"]
	Config.tooltip_border_radius=10
	Config.explicit_size=True
	Config.width=1300
	Config.height=540
	Config.y_label='Dias'
	Config.show_y_labels=True
	Config.x_label='Dias'
	Config.show_x_labels=True
	Config.title_font_size=20
	Config.show_legend = True
	Config.human_readable = True
	Config.fill = True
	Config.value_font_size = 7
	#Config.print_values=True
	#Config.print_values_position='top'
	Config.print_zeroes=False
	#Config.include_x_axis=True
	Config.no_data_text='No hay datos'
	Config.style=custom_style #CleanStyle#
	Config.print_labels=True
	#Config.min_scale=6
	#Config.max_scale=20
	Config.label_font_size=15
	Config.print_labels=True
	Config.font_family='Arial'
	Config.value_colors=('red')
	
	bar_chart = pygal.StackedLine(Config, interpolate='cubic')
	#bar_chart = pygal.HorizontalBar(Config, interpolate='cubic')
	
	
	
	fecha_hoy = now.strftime("%m")

	bar_chart.x_labels = map(str, (categoria))
	
	basedatos_id=request.args(0)
	servidor_nombre=request.args(1) 
	basedato=db.basedatos[basedatos_id] or redirect(error_page)
	session.flash='BD id: %s' %basedatos_id;
	if basedato:
		datos = db(db.bdmon.tx_rutina=='CRECIMIENTO_BD')(db.bdmon.f_corrida>='2020-01-01')\
		(db.bdmon.tx_instancia.upper()==basedato.nombre.upper())\
		(db.bdmon.tx_servidor.upper()==servidor_nombre)\
		(db.bdmon.tx_resultado != '0')\
		.select(db.bdmon.tx_instancia, db.bdmon.f_corrida,  db.bdmon.tx_resultado, \
		orderby='bdmon.tx_instancia, bdmon.f_corrida', distinct=True ) 
	else:
		datos=None
	
	mes = now.strftime("%m")
	tipo="DIARIO"
	bar_chart.title = 'Crecimiento [%s] de la base de datos %s  mes %s,  ' % (tipo, basedato.nombre.upper(), mes)
	bar_chart.title =  bar_chart.title +  'fecha [ %s ]' % (now.strftime("%d-%m-%Y"))
	
	mes_aux=0
	dia_aux=0
	sem_aux=0
	fecha_hoy = now.strftime("%m")
	
	for dato in datos:
		instancia = dato.tx_instancia.upper()
		mes_aux = dato.f_corrida.month
		dia_aux = dato.f_corrida.strftime("%d")
		sem_aux = dato.f_corrida.strftime("%W")
		fecha = dato.f_corrida.strftime("%y%m%d")
		
		if instancia not in datos_por_instancia:
			datos_por_instancia[instancia] = [0] * int(cantidad)
			
		datos_por_instancia[instancia][int(dia_aux)-1] = int(dato.tx_resultado)

	for instancia, cantidad in datos_por_instancia.items():
		bar_chart.add(instancia, cantidad, dot=False)
	bar_chart.value_formatter = lambda x: '%.2f MB' % x if x is not None else '0'	
	session.flash=dia_aux
	return bar_chart.render()


def g_crecimiento_tbs():
	response.files.append(URL('default','static/js/pygal-tooltips.min.js'))  
	response.headers['Content-Type']='image/svg+xml'
	import calendar
	import pygal
	from pygal.style import CleanStyle
	from pygal.style import Style
	from pygal import Config
	from pygal.style import DefaultStyle
	
	year=datetime.datetime.now().year
	mes=datetime.datetime.now().month
	sem=datetime.datetime.now().weekday
	dias_totales = calendar.monthrange(year, mes)[1]
	
	# Esto genera todos los dÃ­as del mes actual
	categoria = [datetime.date(year, mes, day).strftime('%d') for day in range(1, dias_totales+1)]
	cantidad=len(categoria)
	
	datos_por_instancia = {}
	series=[]
	
	now = datetime.datetime.now()
	span = datetime.timedelta(days=0)
	
	dif= now-span

	fecha_hoy = now.strftime("%m")
	custom_style = Style(
		width=600,
		height=300, 
		spacing=50,
		margin=50,
		background='transparent',
		plot_background='transparent',
		foreground='1#53E89B',
		foreground_strong='red',#'#53A0E8',
		foreground_subtle='#630C0D',
		opacity='.10',
		opacity_hover='.9',
		transition='400ms ease-in',
		colors=('#E853A0', '#E8537A', '#E95355', '#E87653', '#E89B53')
		)
	Config = pygal.Config()
	Config.js = ["http://localhost:8000/nodos/static/js/svg.jquery.js",
				"http://localhost:8000/nodos/static/js/pygal-tooltips.min.js"]
	Config.tooltip_border_radius=10
	Config.explicit_size=True
	Config.width=1300
	Config.height=540
	Config.y_label='Dias'
	Config.show_y_labels=True
	Config.x_label='Dias'
	Config.show_x_labels=True
	Config.title_font_size=20
	Config.show_legend = True
	Config.human_readable = True
	Config.fill = False
	Config.value_font_size = 7
	#Config.print_values=True
	#Config.print_values_position='top'
	Config.print_zeroes=False
	#Config.include_x_axis=True
	Config.no_data_text='No hay datos'
	Config.style=custom_style #CleanStyle
	Config.print_labels=True
	#Config.min_scale=6
	#Config.max_scale=20
	Config.label_font_size=15
	Config.print_labels=True
	Config.font_family='Arial'
	Config.value_colors=('red')
	
	bar_chart = pygal.StackedLine(fill=True, interpolate='cubic', style=CleanStyle, ) #Bar(Config, interpolate='cubic')
	#bar_chart = pygal.HorizontalBar(Config, interpolate='cubic')
	
	
	
	fecha_hoy = now.strftime("%m")

	bar_chart.x_labels = map(str, (categoria))
	
	basedatos_id=request.args(0)
	servidor_nombre=request.args(1) 
	basedato=db.basedatos[basedatos_id] or redirect(error_page)
	session.flash='BD id: %s' %basedatos_id;
	if basedato:
		datos = db(db.bdmon.tx_rutina.like('TBS_%'))(db.bdmon.f_corrida>='2020-01-01')\
		(db.bdmon.tx_instancia.upper()==basedato.nombre.upper())\
		(db.bdmon.tx_servidor.upper()==servidor_nombre)\
		(db.bdmon.tx_resultado != '')\
		.select(db.bdmon.tx_instancia, db.bdmon.tx_rutina, db.bdmon.f_corrida,  \
		db.bdmon.tx_resultado,\
		db.bdmon.n_resultado, \
		orderby='bdmon.tx_instancia, bdmon.f_corrida', distinct=True ) 
	else:
		datos=None
	
	mes = now.strftime("%m")
	tipo="DIARIO"
	bar_chart.title = 'Crecimiento [%s] de tablespaces de la bd  %s  mes %s,  ' % (tipo, basedato.nombre.upper(), mes)
	bar_chart.title =  bar_chart.title +  'fecha [ %s ]' % (now.strftime("%d-%m-%Y"))
	
	mes_aux=0
	dia_aux=0
	sem_aux=0
	fecha_hoy = now.strftime("%m")
	
	for dato in datos:
		tbs = dato.tx_rutina.upper()
		mes_aux = dato.f_corrida.month
		dia_aux = dato.f_corrida.strftime("%d")
		sem_aux = dato.f_corrida.strftime("%W")
		fecha = dato.f_corrida.strftime("%y%m%d")
		
		if tbs not in datos_por_instancia:
			datos_por_instancia[tbs] = [0] * int(cantidad)
			
		datos_por_instancia[tbs][int(dia_aux)-1] = int(dato.tx_resultado)

	for tbs, cantidad in datos_por_instancia.items():
		bar_chart.add(tbs, cantidad, dot=False)
	bar_chart.value_formatter = lambda x: '%.2f MB' % x if x is not None else '0'	
	session.flash=dia_aux
	return bar_chart.render()

#line_chart = pygal.Bar()
#line_chart.title = 'Browser usage evolution (in %)'
#line_chart.x_labels = map(str, range(2002, 2013))
#line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
#line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
#line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
#line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
#line_chart.value_formatter = lambda x: '%.2f%%' % x if x is not None else 'âˆ…'
#line_chart.render()


#xy_chart = pygal.XY(stroke=False)
#xy_chart.title = 'Correlation'
#xy_chart.add('A', [(0, 0), (.1, .2), (.3, .1), (.5, 1), (.8, .6), (1, 1.08), (1.3, 1.1), (2, 3.23), (2.43, 2)])
#xy_chart.add('B', [(.1, .15), (.12, .23), (.4, .3), (.6, .4), (.21, .21), (.5, .3), (.6, .8), (.7, .8)])
#xy_chart.add('C', [(.05, .01), (.13, .02), (1.5, 1.7), (1.52, 1.6), (1.8, 1.63), (1.5, 1.82), (1.7, 1.23), (2.1, 2.23), (2.3, 1.98)])
#xy_chart.add('Correl', [(0, 0), (2.8, 2.4)], stroke=True)
#xy_chart.render()


#chart = pygal.Line(title=u'Some different points')
#chart.x_labels = ('one', 'two', 'three')
#chart.add('line', [.0002, .0005, .00035])
#chart.add('other line', [1000, 2000, 7000], secondary=True)
#chart.render()


#line_chart = pygal.Bar()
#line_chart.title = 'Browser usage evolution (in %)'
#line_chart.x_labels = map(str, range(2002, 2013))
#line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
#line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
#line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
#line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
#line_chart.render()

#line_chart = pygal.HorizontalBar()
#line_chart.title = 'Browser usage in February 2012 (in %)'
#line_chart.add('IE', 19.5)
#line_chart.add('Firefox', 36.6)
#line_chart.add('Chrome', 36.3)
#line_chart.add('Safari', 4.5)
#line_chart.add('Opera', 2.3)
#line_chart.render()

#line_chart = pygal.StackedBar()
#line_chart.title = 'Browser usage evolution (in %)'
#line_chart.x_labels = map(str, range(2002, 2013))
#line_chart.add('Firefox', [None, None, 0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
#line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
#line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
#line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
#line_chart.render()

#chart = pygal.Line()
#chart.add('line', [.070106781, 1.414213562, 3.141592654])
#chart.value_formatter = lambda x: "%.2f" % x
#chart.render()

#chart = pygal.XY()
#chart.add('line', [(12, 31), (8, 28), (89, 12)])
#chart.x_value_formatter = lambda x:  '%s%%' % x
#chart.render()

def pie():
	import pygal
	response.headers['Content-Type']='image/svg+xml'
	pie_chart = pygal.Pie(width=400)
	pie_chart.title = 'Browser usage in February 2012 (in %)'
	pie_chart.add('IE', 39.5)
	pie_chart.add('Firefox', 26.6)
	pie_chart.add('Chrome', 26.3)
	pie_chart.add('Safari', 4.5)
	pie_chart.add('Opera', 2.3)
	return pie_chart.render()


def chart_pygal():
	#Please serve this file locally, download at: http://kozea.github.com/pygal.js/latest/pygal-tooltips.min.js
	response.files.append(URL('default','static/js/pygal-tooltips.min.js'))  
	response.headers['Content-Type']='image/svg+xml'
	import pygal
	from pygal.style import Style
 
	custom_style = Style(
		background='transparent',
		plot_background='transparent',
		foreground='#53E89B',
		foreground_strong='#53A0E8',
		foreground_subtle='#630C0D',
		opacity='.6',
		opacity_hover='.9',
		transition='400ms ease-in',
		colors=('#E853A0', '#E8537A', '#E95355', '#E87653', '#E89B53')
		)
 
	chart = pygal.StackedLine(fill=True, interpolate='cubic', style=custom_style, )
	chart.add('A', [1, 3,  5, 16, 13, 3,  7])
	chart.add('B', [5, 2,  3,  2,  5, 7, 17])
	chart.add('C', [6, 10, 9,  7,  3, 1,  0])
	chart.add('D', [2,  3, 5,  9, 12, 9,  5])
	chart.add('E', [7,  4, 2,  1,  2, 10, 0])
	chart.render()  
	return chart.render()


#------------------------------------------ base de datos graficos pantalla parametro -------------------
@auth.requires_login() 
def form_crecimiento_bd():
	querysql = (""" select serv.nombre
			from servidores serv order by 1""")

	basedatos = db(db.basedatos).select(db.basedatos.id, db.basedatos.nombre, db.basedatos.servidor, orderby=db.basedatos.nombre)#db.executesql(querysql)
	sz=len(basedatos)
	return dict(basedatos=basedatos,size=sz)

@auth.requires_login() 
def form_crecimiento_tbs():
	querysql = (""" select serv.nombre
			from servidores serv order by 1""")

	basedatos = db(db.basedatos).select(db.basedatos.id, db.basedatos.nombre, db.basedatos.servidor, orderby=db.basedatos.nombre)#db.executesql(querysql)
	sz=len(basedatos)
	return dict(basedatos=basedatos,size=sz)

@auth.requires_login() 
def form_dashboard():
	now = datetime.datetime.now()
	mon = mon = db(db.bdmon.f_corrida>=(now))  \
		.select(orderby=db.bdmon.tx_servidor|db.bdmon.tx_tipobd|db.bdmon.tx_puerto|db.bdmon.tx_instancia|db.bdmon.tx_rutina)	
	sz=len(mon)
	return dict(mon=mon,size=sz)


#---------------------------------------------Configurar Reportes----------------------------------------
@auth.requires_login() 
def rep_serv_respc():
	querysql = (""" select serv.nombre
			from servidores serv order by 1""")

	servidores = db(db.servidores).select(db.servidores.nombre, orderby=db.servidores.nombre)#db.executesql(querysql)
	sz=len(servidores)
	return dict(servidores=servidores,size=sz)
#--------------------------------------Obtener datos de configuracion de reporte servidor----------------------------------
@auth.requires_login() 
def rep_serv_conf():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#rep_serv_conf').dataTable({"sPaginationType": "full_numbers","autoWidth": true});
	});''')
	data=request.vars
	buff=[]
	servbuff=[]
	for b in data:
		if b=="ambiente" or b=="bdt" or b=="version" or b=="conexion" or b=="responsable" or b=="app" or b=="rac":
			buff.append(b)
		else:
			servbuff.append(data[b])
	if len(data)<=0:
		redirect(URL('rep_serv_respc'))
		
	if len(servbuff)<=0:
		redirect(URL('rep_serv_respc'))
		
		
	s=','.join(buff)
	sql="select"
	fr=" from"
	wh=" where"
	bset=set(buff)
	sql=sql+" serv.nombre, "
	fr=fr+" servidores serv,"
	if "ambiente" in bset:
		sql=sql+ " amb.descri,"
		fr=fr+" ambiente amb,"
		wh=wh+" amb.id=serv.ambiente_id and"
	if "conexion" in bset:
		sql=sql+ " serv.tipoconex,"
	if "bdt" in bset:
		sql=sql+ " bd.nombre,"
		fr=fr+" basedatos bd,"
		wh+=" bd.servidor=serv.id and"
	if "version" in bset:
		sql=sql+ " vers.descri,"
		fr=fr+""" "ver" vers,"""
		wh=wh+" bd.version_id=vers.id and"
	if "app" in bset and "bdt" not in bset:
		sql=sql+ " bd.appl,"
		fr=fr+" basedatos bd,"
		wh+=" bd.servidor=serv.id and"
	
	else:
		if "app" in bset and "bdt" in bset:
			sql=sql+ " bd.appl,"
			wh+=" bd.servidor=serv.id and"

	if "responsable" in bset:
		sql=sql+ " au.nombres"
		fr=fr+" custodios_appl au,"
		wh=wh+" bd.custodio_id=au.id and"
	
	if "version" in bset and "bdt" not in bset and "app" not in bset:
		fr=fr+" basedatos bd,"

	if "responsable" in bset and "bdt" not in bset and "version" not in bset and "app" not in bset:
		fr=fr+" basedatos bd,"
	if sql[-1:]==",":
		sql=sql[:-1]
	if fr[-1:]==",":
		fr=fr[:-1]
	whin=" serv.nombre in ("
	if len(servbuff)>0:
		for i in servbuff:
			whin=whin+" '"+i+"',"
		if whin[-1:]==",":
			whin=whin[:-1]
		whin=whin+")"
	sql=sql+fr+wh+whin
	sql=sql+" order by 1;"
	basedatos = db.executesql(sql)
	#response.flash = sql
	return dict(data=data,s=sql,basedato=basedatos,buff=buff,script=script,sql=sql)
#---------------------------------------generar reporte por servidores------------------------------------
@auth.requires_login() 
def reporte_serv_pdf():
	dt = str(request.now.date().strftime("%d-%b-%Y"))
	buff=request.vars.buff
	sql=request.vars.sql
	basedato=db.executesql(sql)
	letra="times"
	response.title = "Reporte de Servidores"
	if request.extension!="pdf":
		from gluon.contrib.pyfpdf import FPDF, HTMLMixin
		import os
		# define our FPDF class (move to modules if it is reused  frequently)
		class MyFPDF(FPDF, HTMLMixin):
			def header(self):
				"""
				Header on each page
				"""
				logo = os.path.join(request.env.web2py_path, "applications", request.folder , "static", "images", "logo-banco-vnzla.png")
				self.image(logo, x=6, y=8, w=23)
				self.set_font('helvetica','',8)
				self.cell(0,5, 'Fecha: ' + dt  ,0,1,'R')
				self.set_font('helvetica','',10)
				self.cell(0,5, response.title.upper() ,0,1,'C')
				self.ln(2)
			   
			def footer(self):
				self.set_y(-15)
				self.set_font('helvetica','I',10)
				   
		pdf=MyFPDF(format='letter')
		# first page:
		pdf.add_page()
		#pdf.set_auto_page_break(0)
		pdf.set_font(letra, size=6)
		epw = pdf.w - 2*pdf.l_margin
		sz=len(buff or 'vacio')
		col_width = epw/sz
		th = pdf.font_size
		cont=0
		max_w=175
		pdf.set_fill_color(179, 209, 255)
		pdf.cell(0.130*175, 2*th, "Servidor", border=1,fill=True)
		if "ambiente" in buff:
			pdf.cell(175*0.100, 2*th, "Ambiente", border=1,fill=True)
		if "conexion" in buff:
			pdf.cell(175*0.075, 2*th, "ConexiÃ³n".encode("latin_1"), border=1,fill=True)
		if "bdt" in buff:
			pdf.cell(175*0.10, 2*th, "BD", border=1,fill=True)
		if "version" in buff:
			pdf.cell(175*0.075, 2*th, "VersiÃ³n".encode("latin_1"), border=1,fill=True)
		if "app" in buff:
			pdf.cell(175*0.5, 2*th, "AplicaciÃ³n".encode("utf-8").decode("utf-8"), border=1,fill=True)
		if "responsable" in buff:
			pdf.cell(175*0.17, 2*th, "Responsable", border=1,fill=True)
		pdf.ln(2*th)
		fillcont=1
		servidor=""
		for row in basedato:

			if servidor != row[cont]:
				servidor=row[cont]
				pdf.ln(2*th)
			
			if fillcont%2==0:
				pdf.set_fill_color(200, 200, 200)
			else:
				pdf.set_fill_color(204, 204, 204)
	
			
				
			pdf.set_font(letra, size=7)
			pdf.cell(0.130*175, 2*th,row[cont], border=1,fill=False) #nombre servidor
			
				
			if "ambiente" in buff:
				cont+=1
				pdf.set_font(letra, size=5)
				pdf.cell(175*0.100, 2*th, str(row[cont]).encode("latin_1"), border=1,fill=True)
				
			if "conexion" in buff:
				cont+=1
				pdf.cell(175*0.075, 2*th, str(row[cont]), border=1,fill=True)
			pdf.set_font(letra, size=6)
			if "bdt" in buff:
				cont+=1
				pdf.cell(175*0.10, 2*th, str(row[cont]), border=1,fill=True)
			pdf.set_font(letra, size=7)
			if "version" in buff:
				cont+=1
				pdf.cell(175*0.075, 2*th, str(row[cont]), border=1,fill=True)
			pdf.set_font(letra, size=7)
			if "app" in buff:
				cont+=1
				pdf.cell(175*0.5, 2*th, str(row[cont]).encode("utf-8").decode("utf-8"), border=1,fill=True)
			pdf.set_font(letra, size=5)
			if "responsable" in buff:
				cont+=1
				pdf.cell(175*0.17, 2*th, str(row[cont]), border=1,fill=True)
				pdf.ln(2*th)
			cont=0
			fillcont+=1
			
			
				
				
		response.headers['Content-Type']='application/pdf'
		pdf.output("reporteservidores.pdf")
		return  pdf.output(dest='S')
	else:
		return dict()

#--------------------------------------------------------------------------------------------------------------------------

# def ckeditor():
	# form = SQLFORM.grid(db.per)
	# return dict(form=form)

####---------------   reporte a excel --------------------------------

def excel_report2():
	from datetime import datetime
	import os
	import xlwt
	import uuid

	tmpfilename=os.path.join(request.folder,'private',str(uuid.uuid4()))

	font0 = xlwt.Font()
	font0.name = 'Arial'
	font0.bold = True

	style0 = xlwt.XFStyle()
	style0.font = font0

	style1 = xlwt.XFStyle()
	style1.num_format_str = 'DD-MMMM-YYYY'

	wb = xlwt.Workbook()
	ws = wb.add_sheet('Sample report')

	ws.write(0, 0, 'Text here', style0)
	ws.write(0, 6, 'More text here', style0)
	ws.write(0, 7, datetime.now(), style1)

	wb.save(tmpfilename)

	data = open(tmpfilename,"rb").read()
	os.unlink(tmpfilename)
	response.headers['Content-Type']='application/vnd.ms-excel'
	return data


#---------------------------------------------------------------------
def excel_report():
	from datetime import datetime
	import os
	import xlwt
	import uuid
	from xlwt import Workbook #xlwt.Utils 
	#import rowcol_to_cell
	#from xlwt import *
	
	tmpfilename=os.path.join(request.folder,'private','example.xls')
	
	font0 = xlwt.Font()
	font0.name = 'Times New Roman'
	font0.colour_index = 2
	font0.bold = True

	style0 = xlwt.XFStyle()
	style0.font = font0

	style1 = xlwt.XFStyle()
	style1.num_format_str = 'DD-MM-YYYY'
	
	fnt = Font()
	fnt.name = 'Arial'
	fnt.colour_index = 4
	fnt.bold = True
		
	border = xlwt.Borders()  # Frame cells
	border.left = xlwt.Borders.THIN  # Left
	border.top = xlwt.Borders.THIN  # upper
	border.right = xlwt.Borders.THIN  # right
	border.bottom = xlwt.Borders.THIN  # lower
	border.left_colour = 0x40  # Border line color
	border.right_colour = 0x40
	border.top_colour = 0x40
	border.bottom_colour = 0x40
		
	
	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']
	
	encab = xlwt.easyxf('font: bold on; align: wrap on, vert center, horiz center')
	encab.borders = border
	encab.pattern = pattern
	
	style = XFStyle()
	style.font = fnt
	style.font.height = 180
	style.num_format_str = '#,##0'
	style.borders = border
	
	style2 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
	num_format_str='#,##0.00')
	
	texto = XFStyle()
	texto = xlwt.easyxf('align: wrap on, vert center, horiz left')
	#texto.alignment.wrap = 1
	texto.borders = border
		
	textoC = XFStyle()
	textoC = xlwt.easyxf('align: wrap on, vert center, horiz center')
	textoC.alignment.wrap = 1
	textoC.borders = border
		
	fecha = xlwt.easyxf('align: wrap on, vert center, horiz center')
	fecha.num_format_str = 'DD-MM-YYYY'
	fecha.borders = border
		
	hora = xlwt.easyxf('align: wrap on, vert center, horiz center',num_format_str='#,##0.00')
	hora.borders = border
	
	wb = xlwt.Workbook(encoding="utf-8",style_compression=0)
	ws = wb.add_sheet('Todas las Actividades')
	En = wb.add_sheet('En Curso')
	Por = wb.add_sheet('Por Realizar')

	ws.normal_magn=110

	data = []
	act = ws.col(0)
	fec = ws.col(1)
	hor = ws.col(2)
	hor2 = ws.col(3)
	tipo = ws.col(4)
	ana = ws.col(5)
	# sec_col = worksheet.col(0)
	act.width = 1200*20
	fec.width = 150*20
	hor.width = 125*20
	hor2.width = 125*20
	tipo.width = 80*20
	ana.width = 300*20
	head = ['Actividades', 'Fecha', 'Hora de ejecución', 'Horas diurnas', 'Tipo', 'Analista']
	for index, value in enumerate(head):
		ws.write(0, index, value, encab)
		
	rows = db(db.actividades.cod_asig==db.asignacion.id)\
	(db.auth_user.id==db.asignacion.analista)(db.auth_user.id==me).\
	select(db.actividades.descripcion,db.actividades.fecha_inicio,db.actividades.hora_inicio,\
	db.actividades.horas_laboradas,db.actividades.tipo,(db.auth_user.first_name+' '+db.auth_user.last_name).with_alias("analista"), \
	orderby="analista, actividades.fecha_inicio, actividades.hora_inicio" )


	row = 1
	col = 0
		
	for index, r in enumerate(rows):
		ws.row(index).height_mismatch = True
		ws.row(index).height = 50*20
		ws.set_panes_frozen(True) # frozen headings instead of split panes
		ws.set_horz_split_pos(1) # in general, freeze after last heading row
		ws.set_remove_splits(True)
		ws.write (row, 0, r.actividades.descripcion.replace('"',''), texto)
		ws.write (row, 1, r.actividades.fecha_inicio, fecha)
		ws.write (row, 2, r.actividades.hora_inicio, fecha)
		ws.write (row, 3, r.actividades.horas_laboradas, hora)
		ws.write (row, 4, r.actividades.tipo, textoC)
		ws.write (row, 5, r.analista, textoC)
		row +=1
			
	row +=2
	#ws.write(row, 2, 'Total Horas')
	#ws.write(row, 3, Formula("SUM($D$1:$D$100)"))
	#ws.write(row, 5, xlwt.Formula('= D{} - E[]'.format(row,  row)))
	
	# actividades en curso --------------------------------------
	act = En.col(0)
	ana = En.col(1)
	st = En.col(2)
	# sec_col = worksheet.col(0)
	act.width = 1200*20
	ana.width = 300*20
	st.width = 300*20
		
	head = ['Actividades en curso', 'Analista', 'Estatus']
	for index, value in enumerate(head):
		En.write(0, index, value, encab)
	
	#LISTA=['COMPLETADO']
	#(~db.proyectos.status.belongs(LISTA))
			
	rows=db(db.proyectos.descri!='ACTIVIDADES SEMANAL')(db.proyectos.id == db.asignacion.cod_proyecto)\
	(db.auth_user.id==me)(db.auth_user.id==db.asignacion.analista).select(db.proyectos.id, db.proyectos.descri,\
	db.proyectos.status,(db.auth_user.first_name+' '+db.auth_user.last_name).with_alias("analista"), \
	orderby="proyectos.descri,analista")
	row = 1
	id_proy=0
	grupo_analista=''
	analista_anterior=''
	for index, r in enumerate(rows):
		En.row(index).height_mismatch = True
		En.row(index).height = 50*20
		
		En.set_panes_frozen(True) # frozen headings instead of split panes
		En.set_horz_split_pos(1) # in general, freeze after last heading row
		En.set_remove_splits(True)
			
		if id_proy == r.proyectos.id:
			reg =db(db.proyectos.id == db.asignacion.cod_proyecto)\
			(db.auth_user.id==db.asignacion.analista)(db.proyectos.id == id_proy)\
			.select((db.auth_user.first_name+' '+db.auth_user.last_name).with_alias("analista"), orderby="proyectos.descri,analista")
			#grupo_analista='[ '
			for grupo in reg:
				grupo_analista += grupo.analista + ','
			
			#grupo_analista += ' ]'	
			En.write (row - 1, 1, grupo_analista , textoC)
			grupo_analista=''
		else:	
			En.write (row, 0, r.proyectos.descri, texto)
			En.write (row, 1, r.analista, textoC)
			En.write (row, 2, r.proyectos.status, textoC)
			analista_anterior=r.analista
			row +=1
	
		id_proy = r.proyectos.id
			
		
	
	#En.write(row+1, 2, "A3+B3")
	#En.write(row+1, 3, xlwt.Formula(sum(A1:A16)))
			
	# actividades por realizar
	act = Por.col(0)
	st = Por.col(1)
	# sec_col = worksheet.col(0)
	act.width = 1200*20
	st.width = 200*20
	head = ['Actividades por realizar', 'Estatus']
	for index, value in enumerate(head):
		Por.write(0, index, value, encab)
		
	#rows=db(db.proyectos.status == 'EN CURSO')(db.proyectos.descri!='ACTIVIDADES SEMANAL')(db.proyectos.id == db.asignacion.cod_proyecto)\
	rows=db(db.proyectos.status == 'POR REALIZAR').select(orderby="descri")
		
	row = 1
	col = 0
		
	for index, r in enumerate(rows):
		Por.row(index).height_mismatch = True
		Por.row(index).height = 50*20
		Por.set_panes_frozen(True) # frozen headings instead of split panes
		Por.set_horz_split_pos(1) # in general, freeze after last heading row
		Por.set_remove_splits(True)
		Por.write (row, 0, r.descri, texto)
		Por.write (row, 1, r.status, textoC)
		row +=1
		
	nombre=db.auth_user[me]
	from datetime import datetime
	#fecha=convert_date(hasta)
		
			
	#ws.write(row, 2, xlwt.Formula("sum(D$)"))
	#ws.write(row, 0, Formula("SUM(R[C:R[-1]C)"))
		
		
	response.headers['Content-Type']='application/vnd.ms-excel'
	response.headers['Content-disposition'] = 'attachment; filename=%s %s - GL DyA.xls' % (nombre.first_name.upper(), nombre.last_name.upper().decode('utf-8')) 
	wb.save(tmpfilename)
	data = open(tmpfilename,"rb").read()
	os.unlink(tmpfilename)

	return data


def excel_report_graca():
	# -*- coding: windows-1251 -*-
	# -*- coding: utf-8 -*-
	from datetime import datetime
	import os
	import xlwt
	import uuid
	from xlwt import Workbook #xlwt.Utils 
	#import rowcol_to_cell
	#from xlwt import *
	
	
	tmpfilename=os.path.join(request.folder,'private','example.xls')

	
	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']

	
	font0 = xlwt.Font()
	font0.name = 'Times New Roman'
	font0.colour_index = 2
	font0.bold = True

	style0 = xlwt.XFStyle()
	style0.font = font0

	style1 = xlwt.XFStyle()
	style1.num_format_str = 'DD-MM-YYYY'
	
	fnt = Font()
	fnt.name = 'Arial'
	fnt.colour_index = 4
	fnt.bold = True
		
	border = xlwt.Borders()  # Frame cells
	border.left = xlwt.Borders.THIN  # Left
	border.top = xlwt.Borders.THIN  # upper
	border.right = xlwt.Borders.THIN  # right
	border.bottom = xlwt.Borders.THIN  # lower
	border.left_colour = 0x40  # Border line color
	border.right_colour = 0x40
	border.top_colour = 0x40
	border.bottom_colour = 0x40
		
	
	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']
	
	encab = xlwt.easyxf('font: bold on; align: wrap on, vert center, horiz center')
	encab.borders = border
	encab.pattern = pattern
	
	style = XFStyle()
	style.font = fnt
	style.font.height = 180
	style.num_format_str = '#,##0'
	style.borders = border
	
	style2 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
	num_format_str='#,##0.00')
	
	texto = XFStyle()
	texto = xlwt.easyxf('align: wrap on, vert center, horiz left')
	texto.alignment.wrap = 1
	texto.borders = border
	
		
	textoC = XFStyle()
	textoC = xlwt.easyxf('align: wrap on, vert center, horiz center')
	textoC.alignment.wrap = 1
	textoC.borders = border
		
	fecha = xlwt.easyxf('align: wrap on, vert center, horiz center')
	fecha.num_format_str = 'DD-MM-YYYY'
	fecha.borders = border
		
	hora = xlwt.easyxf('align: wrap on, vert center, horiz center',num_format_str='#,##0.00')
	hora.borders = border

	wb = xlwt.Workbook(encoding="utf-8",style_compression=0)
	
	ws = wb.add_sheet('Actividades')
	En = wb.add_sheet('En Curso')
	Por = wb.add_sheet('Por Realizar')
	
	ws.normal_magn=110

	data = []

	fec = ws.col(0)
	hor = ws.col(1)
		
	tipo = ws.col(2)
	act = ws.col(3)
	# sec_col = worksheet.col(0)
	act.width = 650*20
	fec.width = 150*20
	hor.width = 125*20
	tipo.width = 80*20
		
	head = ['Fecha', 'Horas laboradas', 'Tipo', 'Actividad']
	for index, value in enumerate(head):
		ws.write(0, index, value, encab)
		
	rows = db(db.actividades.cod_asig==db.asignacion.id)\
	(db.auth_user.id==db.asignacion.analista)(db.auth_user.id==me).\
	select(db.actividades.descripcion,db.actividades.fecha_inicio,db.actividades.hora_inicio,\
	db.actividades.horas_laboradas,db.actividades.tipo,(db.auth_user.first_name+' '+db.auth_user.last_name).with_alias("analista"), \
	orderby="analista, actividades.fecha_inicio, actividades.hora_inicio" )

	row = 1
	col = 0
		
	for index, r in enumerate(rows):
		ws.row(index).height_mismatch = True
		ws.row(index).height = 40*20
		
		ws.write (row, 0, r.actividades.fecha_inicio, fecha)
		
		ws.write (row, 1, r.actividades.horas_laboradas, hora)
		ws.write (row, 2, r.actividades.tipo, textoC)
		
		ws.write (row, 3, r.actividades.descripcion, texto)
		row +=1
	row +=2	
	nombre=db.auth_user[me]
	from datetime import datetime
	now = datetime.now()
	fecha = now.strftime("%d%m%Y")
	#fecha=convert_date("2020-11-03")
	
	# actividades en curso
	act = En.col(0)
	ana = En.col(1)
	st = En.col(2)
	# sec_col = worksheet.col(0)
	act.width = 1200*20
	ana.width = 300*20
	st.width = 200*20
	head = ['Actividades en curso', 'Analista', 'Estatus']
	for index, value in enumerate(head):
		En.write(0, index, value, encab)
		
	rows=db(db.proyectos.status == 'EN CURSO')(db.proyectos.descri!='ACTIVIDADES SEMANAL')(db.proyectos.id == db.asignacion.cod_proyecto)\
	(db.auth_user.id==db.asignacion.analista).select(db.proyectos.descri,\
	db.proyectos.status,(db.auth_user.first_name+' '+db.auth_user.last_name).with_alias("analista"), \
	orderby="proyectos.descri,analista")
	row = 1
	col = 0
		
	for index, r in enumerate(rows):
		En.row(index).height_mismatch = True
		En.row(index).height = 40*20
		En.write (row, 0, r.proyectos.descri, texto)
		En.write (row, 1, r.analista.upper(), textoC)
		En.write (row, 2, r.proyectos.status, textoC)
		row +=1
		
	# actividades por realizar
	
	
		
	response.headers['Content-Type']='application/vnd.ms-excel'
	response.headers['Content-disposition'] = 'attachment; filename=%s %s - %s - GL DyA.xls' % (nombre.first_name.upper(), nombre.last_name.upper().decode('utf-8'), fecha) 
	wb.save(tmpfilename)
	data = open(tmpfilename,"rb").read()
	os.unlink(tmpfilename)

	return data



#--------- list actividades formato graca

# ----- list actividades solutor delta

def excel_report_solutor():
	# -*- coding: windows-1251 -*-
	# -*- coding: utf-8 -*-
	from datetime import datetime
	import os
	import xlwt
	import uuid
	from xlwt import Workbook #xlwt.Utils 
	#import rowcol_to_cell
	#from xlwt import *
	
	
	tmpfilename=os.path.join(request.folder,'private','example.xls')

	
	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']

	
	font0 = xlwt.Font()
	font0.name = 'Times New Roman'
	font0.colour_index = 2
	font0.bold = True

	style0 = xlwt.XFStyle()
	style0.font = font0

	style1 = xlwt.XFStyle()
	style1.num_format_str = 'DD-MM-YYYY'
	
	fnt = Font()
	fnt.name = 'Arial'
	fnt.colour_index = 4
	fnt.bold = True
		
	border = xlwt.Borders()  # Frame cells
	border.left = xlwt.Borders.THIN  # Left
	border.top = xlwt.Borders.THIN  # upper
	border.right = xlwt.Borders.THIN  # right
	border.bottom = xlwt.Borders.THIN  # lower
	border.left_colour = 0x40  # Border line color
	border.right_colour = 0x40
	border.top_colour = 0x40
	border.bottom_colour = 0x40
		
	
	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']
	
	encab = xlwt.easyxf('font: bold on; align: wrap on, vert center, horiz center')
	encab.borders = border
	encab.pattern = pattern
	
	style = XFStyle()
	style.font = fnt
	style.font.height = 180
	style.num_format_str = '#,##0'
	style.borders = border
	
	style2 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
	num_format_str='#,##0.00')
	
	texto = XFStyle()
	texto = xlwt.easyxf('align: wrap on, vert center, horiz left')
	texto.alignment.wrap = 1
	texto.borders = border
	
		
	textoC = XFStyle()
	textoC = xlwt.easyxf('align: wrap on, vert center, horiz center')
	textoC.alignment.wrap = 1
	textoC.borders = border
		
	fecha = xlwt.easyxf('align: wrap on, vert center, horiz center')
	fecha.num_format_str = 'DD-MM-YYYY'
	fecha.borders = border
		
	hora = xlwt.easyxf('align: wrap on, vert center, horiz center',num_format_str='#,##0.00')
	hora.borders = border

	wb = xlwt.Workbook(encoding="utf-8",style_compression=0)
	
	ws = wb.add_sheet('Actividades')
	En = wb.add_sheet('En Curso')
	Por = wb.add_sheet('Por Realizar')
	
	ws.normal_magn=110

	data = []

	fec = ws.col(0)
	hor = ws.col(1)
		
	tipo = ws.col(2)
	act = ws.col(3)
	# sec_col = worksheet.col(0)
	act.width = 650*20
	fec.width = 150*20
	hor.width = 125*20
	tipo.width = 80*20
		
	head = ['Fecha', 'Hora desde', 'Hora hasta', 'Actividades']
	for index, value in enumerate(head):
		ws.write(0, index, value, encab)
		
	rows = db(db.actividades.cod_asig==db.asignacion.id)\
	(db.auth_user.id==db.asignacion.analista)(db.auth_user.id==me).\
	select(db.actividades.descripcion,db.actividades.fecha_inicio,db.actividades.hora_inicio,db.actividades.hora_fin,\
	db.actividades.horas_diurnas_r,db.actividades.horas_nocturnas_r,db.actividades.horas_diurnas,db.actividades.horas_nocturnas\
	,db.actividades.tipo,(db.auth_user.first_name+' '+db.auth_user.last_name).with_alias("analista"), \
	orderby="analista, actividades.fecha_inicio, actividades.hora_inicio" )

	row = 1
	col = 0
		
	for index, r in enumerate(rows):
		ws.row(index).height_mismatch = True
		ws.row(index).height = 40*20
		
		ws.write (row, 0, r.actividades.fecha_inicio, fecha)
		ws.write (row, 1, r.actividades.hora_inicio, hora)
		ws.write (row, 2, r.actividades.hora_fin, hora)
		ws.write (row, 3, r.actividades.descripcion, texto)
		row +=1
	row +=2	
	nombre=db.auth_user[me]
	from datetime import datetime
	now = datetime.now()
	fecha = now.strftime("%d%m%Y")
	#fecha=convert_date("2020-11-03")
	
	
		
	response.headers['Content-Type']='application/vnd.ms-excel'
	response.headers['Content-disposition'] = 'attachment; filename=%s %s - %s - GL DyA.xls' % (nombre.first_name.upper(), nombre.last_name.upper().decode('utf-8'), fecha) 
	wb.save(tmpfilename)
	data = open(tmpfilename,"rb").read()
	os.unlink(tmpfilename)

	return data
# --- fin format actividades solutor delta







@auth.requires_login()
def list_actividades_graca():
	me = auth.user_id
	actividades=''
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_actividades').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	#SafeLocale()
	
	ac = db.actividades
	actividades = [OPTION(actividad.id  ,_value=actividad.id) for actividad in
	db(ac.id>0).select(ac.ALL)]
	
	camposActividades = [
		###########################################
		# Asignacion
		INPUT(_name='desde', _type='date'),
		INPUT(_name='hasta', _type='date'),
	]

	formaOP = FORM(*camposActividades)
	if formaOP.accepts(request.vars,formname='formaOPHTML',  onvalidation=valida_fechas2, keepvalues=True):
		desde = request.vars.desde
		hasta = request.vars.hasta
		
		
		desde = request.vars.desde
		hasta = request.vars.hasta
		
		
		from datetime import datetime
		import os
		import xlwt
		import uuid
		from xlwt import Workbook #xlwt.Utils 
		#import rowcol_to_cell
		#from xlwt import *
	
		tmpfilename=os.path.join(request.folder,'private','example.xls')
	
		font0 = xlwt.Font()
		font0.name = 'Times New Roman'
		font0.colour_index = 2
		font0.bold = True

		style0 = xlwt.XFStyle()
		style0.font = font0

		style1 = xlwt.XFStyle()
		style1.num_format_str = 'DD-MM-YYYY'
	
		fnt = Font()
		fnt.name = 'Arial'
		fnt.colour_index = 4
		fnt.bold = True
		
		border = xlwt.Borders()  # Frame cells
		border.left = xlwt.Borders.THIN  # Left
		border.top = xlwt.Borders.THIN  # upper
		border.right = xlwt.Borders.THIN  # right
		border.bottom = xlwt.Borders.THIN  # lower
		border.left_colour = 0x40  # Border line color
		border.right_colour = 0x40
		border.top_colour = 0x40
		border.bottom_colour = 0x40
		
	
		pattern = xlwt.Pattern()
		pattern.pattern = xlwt.Pattern.SOLID_PATTERN
		pattern.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']
	
		encab = xlwt.easyxf('font: bold on; align: wrap on, vert center, horiz center')
		encab.borders = border
		encab.pattern = pattern
	
		style = XFStyle()
		style.font = fnt
		style.font.height = 180
		style.num_format_str = '#,##0'
		style.borders = border
	
		style2 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
		num_format_str='#,##0.00')
	
		texto = XFStyle()
		texto = xlwt.easyxf('align: wrap on, vert center, horiz left')
		texto.alignment.wrap = 1
		texto.borders = border
		
		textoC = XFStyle()
		textoC = xlwt.easyxf('align: wrap on, vert center, horiz center')
		textoC.alignment.wrap = 1
		textoC.borders = border
		
		fecha = xlwt.easyxf('align: wrap on, vert center, horiz center')
		fecha.num_format_str = 'DD-MM-YYYY'
		fecha.borders = border
		
		hora = xlwt.easyxf('align: wrap on, vert center, horiz center',num_format_str='#,##0.00')
		hora.borders = border
	
		wb = xlwt.Workbook(encoding="utf-8",style_compression=0)
		ws = wb.add_sheet('Actividades')

		ws.normal_magn=110

		data = []
		
		fec = ws.col(0)
		hor = ws.col(1)
		
		tipo = ws.col(2)
		act = ws.col(3)
		# sec_col = worksheet.col(0)
		act.width = 650*20
		fec.width = 150*20
		hor.width = 125*20
		tipo.width = 80*20
		
		head = ['Fecha', 'Horas laboradas', 'Tipo', 'Actividad']
		for index, value in enumerate(head):
			ws.write(0, index, value, encab)
		
		rows = db(db.actividades.cod_asig==db.asignacion.id)\
		(db.actividades.fecha_inicio >= desde)(db.actividades.fecha_inicio <= hasta)\
		(db.auth_user.id==db.asignacion.analista)(db.auth_user.id==me).\
		select(db.actividades.descripcion,db.actividades.fecha_inicio,db.actividades.hora_inicio,\
		db.actividades.horas_laboradas,db.actividades.tipo,(db.auth_user.first_name+' '+db.auth_user.last_name).with_alias("analista"), \
		orderby="actividades.fecha_inicio, actividades.hora_inicio, analista")

		row = 1
		col = 0
		
		for index, r in enumerate(rows):
			ws.row(index).height_mismatch = True
			ws.row(index).height = 40*20
			
			ws.write (row, 0, r.actividades.fecha_inicio, fecha)
			
			ws.write (row, 1, r.actividades.horas_diurnas_r, hora)
			ws.write (row, 2, r.actividades.tipo, textoC)
			
			ws.write (row, 3, r.actividades.descripcion, texto)
			row +=1
			
		row +=2
		#ws.write(row, 2, 'Total Horas')
		#ws.write(row, 3, Formula("SUM($D$1:$D$100)"))
		#ws.write(row, 5, xlwt.Formula('= D{} - E[]'.format(row,  row)))
		
		
		
		nombre=db.auth_user[me]
		from datetime import datetime
		fecha=convert_date(hasta)
		
			
		#ws.write(row, 2, xlwt.Formula("sum(D$)"))
		#ws.write(row, 0, Formula("SUM(R[C:R[-1]C)"))
			
		nombre=db.auth_user[me]
		from datetime import datetime
		fecha=convert_date(hasta)
		
		response.headers['Content-Type']='application/vnd.ms-excel'
		response.headers['Content-disposition'] = 'attachment; filename=%s %s - %s - GL DyA.xls' % (nombre.first_name.upper(), nombre.last_name.upper().decode('utf-8'), fecha) 
		wb.save(tmpfilename)
		data = open(tmpfilename,"rb").read()
		os.unlink(tmpfilename)
		return data
		
		
	elif formaOP.errors:
		response.flash = 'Fechas erradas'
	else:
		response.flash = 'Exito!'
		
	mis_actividades = db(db.actividades.id>0)(db.actividades.cod_asig==db.asignacion.id)(db.asignacion.analista==me).select()
	return locals()


#--------- fin list actividades formato graca

# -- list actividades solutor 
@auth.requires_login()
def list_actividades_solutor():
	me = auth.user_id
	actividades=''
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_actividades').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	#SafeLocale()
	
	ac = db.actividades
	actividades = [OPTION(actividad.id  ,_value=actividad.id) for actividad in
	db(ac.id>0).select(ac.ALL)]
	
	camposActividades = [
		###########################################
		# Asignacion
		INPUT(_name='desde', _type='date'),
		INPUT(_name='hasta', _type='date'),
	]

	formaOP = FORM(*camposActividades)
	if formaOP.accepts(request.vars,formname='formaOPHTML',  onvalidation=valida_fechas2, keepvalues=True):
		desde = request.vars.desde
		hasta = request.vars.hasta
		
		
		desde = request.vars.desde
		hasta = request.vars.hasta
		
		
		from datetime import datetime
		import os
		import xlwt
		import uuid
		from xlwt import Workbook #xlwt.Utils 
		#import rowcol_to_cell
		#from xlwt import *
	
		tmpfilename=os.path.join(request.folder,'private','example.xls')
	
		font0 = xlwt.Font()
		font0.name = 'Times New Roman'
		font0.colour_index = 2
		font0.bold = True

		style0 = xlwt.XFStyle()
		style0.font = font0

		style1 = xlwt.XFStyle()
		style1.num_format_str = 'DD-MM-YYYY'
	
		fnt = Font()
		fnt.name = 'Arial'
		fnt.colour_index = 4
		fnt.bold = True
		
		border = xlwt.Borders()  # Frame cells
		border.left = xlwt.Borders.THIN  # Left
		border.top = xlwt.Borders.THIN  # upper
		border.right = xlwt.Borders.THIN  # right
		border.bottom = xlwt.Borders.THIN  # lower
		border.left_colour = 0x40  # Border line color
		border.right_colour = 0x40
		border.top_colour = 0x40
		border.bottom_colour = 0x40
		
	
		pattern = xlwt.Pattern()
		pattern.pattern = xlwt.Pattern.SOLID_PATTERN
		pattern.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']
	
		encab = xlwt.easyxf('font: bold on; align: wrap on, vert center, horiz center')
		encab.borders = border
		encab.pattern = pattern
	
		style = XFStyle()
		style.font = fnt
		style.font.height = 180
		style.num_format_str = '#,##0'
		style.borders = border
	
		style2 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
		num_format_str='#,##0.00')
	
		texto = XFStyle()
		texto = xlwt.easyxf('align: wrap on, vert center, horiz left')
		texto.alignment.wrap = 1
		texto.borders = border
		
		textoC = XFStyle()
		textoC = xlwt.easyxf('align: wrap on, vert center, horiz center')
		textoC.alignment.wrap = 1
		textoC.borders = border
		
		fecha = xlwt.easyxf('align: wrap on, vert center, horiz center')
		fecha.num_format_str = 'DD-MM-YYYY'
		fecha.borders = border
		
		hora = xlwt.easyxf('align: wrap on, vert center, horiz center',num_format_str='#,##0.00')
		hora.borders = border
	
		wb = xlwt.Workbook(encoding="utf-8",style_compression=0)
		ws = wb.add_sheet('Actividades')

		ws.normal_magn=110

		data = []
		
		fec = ws.col(0)
		hor1 = ws.col(1)
		hor2 = ws.col(2)
		act = ws.col(3)
		proy = ws.col(4)
		
		hdr = ws.col(5)
		hnr = ws.col(6)
		hd  = ws.col(7)
		hn  = ws.col(8)
		
		# sec_col = worksheet.col(0)
		
		fec.width = 150*20
		hor1.width = 120*20
		hor2.width = 120*20
		
		act.width = 650*20
		proy.width = 130*20
		
		hdr.width = 130*20
		hnr.width = 130*20
		hd.width = 130*20
		hn.width = 130*20

		top_row = 0
		bottom_row = 0
		left_column = 0
		right_column = 1
		#ws.write_merge(top_row, bottom_row, left_column, right_column, 'Long Cell')

		
		head1 = ['Fecha', 'Hora desde', 'Hora hasta', 'Actividad', 'Proyecto','Horas Diurnas','Horas Nocturnas','Horas Diurnas','Horas Nocturnas',]
		for index, value in enumerate(head1):
			ws.write(0, index, value, encab)
		
		rows = db(db.actividades.cod_asig==db.asignacion.id)(db.asignacion.cod_proyecto==db.proyectos.id)\
		(db.actividades.fecha_inicio >= desde)(db.actividades.fecha_inicio <= hasta)\
		(db.auth_user.id==db.asignacion.analista)(db.auth_user.id==me).\
		select(db.actividades.descripcion,db.actividades.cod_asig,\
		db.actividades.fecha_inicio,db.actividades.hora_inicio,db.actividades.hora_fin,\
		db.proyectos.descri,\
		db.actividades.horas_diurnas_r,db.actividades.horas_nocturnas_r,db.actividades.horas_diurnas,db.actividades.horas_nocturnas,\
		db.actividades.tipo,(db.auth_user.first_name+' '+db.auth_user.last_name).with_alias("analista"), \
		orderby="actividades.fecha_inicio, actividades.hora_inicio, analista")

		row = 1
		col = 0
		
		for index, r in enumerate(rows):
			ws.row(index).height_mismatch = True
			ws.row(index).height = 40*20
			
			ws.write (row, 0, r.actividades.fecha_inicio, fecha)
			ws.write (row, 1, r.actividades.hora_inicio, hora)
			ws.write (row, 2, r.actividades.hora_fin, hora)
			
			ws.write (row, 3, r.actividades.descripcion, texto)
			ws.write (row, 4, r.proyectos.descri, texto)
			
			ws.write (row, 5, r.actividades.horas_diurnas_r, hora)
			ws.write (row, 6, r.actividades.horas_nocturnas_r, hora)
			ws.write (row, 7, r.actividades.horas_diurnas, hora)
			ws.write (row, 8, r.actividades.horas_nocturnas, hora)
			
			row +=1
			
		row +=2
		
		nombre=db.auth_user[me]
		from datetime import datetime
		fecha=convert_date(hasta)
		nombre=db.auth_user[me]
		from datetime import datetime
		fecha=convert_date(hasta)
		
		response.headers['Content-Type']='application/vnd.ms-excel'
		response.headers['Content-disposition'] = 'attachment; filename=%s %s - %s - GL DyA.xls' % (nombre.first_name.upper(), nombre.last_name.upper().decode('utf-8'), fecha) 
		wb.save(tmpfilename)
		data = open(tmpfilename,"rb").read()
		os.unlink(tmpfilename)
		return data
		
		
	elif formaOP.errors:
		response.flash = 'Fechas erradas'
	else:
		response.flash = 'Exito!'
		
	mis_actividades = db(db.actividades.id>0)(db.actividades.cod_asig==db.asignacion.id)(db.asignacion.analista==me).select()
	return locals()


#--------- fin list actividades formato solutor

def tabla():
	form=crud.create(db.actividades_sd)
	query = db.actividades_sd.id>0
	rows = db(query).select(orderby=db.actividades_sd.analista|db.actividades_sd.fecha_inicio)

	return locals()


def tabla2():
	form=crud.create(db.actividades_sd)
	query = db.actividades_sd.id>0
	rows = db(query).select(orderby=db.actividades_sd.analista|db.actividades_sd.fecha_inicio)

	return locals()


# -- list actividades solutor 

def func_count_subA(actividad_id):
	cantidad = db(db.subactividades_sd.actividad_id==actividad_id).count()
	return cantidad

@auth.requires_login()
def list_actividades_solutor2():
	me = auth.user_id
	actividades=''
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_actividades_solutor2').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	#SafeLocale()
	
	ac = db.actividades
	actividades = [OPTION(actividad.id  ,_value=actividad.id) for actividad in
	db(ac.id>0).select(ac.ALL)]
	
	camposActividades = [
		###########################################
		# Asignacion
		INPUT(_name='desde', _type='date'),
		INPUT(_name='hasta', _type='date'),
	]

	formaOP = FORM(*camposActividades)
	if formaOP.accepts(request.vars,formname='formaHTMLSD',  onvalidation=valida_fechas2, keepvalues=True):
		desde = request.vars.desde
		hasta = request.vars.hasta
		
		
		desde = request.vars.desde
		hasta = request.vars.hasta
		
		
		from datetime import datetime
		import os
		import xlwt
		import uuid
		from xlwt import Workbook #xlwt.Utils 
		#import rowcol_to_cell
		#from xlwt import *
	
		tmpfilename=os.path.join(request.folder,'private','example.xls')
	
		font0 = xlwt.Font()
		font0.name = 'Times New Roman'
		font0.colour_index = 2
		font0.bold = True

		style0 = xlwt.XFStyle()
		style0.font = font0

		style1 = xlwt.XFStyle()
		style1.num_format_str = 'DD-MM-YYYY'
	
		fnt = Font()
		fnt.name = 'Arial'
		fnt.colour_index = 4
		fnt.bold = True
		
		border = xlwt.Borders()  # Frame cells
		border.left = xlwt.Borders.THIN  # Left
		border.top = xlwt.Borders.THIN  # upper
		border.right = xlwt.Borders.THIN  # right
		border.bottom = xlwt.Borders.THIN  # lower
		border.left_colour = 0x40  # Border line color
		border.right_colour = 0x40
		border.top_colour = 0x40
		border.bottom_colour = 0x40
		
	
		pattern = xlwt.Pattern()
		pattern.pattern = xlwt.Pattern.SOLID_PATTERN
		pattern.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']
	
		encab = xlwt.easyxf('font: bold on; align: wrap on, vert center, horiz center')
		encab.borders = border
		encab.pattern = pattern
	
		style = XFStyle()
		style.font = fnt
		style.font.height = 90
		style.num_format_str = '#,##0'
		style.borders = border

		style2 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
		num_format_str='#,##0.00')

		texto = XFStyle()
		texto = xlwt.easyxf('align: wrap on, vert center, horiz left')
		texto.alignment.wrap = 1
		texto.borders = border
		
		textoC = XFStyle()
		textoC = xlwt.easyxf('align: wrap on, vert center, horiz center')
		textoC.alignment.wrap = 1
		textoC.borders = border
		
		fecha = xlwt.easyxf('align: wrap on, vert center, horiz center')
		fecha.num_format_str = 'DD-MM-YYYY'
		fecha.borders = border
		
		hora = xlwt.easyxf('align: wrap on, vert center, horiz center',num_format_str='#,##0.00')
		hora.borders = border
	
		wb = xlwt.Workbook(encoding="utf-8",style_compression=0)
		ws = wb.add_sheet('Actividades')

		ws.normal_magn=110

		data = []
		
		analista = ws.col(0)
		ambiente = ws.col(1)
		tipo = ws.col(2)
		fec1 = ws.col(3)
		fec2 = ws.col(4)
		servidor = ws.col(5)
		bd = ws.col(6)
		proy = ws.col(7)
		subp = ws.col(8)
		desc = ws.col(9)
		incid_bd = ws.col(10)
		incid_otros = ws.col(11)
		obs_otros = ws.col(12)
		tot = ws.col(13)
		status = ws.col(14)
		subactividad = ws.col(15)
		tot2 = ws.col(16)
		status2 = ws.col(17)
		# sec_col = worksheet.col(0)
		
		analista.width = 200*20
		ambiente.width = 200*20
		tipo.width = 200*20
		fec1.width = 200*20
		fec2.width = 200*20
		
		proy.width = 600*20
		servidor.width = 250*20
		bd.width = 250*20
		subp.width = 400*20
		desc.width = 700*20
		incid_bd.width = 130*20
		incid_otros.width = 130*20
		obs_otros.width = 130*20
		tot.width = 130*20
		status.width = 330*20
		subactividad.width = 700*20
		tot2.width = 130*20
		status2.width = 130*20

		top_row = 0
		bottom_row = 0
		left_column = 0
		right_column = 1
		#ws.write_merge(top_row, bottom_row, left_column, right_column, 'Long Cell')

		des_tipo=''

		head1 = ['Analista','Ambiente','Tipo','Fecha Inicio', 'Fecha fin', 'Servidor','BD','Proyecto', 'Sub-Proyecto',\
		'Descripcion Actividad','Incidencia-BD','Incidencia-Otros','Obs Otros','Total Hora','Estatus','SubActividad','Total Horas Sub','Estatus']
		for index, value in enumerate(head1):
			ws.write(0, index, value, encab)
		

		#from dateutil.parser import parse
		#desde = New Date(desde)
		#start = parse('%s 00:00:00' % (desde.strftime('%Y-%m-%d')))
		#end = parse('%s 23:59:59' % (hasta.strftime('%Y-%m-%d')))

		a=db.actividades_sd
		b=db.subactividades_sd

		#query=(a.fecha_inicio >= desde)&(a.fecha_inicio <= hasta)|(b.completado=='ABIERTA')
		query=(a.fecha_inicio >= desde)&(a.fecha_inicio <= hasta)
		left=b.on(a.id==b.actividad_id)
		orden=a.analista|a.id|b.id|a.fecha_inicio

		rows = db(query).select(a.id, a.tipo, a.ambiente_id,a.analista,a.fecha_inicio, a.fecha_fin,a.cod_proy,a.cod_subp,a.descripcion,a.horas_laboradas,\
			a.cod_servidor,a.cod_bd,a.incid_bd,a.incid_otros, a.completado, a.obs_otros,\
			b.tipo,	b.analista,	b.fecha_inicio.with_alias('analista2'),\
			b.cod_proy.with_alias('proy'),b.cod_subp.with_alias('sub'),b.descripcion,b.horas_laboradas,b.completado,b.cod_servidor.with_alias('ser'),\
			b.cod_bd.with_alias('bd'),	orderby=orden, left=left)

		row = 1
		col = 0
		w_analista=''

		for index, r in enumerate(rows):

			if r.actividades_sd.tipo == 'R':
				des_tipo='REMOTO'
			else:
				des_tipo='PRESENCIAL'

			# if r.analista!=w_analista:
			# 	row +=1
			# 	ws.write (row, 0, r.analista.first_name +' '+r.analista.last_name,encab)
			# 	row +=2
			
			format_date = '%d-%m-%Y %H:%M%p'

			ws.write (row, 0, r.actividades_sd.analista.first_name +' '+r.actividades_sd.analista.last_name , texto)
			ws.write (row, 1, r.actividades_sd.ambiente_id.descri, texto)
			ws.write (row, 2, des_tipo, texto)
			ws.write (row, 3, r.actividades_sd.fecha_inicio.strftime(format_date), fecha)
			ws.write (row, 4, r.actividades_sd.fecha_fin.strftime(format_date), fecha)
		
			if r.actividades_sd.cod_servidor >0:
				ws.write (row, 5, r.actividades_sd.cod_servidor.nombre, texto)
			else:
				ws.write (row, 5, r.actividades_sd.cod_servidor, texto)
			
			if r.actividades_sd.cod_bd >0:
				ws.write (row, 6, r.actividades_sd.cod_bd.nombre, texto)
			else:
				ws.write (row, 6, r.actividades_sd.cod_bd, texto)
	
			ws.write (row, 7, r.actividades_sd.cod_proy.descri, texto)

			if r.actividades_sd.cod_subp >0:
				ws.write (row, 8, r.actividades_sd.cod_subp.descri, texto)
			else:
				ws.write (row, 8, r.actividades_sd.cod_subp, texto)

			ws.write (row, 9, r.actividades_sd.descripcion, texto)
			if r.actividades_sd.incid_bd:
				ws.write (row, 10, 'X', texto)
			else:
				ws.write (row, 10, '', texto)

			if r.actividades_sd.incid_otros:
				ws.write (row, 11, 'X', texto)
			else:
				ws.write (row, 11, '', texto)
					
			ws.write (row, 12, r.actividades_sd.obs_otros, texto)

			##---- NO MUESTRA LAS HORAS LABORADAS SI TIENE SUBACTIVIDADES

			if func_count_subA(r.actividades_sd.id)==0:
				ws.write (row, 13, r.actividades_sd.horas_laboradas, texto)
			else:	
				ws.write (row, 13, '0,00', texto)


			ws.write (row, 14, r.actividades_sd.completado, texto)
			ws.write (row, 15, r.subactividades_sd.descripcion, texto)

			ws.write (row, 16, r.subactividades_sd.horas_laboradas, texto)
			
			ws.write (row, 17, r.subactividades_sd.completado, texto)

			w_analista = r.actividades_sd.analista
			
			row +=1
			
		
		row =1

		# -------- Actividades abiertas - subactividades --------------------------------------------
		wsa = wb.add_sheet('Actividades Abiertas')

		wsa.normal_magn=110

		analista = wsa.col(0)
		ambiente = wsa.col(1)
		tipo = wsa.col(2)
		fec1 = wsa.col(3)
		fec2 = wsa.col(4)
		servidor = wsa.col(5)
		bd = wsa.col(6)
		proy = wsa.col(7)
		subp = wsa.col(8)
		desc = wsa.col(9)
		incid_bd = wsa.col(10)
		incid_otros = wsa.col(11)
		obs_otros = wsa.col(12)
		tot = wsa.col(13)
		status = wsa.col(14)
		
	
	
		# sec_col = worksheet.col(0)
		
		analista.width = 200*20
		ambiente.width = 700*20
		tipo.width = 200*20
		fec1.width = 200*20
		fec2.width = 200*20

		proy.width = 600*20
		servidor.width = 250*20
		bd.width = 250*20
		subp.width = 400*20
		desc.width = 700*20
		incid_bd.width = 130*20
		incid_otros.width = 130*20
		obs_otros.width = 130*20
		tot.width = 130*20
		status.width = 130*20

		top_row = 0
		bottom_row = 0
		left_column = 0
		right_column = 1
		#ws.write_merge(top_row, bottom_row, left_column, right_column, 'Long Cell')

		des_tipo=''

		head1 = ['Analista','Actividad Principal','Tipo','Fecha Inicio', 'Fecha fin', 'Servidor','BD','Proyecto', 'Sub-Proyecto',\
		'Descripcion Actividad','Incidencia-BD','Incidencia-Otros','Obs Otros','Total Hora','Estatus']
		for index, value in enumerate(head1):
			wsa.write(0, index, value, encab)



		a=db.actividades_sd
		b=db.subactividades_sd

		query=(b.fecha_inicio >= desde)&(b.fecha_inicio <= hasta)|(a.completado=='ABIERTA')
		#query=(a.completado=='ABIERTA')
		left=b.on(a.id==b.actividad_id)
		orden=a.analista|a.id|b.id|a.fecha_inicio

		rowsb = db(query).select(a.tipo, a.ambiente_id,a.analista,a.fecha_inicio,a.fecha_fin, a.cod_proy,a.cod_subp,a.descripcion,a.horas_laboradas,\
			a.cod_servidor,a.cod_bd,a.incid_bd,a.incid_otros, a.completado, a.obs_otros,\
			b.actividad_id, b.tipo,	b.analista,	b.fecha_inicio, b.fecha_fin, \
			b.cod_proy,b.cod_subp,b.descripcion,b.horas_laboradas,b.completado,b.cod_servidor,b.cod_bd,	orderby=orden, left=left)


		w_act=''
		for index, r in enumerate(rowsb):
			if r.subactividades_sd.analista:
				if r.actividades_sd.tipo == 'R':
					des_tipo='REMOTO'
				else:
					des_tipo='PRESENCIAL'
	
				if r.actividades_sd.analista:
					wsa.write (row, 0, r.actividades_sd.analista.first_name +' '+r.actividades_sd.analista.last_name , texto)
				else:
					wsa.write (row, 0, ' ', texto)
	
				if r.subactividades_sd.actividad_id:	
					wsa.write (row, 1, r.subactividades_sd.actividad_id.descripcion, texto)
				else:
					wsa.write (row, 1, '', texto)
	
				wsa.write (row, 2, des_tipo, texto)
				wsa.write (row, 3, r.subactividades_sd.fecha_inicio.strftime(format_date), fecha)
				wsa.write (row, 4, r.subactividades_sd.fecha_fin.strftime(format_date), fecha)
			
				wsa.write (row, 5, '', texto)
				
				wsa.write (row, 6, '', texto)
				
				if r.subactividades_sd.cod_proy:
					wsa.write (row, 7, r.subactividades_sd.cod_proy.descri, texto)
				else:
					wsa.write (row, 7, ' ', texto)	

				if r.subactividades_sd.cod_subp >0:
					wsa.write (row, 8, r.subactividades_sd.cod_subp.descri, texto)
				else:
					wsa.write (row, 8, r.subactividades_sd.cod_subp, texto)
	
				wsa.write (row, 9, r.subactividades_sd.descripcion, texto)
				
				wsa.write (row, 10, '', texto)
	
				wsa.write (row, 11, '', texto)
						
				
				wsa.write (row, 12, '', texto)
				wsa.write (row, 13, r.subactividades_sd.horas_laboradas, texto)
				wsa.write (row, 14, r.subactividades_sd.completado, texto)
				
				w_analista = r.subactividades_sd.analista
				
				w_act=r.subactividades_sd.actividad_id

				row +=1

		
		nombre=db.auth_user[me]
		from datetime import datetime
		fecha=convert_date(hasta)

		response.headers['Content-Type']='application/vnd.ms-excel'
		response.headers['Content-disposition'] = 'attachment; filename=%s %s - %s - GL DyA.xls' % (nombre.first_name.upper(), nombre.last_name.upper().decode('utf-8'), fecha) 
		wb.save(tmpfilename)
		data = open(tmpfilename,"rb").read()
		os.unlink(tmpfilename)
		return data
		
		
	elif formaOP.errors:
		response.flash = 'Fechas erradas'
	else:
		response.flash = 'Exito!'
		
	mis_actividades = db(db.actividades.id>0)(db.actividades.cod_asig==db.asignacion.id)(db.asignacion.analista==me).select()
	return locals()



#--------- fin list actividades formato solutor



	

#--------- exportar inventario a excel ---------------------------------------------------------

def exportar_inv_excel2():
	import pandas as pd
	
	return locals()


#@auth.requires_membership('dba')
@auth.requires_membership('DBA')
def exportar_inv_excel():
	# -*- coding: windows-1251 -*-
	# -*- coding: utf-8 -*-
	from datetime import datetime
	import os
	import xlwt
	import uuid
	from xlwt import Workbook #xlwt.Utils 
	#import rowcol_to_cell
	#from xlwt.Utils import rowcol_to_cell
	#from xlwt import *
	
	
	tmpfilename='InventarioBD'

	
	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']

	
	font0 = xlwt.Font()
	font0.name = 'Times New Roman'
	font0.colour_index = 2
	font0.bold = True

	style0 = xlwt.XFStyle()
	style0.font = font0

	style1 = xlwt.XFStyle()
	style1.num_format_str = 'DD-MM-YYYY'
	
	fnt = font0
	fnt.name = 'Arial'
	fnt.colour_index = 4
	fnt.bold = True
		
	border = xlwt.Borders()  # Frame cells
	border.left = xlwt.Borders.THIN  # Left
	border.top = xlwt.Borders.THIN  # upper
	border.right = xlwt.Borders.THIN  # right
	border.bottom = xlwt.Borders.THIN  # lower
	border.left_colour = 0x40  # Border line color
	border.right_colour = 0x40
	border.top_colour = 0x40
	border.bottom_colour = 0x40
		
	
	pattern = xlwt.Pattern()
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN
	pattern.pattern_fore_colour = xlwt.Style.colour_map['pale_blue']
	
	encab = xlwt.easyxf('font: name Arial, bold on; align: wrap on, vert center, horiz center')
	encab.borders = border
	encab.pattern = pattern
	
	style = xlwt.XFStyle()
	style.font = fnt
	style.font.height = 180
	style.num_format_str = '#,##0'
	style.borders = border
	
	style2 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
	num_format_str='#,##0.00')
	
	xalig = xlwt.Alignment()
	xalig.horz = 0x02   #  the font level is centered 
	xalig.vert = 0x01   #  the font level is centered 
	xalig.wrap = True

	xfont = xlwt.Font()
	xfont.colour_index =  xlwt.Style.colour_map['black']
	xfont.bold = False          #  bold 
	xfont.height = 20 * 10     #  set font height （20 it's the same base, 10 the font size is used for resizing ）
	xfont.name = ' arial '     #  set the font 

	texto = style
	#texto = xlwt.easyxf('align: wrap on, vert center, horiz left')
	#texto.alignment.wrap = 1
	texto.borders = border
	texto.font = xfont
	texto.alignment = xalig
			
	fecha = xlwt.easyxf('align: wrap on, vert center, horiz center')
	fecha.num_format_str = 'DD-MM-YYYY'
	fecha.borders = border
		
	hora = xlwt.easyxf('align: wrap on, vert center, horiz center',num_format_str='#,##0.00')
	hora.borders = border

	wb = xlwt.Workbook(encoding="utf-8",style_compression=0)
	
	ws = wb.add_sheet('PRODUCCION')
	ca = wb.add_sheet('CALIDAD')
	de = wb.add_sheet('DESARROLLO')
	drs = wb.add_sheet('DATAGUARD')


	# ------ produccion -------------------------------------
	ws.normal_magn=90

	data = []
	tequi = ws.col(0)
	serv = ws.col(1)
	ip = ws.col(2)
	tipobase = ws.col(3)
	base = ws.col(4)
	edo= ws.col(5)
	ver = ws.col(6)
	asm = ws.col(7)
	appl = ws.col(8)
	rac = ws.col(9)
	# sec_col = worksheet.col(0)
	tequi.width = 150*20
	serv.width = 200*20
	ip.width = 200*20
	tipobase.width = 150*20
	base.width = 300*20
	edo.width = 300*20
	ver.width = 150*20
	asm.width = 120*20
	appl.width = 500*20
	rac.width = 150*20
	
	head = ['TIPO EQUIPO','SERVIDOR', 'IP', 'TIPO BD', 'BASE DE DATOS','ESTADO', 'VERSION', 'ASM', 'APLICACION','RAC']
	for index, value in enumerate(head):
		ws.write(0, index, value, encab)
	
	
	#query=db(db.basedatos.servidor == db.servidores.id)(db.basedatos.ambiente_id == db.ambiente.id)\
	#(db.basedatos.version_id == db.ver.id)(db.servidores.tipo_equipo == db.tipo_equipos.id)(db.ambiente.descri.like('PRODUCC%'))
	
	query=db(db.ambiente.descri.like('PRODUCC%'))
	#query=db(db.ambiente.descri.like('PRODUCC%'))(db.estadobd.descri.like('DISPO%'))
	
	left=[db.basedatos.on(db.servidores.id == db.basedatos.servidor),
			db.ambiente.on(db.basedatos.ambiente_id == db.ambiente.id),
			db.ver.on(db.basedatos.version_id == db.ver.id),
			db.tipo_equipos.on(db.servidores.tipo_equipo == db.tipo_equipos.id),
			db.estadobd.on(db.basedatos.estado_id == db.estadobd.id),
			db.tipobd.on(db.basedatos.tipobd_id == db.tipobd.id)
		]
	orden="tipo_equipos.descri, servidores.nombre, basedatos.nombre, estadobd.descri"
	
	rows = (query).select(db.tipo_equipos.descri, db.servidores.nombre, db.servidores.ip, db.tipobd.descri, db.basedatos.nombre, \
	db.ver.descri, db.basedatos.asm, db.basedatos.appl, db.estadobd.descri, db.servidores.rac, left=left, orderby=orden )

	row = 1
	col = 0
		
	for index, r in enumerate(rows):
		ws.row(index).height_mismatch = True

		ws.row(index).height = 40*20
		ws.write (row, 0, r.tipo_equipos.descri, texto)
		ws.write (row, 1, r.servidores.nombre, texto)
		ws.write (row, 2, r.servidores.ip, texto)
		ws.write (row, 3, r.tipobd.descri, texto)
		ws.write (row, 4, r.basedatos.nombre, texto)
		ws.write (row, 5, r.estadobd.descri, texto)
		ws.write (row, 6, r.ver.descri, texto)
		ws.write (row, 7, r.basedatos.asm, texto)
		#data = str(r.basedatos.appl)
		#ws.col(8).width = 256 * len(data) * 2 
		ws.write (row, 8, r.basedatos.appl, texto)
		ws.write (row, 9, r.servidores.rac, texto)
		row +=1
	
	#ws.write(row+2, 2, xlwt.Formula("A3+B3"))
	# ------ calidad -------------------------------------
	ca.normal_magn=90

	
	data = []
	tequi = ca.col(0)
	serv = ca.col(1)
	ip = ca.col(2)
	tipobase = ca.col(3)
	base = ca.col(4)
	edo= ca.col(5)
	ver = ca.col(6)
	asm = ca.col(7)
	appl = ca.col(8)
	rac = ca.col(9)
	# sec_col = worksheet.col(0)
	tequi.width = 150*20
	serv.width = 200*20
	ip.width = 200*20
	tipobase.width = 150*20
	base.width = 300*20
	edo.width = 300*20
	ver.width = 150*20
	asm.width = 120*20
	appl.width = 500*20
	rac.width = 150*20

	
	
	head = ['TIPO EQUIPO','SERVIDOR', 'IP', 'TIPO BD', 'BASE DE DATOS','ESTADO', 'VERSION', 'ASM', 'APLICACION','RAC']
	for index, value in enumerate(head):
		ca.write(0, index, value, encab)
	
	
	rows = db(db.basedatos.servidor==db.servidores.id)(db.basedatos.ambiente_id==db.ambiente.id)\
	(db.basedatos.version_id==db.ver.id)(db.servidores.tipo_equipo==db.tipo_equipos.id)(db.ambiente.descri=='CALIDAD').\
	select(db.tipo_equipos.descri, db.servidores.nombre, db.servidores.ip, db.basedatos.nombre, db.ver.descri, db.basedatos.asm, db.basedatos.appl, db.servidores.rac, \
	orderby="tipo_equipos.descri, servidores.nombre, basedatos.nombre" )

	
	row = 1
	col = 0

	query=db(db.ambiente.descri.like('CALIDAD%'))
	#query=db(db.ambiente.descri.like('PRODUCC%'))(db.estadobd.descri.like('DISPO%'))
	
	left=[db.basedatos.on(db.servidores.id == db.basedatos.servidor),
			db.ambiente.on(db.basedatos.ambiente_id == db.ambiente.id),
			db.ver.on(db.basedatos.version_id == db.ver.id),
			db.tipo_equipos.on(db.servidores.tipo_equipo == db.tipo_equipos.id),
			db.estadobd.on(db.basedatos.estado_id == db.estadobd.id),
			db.tipobd.on(db.basedatos.tipobd_id == db.tipobd.id)
		]
	orden="tipo_equipos.descri, servidores.nombre, basedatos.nombre, estadobd.descri"
	
	rows = (query).select(db.tipo_equipos.descri, db.servidores.nombre, db.servidores.ip, db.tipobd.descri, db.basedatos.nombre, \
	db.ver.descri, db.basedatos.asm, db.basedatos.appl, db.estadobd.descri, db.servidores.rac, left=left, orderby=orden )

	row = 1
	col = 0
		
	for index, r in enumerate(rows):
		ca.row(index).height_mismatch = True
		ca.row(index).height = 40*20
		ca.write (row, 0, r.tipo_equipos.descri, texto)
		ca.write (row, 1, r.servidores.nombre, texto)
		ca.write (row, 2, r.servidores.ip, texto)
		ca.write (row, 3, r.tipobd.descri, texto)
		ca.write (row, 4, r.basedatos.nombre, texto)
		ca.write (row, 5, r.estadobd.descri, texto)
		ca.write (row, 6, r.ver.descri, texto)
		ca.write (row, 7, r.basedatos.asm, texto)
		ca.write (row, 8, r.basedatos.appl, texto)
		ca.write (row, 9, r.servidores.rac, texto)
		row +=1		
	# ------ desarrollo -------------------------------------
	de.normal_magn=90

	data = []

	tequi = de.col(0)
	serv = de.col(1)
	ip = de.col(2)
	tipobase = de.col(3)
	base = de.col(4)
	edo= de.col(5)
	ver = de.col(6)
	asm = de.col(7)
	appl = de.col(8)
	rac = de.col(9)

	# sec_col = worksheet.col(0)
	# sec_col = worksheet.col(0)
	tequi.width = 150*20
	serv.width = 200*20
	ip.width = 200*20
	tipobase.width = 150*20
	base.width = 300*20
	edo.width = 300*20
	ver.width = 150*20
	asm.width = 120*20
	appl.width = 500*20
	rac.width = 150*20
	
	head = ['TIPO EQUIPO','SERVIDOR', 'IP', 'TIPO BD', 'BASE DE DATOS','ESTADO', 'VERSION', 'ASM', 'APLICACION','RAC']
	for index, value in enumerate(head):
		de.write(0, index, value, encab)
	
	
	query=db(db.ambiente.descri.like('DESA%'))
	#query=db(db.ambiente.descri.like('PRODUCC%'))(db.estadobd.descri.like('DISPO%'))
	
	left=[db.basedatos.on(db.servidores.id == db.basedatos.servidor),
			db.ambiente.on(db.basedatos.ambiente_id == db.ambiente.id),
			db.ver.on(db.basedatos.version_id == db.ver.id),
			db.tipo_equipos.on(db.servidores.tipo_equipo == db.tipo_equipos.id),
			db.estadobd.on(db.basedatos.estado_id == db.estadobd.id),
			db.tipobd.on(db.basedatos.tipobd_id == db.tipobd.id)
		]
	orden="tipo_equipos.descri, servidores.nombre, basedatos.nombre, estadobd.descri"
	
	rows = (query).select(db.tipo_equipos.descri, db.servidores.nombre, db.servidores.ip, db.tipobd.descri, db.basedatos.nombre, \
	db.ver.descri, db.basedatos.asm, db.basedatos.appl, db.estadobd.descri, db.servidores.rac, left=left, orderby=orden )

	
	row = 1
	col = 0
		
	for index, r in enumerate(rows):
		de.row(index).height_mismatch = True
		de.row(index).height = 40*20
		de.write (row, 0, r.tipo_equipos.descri, texto)
		de.write (row, 1, r.servidores.nombre, texto)
		de.write (row, 2, r.servidores.ip, texto)
		de.write (row, 3, r.tipobd.descri, texto)
		de.write (row, 4, r.basedatos.nombre, texto)
		de.write (row, 5, r.estadobd.descri, texto)
		de.write (row, 6, r.ver.descri, texto)
		de.write (row, 7, r.basedatos.asm, texto)
		de.write (row, 8, r.basedatos.appl, texto)
		de.write (row, 9, r.servidores.rac, texto)
		row +=1	

# ------ produccion -------------------------------------
	drs.normal_magn=90

	data = []
	tequi = ws.col(0)
	serv = ws.col(1)
	ip = ws.col(2)
	tipobase = ws.col(3)
	base = ws.col(4)
	edo= ws.col(5)
	ver = ws.col(6)
	asm = ws.col(7)
	appl = ws.col(8)
	rac = ws.col(9)
	# sec_col = worksheet.col(0)
	tequi.width = 150*20
	serv.width = 200*20
	ip.width = 200*20
	tipobase.width = 150*20
	base.width = 300*20
	edo.width = 300*20
	ver.width = 150*20
	asm.width = 120*20
	appl.width = 500*20
	rac.width = 150*20
	
	head = ['TIPO EQUIPO','SERVIDOR', 'IP', 'TIPO BD', 'BASE DE DATOS','ESTADO', 'VERSION', 'ASM', 'APLICACION','RAC']
	for index, value in enumerate(head):
		drs.write(0, index, value, encab)
	
	
	#query=db(db.basedatos.servidor == db.servidores.id)(db.basedatos.ambiente_id == db.ambiente.id)\
	#(db.basedatos.version_id == db.ver.id)(db.servidores.tipo_equipo == db.tipo_equipos.id)(db.ambiente.descri.like('PRODUCC%'))
	
	query=db(db.ambiente.descri.like('DATAGUAR%'))
	#query=db(db.ambiente.descri.like('PRODUCC%'))(db.estadobd.descri.like('DISPO%'))
	
	left=[db.basedatos.on(db.servidores.id == db.basedatos.servidor),
			db.ambiente.on(db.basedatos.ambiente_id == db.ambiente.id),
			db.ver.on(db.basedatos.version_id == db.ver.id),
			db.tipo_equipos.on(db.servidores.tipo_equipo == db.tipo_equipos.id),
			db.estadobd.on(db.basedatos.estado_id == db.estadobd.id),
			db.tipobd.on(db.basedatos.tipobd_id == db.tipobd.id)
		]
	orden="tipo_equipos.descri, servidores.nombre, basedatos.nombre, estadobd.descri"
	
	rows = (query).select(db.tipo_equipos.descri, db.servidores.nombre, db.servidores.ip, db.tipobd.descri, db.basedatos.nombre, \
	db.ver.descri, db.basedatos.asm, db.basedatos.appl, db.estadobd.descri, db.servidores.rac, left=left, orderby=orden )

	row = 1
	col = 0
		
	for index, r in enumerate(rows):
		drs.row(index).height_mismatch = True

		drs.row(index).height = 40*20
		drs.write (row, 0, r.tipo_equipos.descri, texto)
		drs.write (row, 1, r.servidores.nombre, texto)
		drs.write (row, 2, r.servidores.ip, texto)
		drs.write (row, 3, r.tipobd.descri, texto)
		drs.write (row, 4, r.basedatos.nombre, texto)
		drs.write (row, 5, r.estadobd.descri, texto)
		drs.write (row, 6, r.ver.descri, texto)
		drs.write (row, 7, r.basedatos.asm, texto)
		#data = str(r.basedatos.appl)
		#ws.col(8).width = 256 * len(data) * 2 
		drs.write (row, 8, r.basedatos.appl, texto)
		drs.write (row, 9, r.servidores.rac, texto)
		row +=1
	
	#ws.write(row+2, 2, xlwt.Formula("A3+B3"))
	# ------ fin pestañas  -------------------------------------		
		
	nombre=db.auth_user[me]
	from datetime import datetime
	now = datetime.now()
	fecha = now.strftime("%d%m%Y")
		
	response.headers['Content-Type']='application/vnd.ms-excel'
	response.headers['Content-disposition'] = 'attachment; filename=%s-%s%s' % (tmpfilename, fecha,  '.xls')
	wb.save(tmpfilename)
	data = open(tmpfilename,"rb").read()
	os.unlink(tmpfilename)

	return data





#-------- fin exportar inventario a excel ----------------------------------------------------------------------


@auth.requires_login()
def list_estadisticas():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#list_estadisticas_tab1').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	oTable = $('#list_estadisticas_tab2').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')

	result_esta_serv = db.executesql('''
		-- cantidad bd por servidor
		SELECT 'SERVIDORES'::text AS TIPO, a.descri::text AS ambiente, 'TEQUI-'||t.descri AS PARAMETROS,	s.nombre AS descri, count(b.id) AS cant 
		FROM SERVIDORES S, basedatos b, ambiente a, tipo_equipos t 
		where s.id = b.servidor and a.id = s.ambiente_id and t.id = s.tipo_equipo group by a.descri, t.descri, s.nombre
		UNION
		-- TODOS TIPO DE ESQUIPOS POR AMBIENTE
		SELECT 'SERVIDORES' AS TIPO, A.DESCRI AS ABMIENTE, 'TIPO EQUIPO' AS PARAMETROS, T.DESCRI AS DESCRI, COUNT(*) FROM SERVIDORES S, TIPO_EQUIPOS T, AMBIENTE A
		WHERE T.ID=S.TIPO_EQUIPO AND A.ID = S.AMBIENTE_ID GROUP BY 1,A.DESCRI, T.DESCRI
		UNION
		-- TODOS ALMACEN POR AMBIENTE
		SELECT 'SERVIDORES' AS TIPO, A.DESCRI AS ABMIENTE, 'STORAGE' AS PARAMETROS, AL.DESCRI AS DESCRI, COUNT(*) 	
		FROM SERVIDORES S, ALMACEN AL, AMBIENTE A
		WHERE  A.ID = S.AMBIENTE_ID AND AL.ID = S.ALMACEN AND AL.DESCRI='VMAX' AND
		S.ID IN (Select servidor 
											from basedatos B, ESTADOBD E 
											where B.asm='ASM-SI' AND E.ID = B.ESTADO_ID
											AND E.DESCRI = 'DISPONIBLE')
		GROUP BY 1,A.DESCRI, AL.DESCRI
		UNION
		-- TOTAL SERVIDORES 
		SELECT 'SERVIDORES'::text AS TIPO, ''::text AS ambiente, 'PARAMETROS' AS PARAMETROS,	'TOTAL' AS descri, count(*) AS cant 
		FROM SERVIDORES S
		UNION
		-- TOTAL POR AMBIENTE
		SELECT 'SERVIDORES' AS TIPO, 'TODOS' AS ABMIENTE, 'AMBIENTES' AS PARAMETROS, A.DESCRI AS DESCRI, COUNT(*) FROM SERVIDORES S, AMBIENTE A
		WHERE  A.ID = S.AMBIENTE_ID GROUP BY 1,2,A.DESCRI
		UNION
		-- TOTAL POR RAC-SI
		SELECT 'SERVIDORES'::text AS TIPO, 'TODOS'::text AS ambiente, 'RAC' AS PARAMETROS,	S.RAC AS descri, count(*) AS cant 
		FROM SERVIDORES S
		WHERE S.RAC ='RAC-SI' GROUP BY 1,S.RAC
		UNION
		-- TOTAL RAC POR AMBIENTE
		SELECT 'SERVIDORES'::text AS TIPO, A.DESCRI::text AS ambiente,'RAC' AS PARAMETROS,	S.RAC AS descri, count(*) AS cant 
		FROM SERVIDORES S, AMBIENTE A
		WHERE A.ID = S.AMBIENTE_ID GROUP BY 1,A.DESCRI, S.RAC
		UNION
		-- TOTAL VERSION POR SERVIDOR AMBIENTE
		SELECT 'SERVIDORES'::text AS TIPO, a.descri::text AS ambiente, s.nombre AS PARAMETROS,	v.descri AS descri, count(b.id) AS cant 
		FROM SERVIDORES S, basedatos b, ambiente a, ver v , estadobd e
		where s.id = b.servidor and a.id = s.ambiente_id and v.id = b.version_id and e.id = b.estado_id and e.descri='DISPONIBLE' 
		group by a.descri, s.nombre, v.descri
		ORDER BY 1, 2 DESC, 3
		''');
		
	result_esta_bd = db.executesql('''
		SELECT 'BASE DE DATOS'::text AS TIPO, 'TODOS'::text AS ambiente,'AMBIENTES' AS PARAMETROS,	'PRODUCCIÃ“N'::text AS descri, count(*) AS cant
		FROM basedatos b,ambiente a WHERE a.id = b.ambiente_id AND a.descri::text = 'PRODUCCIÃ“N'::text
		UNION
		SELECT 'BASE DE DATOS', 'TODOS'::text AS ambiente,'AMBIENTES' AS PARAMETROS,	'CALIDAD'::text AS descri,count(*) AS cant
		FROM basedatos b,ambiente a	WHERE a.id = b.ambiente_id AND a.descri::text = 'CALIDAD'::text
		UNION
		SELECT 'BASE DE DATOS','TODOS'::text AS ambiente,'AMBIENTES' AS PARAMETROS,	'DESARROLLO'::text AS descri,count(*) AS cant
		FROM basedatos b,ambiente a		WHERE a.id = b.ambiente_id AND a.descri::text = 'DESARROLLO'::text
		UNION
		SELECT 'BASE DE DATOS','TODOS'::text AS ambiente,'AMBIENTES' AS PARAMETROS,	'LABORATORIO'::text AS descri,	count(*) AS cant
		FROM basedatos b,ambiente a		WHERE a.id = b.ambiente_id AND a.descri::text = 'LABORATORIO'::text
		UNION
		SELECT 'BASE DE DATOS','TODOS'::text AS ambiente,'AMBIENTES' AS PARAMETROS,	'OTROS AMBIENTES'::text AS descri,count(*) AS cant
		FROM basedatos b,ambiente a	WHERE a.id = b.ambiente_id AND (a.descri::text != ALL (ARRAY['PRODUCCIÃ“N'::character varying, 'CALIDAD'::character varying, 'DESARROLLO'::character varying, 'LABORATORIO'::character varying]::text[]))
		UNION
		SELECT 'BASE DE DATOS','TODOS'::text AS ambiente,'ASM' AS PARAMETROS,'ASM-SI'::text AS descri,count(*) AS cant
		FROM basedatos b,ambiente a	WHERE b.asm::text = 'ASM-SI'::text AND a.id = b.ambiente_id	GROUP BY a.descri, 'ASM-SI'::text
		UNION
		SELECT 'BASE DE DATOS','TODOS'::text AS ambiente,'ASM' AS PARAMETROS,'ASM-NO'::text AS descri,count(*) AS cant
		FROM basedatos b,ambiente a	WHERE b.asm::text = 'ASM-NO'::text AND a.id = b.ambiente_id	GROUP BY a.descri, 'ASM-NO'::text
		UNION
		SELECT 'BASE DE DATOS','TODOS'::text AS ambiente,'APPL' AS PARAMETROS,'SIN-APPL'::text AS descri,count(*) AS cant
		FROM basedatos b,ambiente a	WHERE (b.appl='' OR b.appl is null) AND a.id = b.ambiente_id	GROUP BY a.descri, 'SIN-APPL'::text
		UNION
		SELECT 'BASE DE DATOS','TODOS' AS ambiente,'BACKUP' AS PARAMETROS,soft_respaldo::text AS descri,	count(*) AS cant
		FROM basedatos b,ambiente a	WHERE a.id = b.ambiente_id	GROUP BY 1,a.descri, b.soft_respaldo
		UNION
		SELECT 'BASE DE DATOS','TODOS' AS ambiente,'BACKUP' AS PARAMETROS,soft_respaldo::text AS descri,	count(*) AS cant
		FROM basedatos b WHERE b.soft_respaldo='NETWORKER' GROUP BY 1,soft_respaldo
		UNION
		SELECT 'BASE DE DATOS','TODOS' AS ambiente,'BACKUP' AS PARAMETROS,soft_respaldo::text AS descri,	count(*) AS cant
		FROM basedatos b WHERE  b.soft_respaldo='VERITAS'	GROUP BY 1,soft_respaldo
		UNION
		SELECT 'BASE DE DATOS','TODOS' AS ambiente,'BACKUP' AS PARAMETROS,soft_respaldo::text AS descri,	count(*) AS cant
		FROM basedatos b	WHERE  b.soft_respaldo='SIN BACKUP'	GROUP BY 1,soft_respaldo
		UNION
		SELECT 'BASE DE DATOS','TODOS'::text AS ambiente,'ASM' AS PARAMETROS,	b.asm AS descri,count(*) AS cant
		FROM basedatos b	WHERE b.asm::text = 'ASM-SI'::text	GROUP BY 1,'TODOS'::text, b.asm
		UNION
		SELECT 'BASE DE DATOS','TODOS'::text AS ambiente,'ASM' AS PARAMETROS,	b.asm AS descri,count(*) AS cant
		FROM basedatos b	WHERE b.asm::text = 'ASM-NO'::text	GROUP BY 1,'TODOS'::text, b.asm
		UNION
		SELECT 'BASE DE DATOS',a.descri AS ambiente,'ESTADO' AS PARAMETROS,e.descri,	count(*) AS cant
		FROM basedatos b,estadobd e,ambiente a	WHERE b.estado_id = e.id AND a.id = b.ambiente_id	GROUP BY 1,a.descri, e.descri
		UNION
		SELECT 'BASE DE DATOS',a.descri AS ambiente,'VERSION' AS PARAMETROS,v.descri,count(b.version_id) AS cant
		FROM basedatos b,ver v,	ambiente a	WHERE v.id = b.version_id AND a.id = b.ambiente_id	GROUP BY 1,a.descri, v.descri
		ORDER BY 1, 2 DESC, 3
		''');
	#r = db.executesql('''
	#	SELECT 'BASE DE DATOS'::text AS TIPO, 'TODOS'::text AS ambiente,'AMBIENTES' AS PARAMETROS,	'PRODUCCIÃ“N'::text AS descri, count(*) AS cant
	#	FROM basedatos b,ambiente a WHERE a.id = b.ambiente_id AND a.descri::text = 'PRODUCCIÃ“N'::text
	#	ORDER BY 1, 2 DESC, 3
	#   ''', as_dict=True);
	r=''  
	return dict(script=script, serv=result_esta_serv, bd=result_esta_bd, r=r)

def detalle_esta():
	bd_serv=request.args(0)
	ambiente=request.args(1) 
	tipo_par=request.args(2)
	parametro=request.args(3)
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#detalle_esta').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''') 
	query=''
	where=''
	if bd_serv == 'BD':
		if ambiente=='' and parametro=='TOTAL':
			where = "where s.id = b.servidor ";
			query=''' select s.nombre, b.nombre, b.appl from basedatos b, servidores s ''' + where
		elif ambiente=='TODOS' and tipo_par=='ASM':
			where = "where s.id = b.servidor and b.asm=" + "'" + parametro + "'";
			query=''' select s.nombre, b.nombre, b.appl from basedatos b, servidores s ''' + where
		elif ambiente=='TODOS' and tipo_par=='AMBIENTES':
			where = "where s.id = b.servidor and  a.id = b.ambiente_id and a.descri like('%" + parametro[:4] + "%')";
			query=''' select s.nombre, b.nombre, b.appl from basedatos b, servidores s, ambiente a ''' + where
		elif ambiente=='TODOS' and tipo_par=='BACKUP':
			where = "where s.id = b.servidor and b.soft_respaldo like('%" + parametro[:4] + "%')";
			query=''' select s.nombre, b.nombre, b.appl from basedatos b, servidores s ''' + where
		elif ambiente[:4] != 'TODO' and tipo_par=='ASM':
			where = "where s.id = b.servidor and  a.id = b.ambiente_id and a.descri like('%" + ambiente[:4] + "%')" + " and b.asm=" + "'" + parametro + "'";
			query=''' select s.nombre, b.nombre, b.appl from basedatos b, servidores s, ambiente a ''' + where
		elif ambiente[:4] != 'TODO' and tipo_par=='BACKUP':
			where = "where s.id = b.servidor and  a.id = b.ambiente_id and a.descri like('%" + ambiente[:4] + "%')" + " and b.soft_respaldo like('%" + parametro[:4] + "%')";
			query=''' select s.nombre, b.nombre, b.appl from basedatos b, servidores s, ambiente a ''' + where
		elif ambiente[:4] != 'TODO' and tipo_par=='ESTADO':
			where = "where s.id = b.servidor and  a.id = b.ambiente_id and e.id = b.estado_id and a.descri like('%" + ambiente[:4] + "%')" + " and e.descri like('%" + parametro[:4] + "%')";
			query=''' select s.nombre, b.nombre, b.appl from basedatos b, servidores s, ambiente a, estadobd e ''' + where
		elif ambiente[:4] != 'TODO' and tipo_par=='VERSION':
			where = "where s.id = b.servidor and  a.id = b.ambiente_id and e.id = b.version_id and a.descri like('%" + ambiente[:4] + "%')" + " and e.descri ='" + parametro + "'";
			query=''' select s.nombre, b.nombre, b.appl from basedatos b, servidores s, ambiente a, ver e ''' + where
		elif ambiente[:4] != 'TODO' and tipo_par=='APPL':
			where = "where s.id = b.servidor and  a.id = b.ambiente_id and  a.descri like('%" + ambiente[:4] + "%')" + " and B.APPL IS NULL";
			query=''' select s.nombre, b.nombre, b.appl from basedatos b, servidores s, ambiente a ''' + where
	elif bd_serv == 'SERV':
		if ambiente=='' and parametro=='TOTAL':
			where = "where t.id = s.tipo_equipo ";
			query=''' select t.descri, s.nombre, s.ip from servidores s, tipo_equipos t ''' + where
		elif ambiente=='TODOS' and tipo_par=='ASM':
			where = "where s.id = b.servidor and b.asm=" + "'" + parametro + "'";
			query=''' select s.nombre, b.nombre, s.ip from basedatos b, servidores s ''' + where

		elif ambiente!='TODOS' and tipo_par[:5]=='TEQUI':
			#UPDATE SERVIDORES SET NOMBRE = REPLACE(NOMBRE,'/','-')

			where = "where s.id = b.servidor and v.id = b.version_id and s.nombre=" + "'" +  parametro + "'";
			query=''' select s.nombre, b.nombre, v.descri from basedatos b, servidores s, VER V ''' + where
		elif ambiente[:4] != 'TODO' and tipo_par=='STORAGE':
			where = "where AL.ID= S.ALMACEN AND a.id = s.ambiente_id and a.descri like('%" + ambiente[:4] + "%')" + " and AL.DESCRI =" + "'" + parametro + "'" 
			where += " AND S.ID IN (select servidor  from basedatos B, ESTADOBD E 	where B.asm='ASM-SI' AND E.ID = B.ESTADO_ID	AND E.DESCRI = 'DISPONIBLE')";
			query=''' select a.descri,s.nombre, s.ip from  servidores s, ambiente a, ALMACEN AL ''' + where	
	
		elif ambiente!='TODOS' and tipo_par !='VERSION':
			where = "where s.id = b.servidor and v.id = b.version_id and s.nombre=" + "'" + tipo_par + "'" + " and V.DESCRI = " + "'" + parametro + "'";
			query=''' select s.nombre, b.nombre, v.descri from basedatos b, servidores s, VER V ''' + where
		
		elif ambiente=='TODOS' and tipo_par=='RAC':
			where = "where s.rac=" + "'" + parametro + "'";
			query=''' select s.nombre, s.ip, s.rac from servidores s ''' + where
		elif ambiente=='TODOS' and tipo_par=='TIPO_EQUIPO':
			where = "where s.tipo_equipo = t.id and t.descri like('%" + parametro[:4] + "%')";
			query=''' select t.descri, s.nombre, s.rac from servidores s, tipo_equipos t ''' + where
		elif ambiente=='TODOS' and tipo_par=='AMBIENTES':
			where = "where a.id = s.ambiente_id and a.descri like('%" + parametro[:4] + "%')";
			query=''' select a.descri,s.nombre , s.rac from  servidores s, ambiente a ''' + where
		elif ambiente[:4] != 'TODO' and tipo_par=='RAC':
			where = "where a.id = s.ambiente_id and a.descri like('%" + ambiente[:4] + "%')" + " and s.rac=" + "'" + parametro + "'";
			query=''' select a.descri,s.nombre, s.ip from  servidores s, ambiente a ''' + where
		elif ambiente[:4] != 'TODO' and tipo_par=='TIPO_EQUIPO':
			where = "where s.ambiente_id = a.id and  t.id = s.tipo_equipo and a.descri like('%" + ambiente[:4] + "%')" + " and t.descri like('%" + parametro[:4] + "%')";
			query=''' select t.descri, s.nombre, s.ip from tipo_equipos t, servidores s, ambiente a ''' + where
		
	else:	
		session.flash='no';
	datos=db.executesql(query);	
	return dict(script=script, bd_serv=bd_serv, ambiente=ambiente, tipo_par=tipo_par, parametro=parametro, query=query, datos=datos)


# ------ pin y tnsping ---------------------------------

import subprocess
import time
from gluon.tools import Service
service = Service()

def check_ping(ip):
	try:
		start = time.time()
		output = subprocess.check_output(
			['ping', '-c', '1', '-W', '2', ip],
			stderr=subprocess.STDOUT,
			universal_newlines=True
		)
		latency = round((time.time() - start) * 1000, 2)  # ms
		return {
			'status': True,
			'latency': latency,
			'last_response': request.now
		}
	except Exception as e:
		return {
			'status': False,
			'latency': None,
			'last_response': request.now
		}


def construir_tns_entry(record):
	if record.tns_entry:
		return record.tns_entry
	return f"""(DESCRIPTION=
				(ADDRESS=(PROTOCOL=TCP)(HOST={record.servidor_id.ip})(PORT={record.puerto}))
				(CONNECT_DATA=(SERVER=DEDICATED)
					{f"(SID={record.sid})" if record.sid else ""}
					{f"(SERVICE_NAME={record.service_name})" if record.service_name else ""}
				))"""

def check_tnsping(record):
	try:
		# Construir la cadena de conexión directa (EZCONNECT)
		if record.nombre:
			connect_string = f"{record.servidor.ip}:{record.puerto}/{record.nombre}"
		else:
			connect_string = f"{record.servidor.ip}:{record.puerto}/{record.service_name}"
		
		start = time.time()
		
		# Ejecutar tnsping con timeout
		process = subprocess.Popen(
			['tnsping', connect_string],
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			universal_newlines=True,
			env={'ORACLE_HOME': record.servidor.oracle_home} if record.servidor.oracle_home else None
		)
		
		try:
			stdout, stderr = process.communicate(timeout=15)
			
			# Analizar respuesta
			if "OK" in stdout:
				return {
					'status': True,
					'output': stdout,
					'response_time': round((time.time() - start) * 1000, 2),
					'connect_string': connect_string,
					'last_check': request.now
				}
			else:
				return {
					'status': False,
					'error': 'TNS Error',
					'output': stdout or stderr,
					'connect_string': connect_string,
					'last_check': request.now
				}
				
		except subprocess.TimeoutExpired:
			process.kill()
			return {
				'status': False,
				'error': 'Timeout',
				'output': 'El comando tnsping excedió el tiempo de espera (15s)',
				'connect_string': connect_string,
				'last_check': request.now
			}
		
	except Exception as e:
		return {
			'status': False,
			'error': str(e),
			'output': f"Error al ejecutar tnsping: {str(e)}",
			'connect_string': connect_string,
			'last_check': request.now
		}

@auth.requires_login()
def dashboard():
	# Obtener y verificar servidores (igual que antes)
	servidores = []
	for server in db(db.servidores)(db.servidores.ip != "1.1.1.1").select():
		ping_result = check_ping(server.ip)
		servidores.append({
			'id': server.id,
			'nombre': server.nombre,
			'ip': server.ip,
			'status': ping_result['status'],
			'latency': ping_result.get('latency', 0),
			'last_response': ping_result.get('last_response', 'N/A')
		})
	
	# Obtener y verificar instancias de BD
	bases_datos = []
	for db_record in db(db.basedatos)(db.basedatos.nombre != 'BD NUEVA').select(orderby=db.basedatos.nombre):
		# Determinar el tipo de verificación según el tipo de BD
		if db_record.tipobd_id and db_record.tipobd_id.descri.lower() == 'mssqlserver':
			# Verificación para SQL Server
			sqlserver_result = check_sqlserver(db_record)
			bases_datos.append({
				'id': db_record.id,
				'nombre': db_record.nombre,
				'servidor_id': db_record.servidor,
				'aplicacion': db_record.appl,
				'ambiente': db_record.ambiente_id.descri,
				'status': sqlserver_result['status'],
				'output': sqlserver_result.get('output', ''),
				'response_time': sqlserver_result.get('response_time', 0),
				'tns_entry': sqlserver_result.get('connection_string', ''),
				'last_check': sqlserver_result.get('last_check', 'N/A')
			})
		else:
			# Verificación para Oracle (tnsping) como antes
			tnsping_result = check_tnsping(db_record)
			bases_datos.append({
				'id': db_record.id,
				'nombre': db_record.nombre,
				'servidor_id': db_record.servidor,
				'aplicacion': db_record.appl,
				'ambiente': db_record.ambiente_id.descri,
				'status': tnsping_result['status'],
				'output': tnsping_result.get('output', ''),
				'response_time': tnsping_result.get('response_time', 0),
				'tns_entry': tnsping_result.get('connect_string', ''),
				'last_check': tnsping_result.get('last_check', 'N/A')
			})
	
	return dict(
		servidores=servidores,
		bases_datos=bases_datos,
		time=request.now
	)


def check_sqlserver(db_record):
	import pyodbc
	from datetime import datetime
	import json
	import os
	from dotenv import load_dotenv
	
	try:
		# Construir cadena de conexión
		server = db_record.servidor.ip if db_record.servidor else 'localhost'
		database = db_record.nombre
		username = os.getenv('SQLSERVER_USER')  # Valor por defecto solo para desarrollo
		password = os.getenv('SQLSERVER_PASSWORD')
		
		# Cadena de conexión directa para pyodbc
		connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server},1433;DATABASE={database};UID={username};PWD={password}"
		start_time = datetime.now()
		
		# Intentar conexión
		conn = pyodbc.connect(connection_string, timeout=10)
		cursor = conn.cursor()
		
		# Ejecutar una consulta simple para verificar
		cursor.execute("SELECT 1")
		result = cursor.fetchone()
		
		end_time = datetime.now()
		response_time = (end_time - start_time).total_seconds() * 1000  # ms
		
		conn.close()
		
		return {
			'status': 1,
			'output': "Conexión exitosa a SQL Server",
			'response_time': round(response_time, 2),
			'connection_string': connection_string,
			'last_check': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		}
		
	except Exception as e:
		return {
			'status': 0,
			'output': f'Conexion fallida: {str(e)}',
			'response_time': 0,
			'connection_string': connection_string if 'connection_string' in locals() else 'No se pudo construir',
			'last_check': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		}

#----- area de graficas -----------
def horas_por_bd():
	import datetime
	
	# Obtener parámetros de mes y año (o usar el actual)
	mes_param = request.vars.mes  # Formato esperado: "YYYY-MM"
	
	if mes_param:
		try:
			año_seleccionado, mes_seleccionado = map(int, mes_param.split('-'))
		except:
			# Si el formato es incorrecto, usar el mes actual
			hoy = datetime.date.today()
			mes_seleccionado = hoy.month
			año_seleccionado = hoy.year
	else:
		hoy = datetime.date.today()
		mes_seleccionado = hoy.month
		año_seleccionado = hoy.year
	
	# Consulta SQL para obtener los meses disponibles con datos
	sql_meses = """
	SELECT DISTINCT 
		   EXTRACT(YEAR FROM fecha_inicio) as año,
		   EXTRACT(MONTH FROM fecha_inicio) as mes
	FROM actividades_sd
	ORDER BY año DESC, mes DESC
	"""
	
	# Consulta SQL principal modificada para incluir el nombre del servidor
	sql = """
	SELECT b.nombre, ser.nombre as servidor, 
		   SUM(a.horas_laboradas + a.horas_extras) as total_horas
	FROM actividades_sd a
	JOIN servidores ser ON ser.id = a.cod_servidor
	JOIN basedatos b ON b.servidor = ser.id
	WHERE EXTRACT(MONTH FROM a.fecha_inicio) = %s
	AND EXTRACT(YEAR FROM a.fecha_inicio) = %s
	GROUP BY b.nombre, ser.nombre
	ORDER BY total_horas DESC
	"""
	
	try:
		# Obtener meses disponibles
		meses_db = db.executesql(sql_meses, as_dict=True)
		meses_disponibles = [
			f"{int(m['año'])}-{int(m['mes']):02d}" for m in meses_db
		]
		
		# Obtener datos para el mes seleccionado
		registros = db.executesql(sql, (mes_seleccionado, año_seleccionado), as_dict=True)
		
		# Preparar datos para el gráfico incluyendo servidor
		chart_data = [['Base de Datos', 'Horas']]
		for r in registros:
			# Mostrar "BD (Servidor)" como etiqueta
			label = f"{r['nombre']} ({r['servidor']})"
			chart_data.append([label, float(r['total_horas'])])
			
		return dict(
			chart_data=chart_data,
			mes=f"{mes_seleccionado}/{año_seleccionado}",
			mes_param=f"{año_seleccionado}-{mes_seleccionado:02d}",
			meses_disponibles=meses_disponibles
		)
		
	except Exception as e:
		return dict(error=str(e))


# ambiente


def horas_por_ambiente():
	from datetime import datetime
	
	# Obtener parámetros de mes y año (o usar el actual)
	mes_param = request.vars.mes  # Formato esperado: "YYYY-MM"
	
	if mes_param:
		try:
			año_seleccionado, mes_seleccionado = map(int, mes_param.split('-'))
			mes_str = datetime(año_seleccionado, mes_seleccionado, 1).strftime("%B %Y")
		except:
			# Si el formato es incorrecto, usar el mes actual
			ahora = datetime.now()
			mes_seleccionado = ahora.month
			año_seleccionado = ahora.year
			mes_str = ahora.strftime("%B %Y")
	else:
		ahora = datetime.now()
		mes_seleccionado = ahora.month
		año_seleccionado = ahora.year
		mes_str = ahora.strftime("%B %Y")
	
	# Consulta para obtener meses disponibles con datos
	sql_meses = """
	SELECT DISTINCT 
		   EXTRACT(YEAR FROM fecha_inicio) as año,
		   EXTRACT(MONTH FROM fecha_inicio) as mes
	FROM actividades_sd
	ORDER BY año DESC, mes DESC
	"""
	
	# Consulta principal que suma horas laboradas + horas extras
	query = """
	SELECT 
		am.descri as ambiente,
		COALESCE(SUM(a.horas_laboradas + COALESCE(a.horas_extras, 0)), 0) as total_horas,
		COALESCE(SUM(a.horas_laboradas), 0) as horas_normales,
		COALESCE(SUM(a.horas_extras), 0) as horas_extra
	FROM 
		ambiente am
	LEFT JOIN 
		actividades_sd a ON a.ambiente_id = am.id
		AND EXTRACT(MONTH FROM a.fecha_inicio) = {mes}
		AND EXTRACT(YEAR FROM a.fecha_inicio) = {año}
	GROUP BY 
		am.descri, am.id
	ORDER BY 
		am.id
	""".format(mes=mes_seleccionado, año=año_seleccionado)
	
	try:
		# Obtener meses disponibles
		meses_db = db.executesql(sql_meses, as_dict=True)
		meses_disponibles = [
			f"{int(m['año'])}-{int(m['mes']):02d}" for m in meses_db
		]
		
		# Obtener datos para el mes seleccionado
		registros = db.executesql(query, as_dict=True)
		
		# Preparar datos para el gráfico
		ambientes = []
		horas_totales = []
		horas_normales = []
		horas_extras = []
		
		for r in registros:
			ambientes.append(r['ambiente'])
			horas_normales.append(float(r['horas_normales']))
			horas_extras.append(float(r['horas_extra']))
			horas_totales.append(float(r['total_horas']))
		
		return dict(
			ambientes=ambientes,
			horas_totales=horas_totales,
			horas_normales=horas_normales,
			horas_extras=horas_extras,
			mes_actual=mes_str,
			mes_param=mes_param if mes_param else f"{año_seleccionado}-{mes_seleccionado:02d}",
			meses_disponibles=meses_disponibles
		)
		
	except Exception as e:
		return dict(error=str(e))


#----- por analista



def horas_por_analista():
	from datetime import datetime
	
	# Inicializar variables
	error = None
	meses_disponibles = []
	analistas = []
	chart_bd = {'labels': [], 'data': []}
	chart_ambiente = {'labels': [], 'normales': [], 'extras': [], 'totales': []}
	total_horas = 0.0
	
	# Obtener parámetros
	mes_param = request.vars.mes  # Formato YYYY-MM
	analista_id = request.vars.analista  # ID del analista
	
	# Validar mes o usar actual
	ahora = datetime.now()
	if mes_param:
		try:
			año, mes = map(int, mes_param.split('-'))
			mes_str = datetime(año, mes, 1).strftime("%B %Y")
			mes_formatted = f"{año}-{mes:02d}"
		except:
			año, mes = ahora.year, ahora.month
			mes_str = ahora.strftime("%B %Y")
			mes_formatted = f"{año}-{mes:02d}"
	else:
		año, mes = ahora.year, ahora.month
		mes_str = ahora.strftime("%B %Y")
		mes_formatted = f"{año}-{mes:02d}"
	
	try:
		# 1. Obtener meses disponibles
		sql_meses = """
		SELECT DISTINCT 
			   EXTRACT(YEAR FROM fecha_inicio) as año,
			   EXTRACT(MONTH FROM fecha_inicio) as mes
		FROM actividades_sd
		ORDER BY año DESC, mes DESC
		"""
		meses_db = db.executesql(sql_meses, as_dict=True)
		meses_disponibles = [f"{int(m['año'])}-{int(m['mes']):02d}" for m in meses_db] or [mes_formatted]
		
		# 2. Obtener lista de analistas (desde auth_user)
		sql_analistas = """
		SELECT id, first_name || ' ' || last_name as nombre 
		FROM auth_user
		WHERE id IN (SELECT DISTINCT analista FROM actividades_sd)
		ORDER BY last_name, first_name
		"""
		analistas = db.executesql(sql_analistas, as_dict=True)
		
		# 3. Datos por Base de Datos
		sql_bd = """
		SELECT b.nombre, ser.nombre as servidor, 
			   SUM(a.horas_laboradas + COALESCE(a.horas_extras, 0)) as total_horas
		FROM actividades_sd a
		JOIN servidores ser ON ser.id = a.cod_servidor
		JOIN basedatos b ON b.servidor = ser.id
		WHERE EXTRACT(MONTH FROM a.fecha_inicio) = %s
		AND EXTRACT(YEAR FROM a.fecha_inicio) = %s
		{filtro_analista}
		GROUP BY b.nombre, ser.nombre
		ORDER BY total_horas DESC
		""".format(
			filtro_analista="AND a.analista = %s" if analista_id else ""
		)
		
		params_bd = [mes, año]
		if analista_id:
			params_bd.append(analista_id)
		
		bd_data = db.executesql(sql_bd, params_bd, as_dict=True)
		chart_bd = {
			'labels': [f"{r['nombre']} ({r['servidor']})" for r in bd_data],
			'data': [float(r['total_horas']) for r in bd_data]
		}
		
		# 4. Datos por Ambiente
		sql_ambiente = """
		SELECT am.descri as ambiente,
			   SUM(a.horas_laboradas) as horas_normales,
			   SUM(COALESCE(a.horas_extras, 0)) as horas_extras,
			   SUM(a.horas_laboradas + COALESCE(a.horas_extras, 0)) as total_horas
		FROM ambiente am
		JOIN actividades_sd a ON a.ambiente_id = am.id
		WHERE EXTRACT(MONTH FROM a.fecha_inicio) = %s
		AND EXTRACT(YEAR FROM a.fecha_inicio) = %s
		{filtro_analista}
		GROUP BY am.descri, am.id
		ORDER BY total_horas DESC
		""".format(
			filtro_analista="AND a.analista = %s" if analista_id else ""
		)
		
		params_ambiente = [mes, año]
		if analista_id:
			params_ambiente.append(analista_id)
		
		ambiente_data = db.executesql(sql_ambiente, params_ambiente, as_dict=True)
		chart_ambiente = {
			'labels': [r['ambiente'] for r in ambiente_data],
			'normales': [float(r['horas_normales']) for r in ambiente_data],
			'extras': [float(r['horas_extras']) for r in ambiente_data],
			'totales': [float(r['total_horas']) for r in ambiente_data]
		}
		total_horas = sum(chart_ambiente['totales']) if chart_ambiente['totales'] else 0
		
		# Obtener nombre del analista seleccionado
		analista_seleccionado = next(
			(a['nombre'] for a in analistas if str(a['id']) == str(analista_id)),
			"Todos los analistas"
		)
		
	except Exception as e:
		error = str(e)
	
	return dict(
		chart_bd=chart_bd,
		chart_ambiente=chart_ambiente,
		meses_disponibles=meses_disponibles,
		mes_param=mes_formatted,
		mes_actual=mes_str,
		analistas=analistas,
		analista_id=analista_id,
		analista_seleccionado=analista_seleccionado,
		total_horas=total_horas,
		error=error
	)


def horas_por_ambiente_mes_actual():
	from datetime import datetime
	
	# Obtener el mes y año actual
	ahora = datetime.now()
	mes_actual = ahora.month
	año_actual = ahora.year
	
	# Consulta corregida para PostgreSQL
	query = """
	SELECT am.descri as ambiente, 
		   COALESCE(SUM(a.horas_laboradas), 0) as total_horas,
		   am.id as ambiente_id
	FROM ambiente am
	LEFT JOIN actividades_sd a ON a.ambiente_id = am.id
	  AND EXTRACT(MONTH FROM a.fecha_inicio) = {mes}
	  AND EXTRACT(YEAR FROM a.fecha_inicio) = {año}
	GROUP BY am.id, am.descri
	ORDER BY am.id
	""".format(mes=mes_actual, año=año_actual)
	
	registros = db.executesql(query, as_dict=True)
	
	# Preparar datos para el gráfico
	ambientes = []
	horas = []
	
	for r in registros:
		ambientes.append(r['ambiente'])
		horas.append(float(r['total_horas']))
	
	return dict(
		ambientes=ambientes, 
		horas=horas,
		mes_actual=ahora.strftime("%B %Y")
	)

def horas_por_actividades():
	from datetime import datetime
	
	# Obtener parámetros del formulario o usar valores por defecto
	mes = request.vars.mes or datetime.now().month
	año = request.vars.año or datetime.now().year
	
	try:
		mes = int(mes)
		año = int(año)
	except:
		mes = datetime.now().month
		año = datetime.now().year
	
	# Validar rangos
	mes = max(1, min(12, mes))
	año = max(2000, min(2100, año))
	
	# Consulta SQL
	query = """
	SELECT 
		p.descri as proyecto,
		SUM(a.horas_laboradas + COALESCE(a.horas_extras, 0)) as total_horas,
		COUNT(a.id) as cantidad_actividades
	FROM 
		actividades_sd a
	JOIN 
		proyectos p ON a.cod_proy = p.id
	WHERE
		EXTRACT(MONTH FROM a.fecha_inicio) = {mes}
		AND EXTRACT(YEAR FROM a.fecha_inicio) = {año}
	GROUP BY 
		p.descri
	ORDER BY 
		total_horas DESC
	""".format(mes=mes, año=año)
	
	registros = db.executesql(query, as_dict=True)
	
	# Preparar datos
	proyectos = [r['proyecto'] for r in registros]
	horas = [float(r['total_horas']) for r in registros]
	background_colors = [get_color_for_proyecto(p) for p in proyectos]
	border_colors = [color.replace('0.7', '1') for color in background_colors]
	
	# Generar lista de meses y años para el dropdown
	meses = [
		(1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), 
		(4, 'Abril'), (5, 'Mayo'), (6, 'Junio'),
		(7, 'Julio'), (8, 'Agosto'), (9, 'Septiembre'),
		(10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
	]
	
	años = list(range(2020, datetime.now().year + 1))
	cant_actividades = [float(r['cantidad_actividades']) for r in registros]
	return dict(
		registros=registros,
		proyectos=proyectos,
		horas=horas,
		background_colors=background_colors,
		border_colors=border_colors,
		mes_actual=mes,
		año_actual=año,
		meses=meses,
		años=años,
		cant_actividades=cant_actividades,
		nombre_mes=next((m[1] for m in meses if m[0] == mes), ''),
		total_general=sum(horas)
	)

def get_color_for_proyecto(proyecto):
	# Asignar colores consistentes a cada proyecto basado en hash
	colores_disponibles = [
		'rgba(54, 162, 235, 0.7)',  # Azul
		'rgba(255, 99, 132, 0.7)',  # Rojo
		'rgba(75, 192, 192, 0.7)',  # Verde
		'rgba(255, 206, 86, 0.7)',  # Amarillo
		'rgba(153, 102, 255, 0.7)', # Morado
		'rgba(255, 159, 64, 0.7)',  # Naranja
		'rgba(199, 199, 199, 0.7)', # Gris
		'rgba(83, 102, 255, 0.7)',  # Azul oscuro
		'rgba(40, 167, 69, 0.7)',   # Verde oscuro
		'rgba(108, 117, 125, 0.7)'  # Gris oscuro
	]
	
	# Generar un índice consistente basado en el nombre del proyecto
	hash_valor = sum(ord(c) for c in proyecto)
	indice_color = hash_valor % len(colores_disponibles)
	
	return colores_disponibles[indice_color]


import gluon.contrib.simplejson

@auth.requires_login()
def progreso_monitoreo():
	"""
	Devuelve el estado actual del monitoreo: base de datos y consulta actual.
	Puedes guardar el progreso en session, en una tabla temporal, o en un archivo.
	Aquí se muestra un ejemplo usando session.
	"""
	progreso = session.progreso_monitoreo or {}
	return gluon.contrib.simplejson.dumps(progreso)


