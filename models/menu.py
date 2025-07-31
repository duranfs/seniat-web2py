
from gluon import current
response = current.response

response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]


# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

configuracion_actividades = [
    (T('Configurar Actividades'), False, '#', [
            (T('Ver tipo actividad'), URL('default','list_proyectos')==URL(),URL('default','list_proyectos'),[]),
			(T('Crear tipo actividad'), URL('default','crear_proyectos')==URL(),URL('default','crear_proyectos'),[]),
			(T('Editar tipo actividad'), URL('default','editar_proyectos')==URL(),URL('default','editar_proyectos'),[]),
			(T('Subactividades'), URL('subproyectos','crear_subproyectos')==URL(),URL('subproyectos','crear_subproyectos'),[]),
			#(T('reporte nuevo  '), URL('reportes','reporte_sd')==URL(),URL('reportes','reporte_sd'),[]),
        ]),
]


actividades_dba = [
    (T('Actividades'), False, '#', [
	      (T('Registrar Actividades '), URL('default','crear_actividades_sd')==URL(),URL('default','crear_actividades_sd'),[]),
          (T('Editar Actividades'), URL('default','list_actividades_sd')==URL(),URL('default','list_actividades_sd'),[]),
          (T('Editar SubActividades'), URL('bitacora','list_subactividades_sd')==URL(),URL('bitacora','list_subactividades_sd'),[]),
          (T('Bitácora de Actividades'), URL('bitacora','bitacora_actividades_sd')==URL(),URL('bitacora','bitacora_actividades_sd'),[]),
          (T('Reporte de Actividades'), URL('reportes','reporte_sd')==URL(),URL('reportes','reporte_sd'),[]),
           ]),
]

inventario = [
	(T('Inventario'), False, '#', [
				(T('Servidores'),URL('default','list_servidores')==URL(),URL('default','list_servidores'),[]),
				(T('Base de Datos'),URL('default','list_basedatos')==URL(),URL('default','list_basedatos'),[]),
				(T('Estadisticas'),URL('default','list_estadisticas')==URL(),URL('default','list_estadisticas'),[]),
				(T('Cuentas/claves'),URL('default','list_cuentas_so')==URL(),URL('default','list_cuentas_so'),[]),
				#(T('Custodios'),URL('default','list_custodios_bd_appl')==URL(),URL('default','list_custodios_bd_appl'),[]),
				#(T('Politicas de Respaldos'),URL('default','list_matriz_respaldo')==URL(),URL('default','list_matriz_respaldo'),[]),
				#(T('Reporte RMAN y RMAN12'),URL('default','lista_rman12_online')==URL(),URL('default','lista_rman12_online'),[]),
				]),
				]

dba_admin =  [
	(T('DBA'), False, '#', [
				(T('Administradores'), URL('default','list_dba')==URL(),URL('default','list_dba'),[]),
				(T('Ejecutar SQL CYGNUS'), URL('oracle','ejecutar_sql')==URL(),URL('oracle','ejecutar_sql'),[]),
				]),
	(T('Tablas'), False, '#', [
				(T('Tipo de Equipos'), URL('default','list_tipoequipo')==URL(),URL('default','list_tipoequipo'),[]),
				(T('Tipos de Bases de Datos'), URL('default','list_dba')==URL(),URL('default','list_tipobd'),[]),
				(T('Ubicacion/Area'), URL('default','list_dba')==URL(),URL('default','list_ubicacion'),[]),
				(T('Ambiente'), URL('default','list_dba')==URL(),URL('default','list_ambiente'),[]),
				(T('Versiones'), URL('default','list_dba')==URL(),URL('default','list_version'),[]),
				(T('Sistema Operativo'), URL('default','list_dba')==URL(),URL('default','list_so'),[]),
				(T('Estados Base de datos'), URL('default','list_dba')==URL(),URL('default','list_estados'),[]),
				(T('Custodios por Aplicacion'), URL('default','list_dba')==URL(),URL('default','list_custodios'),[]),]),
	(T('Reportes'), False, '#', [
				(T('Exportar inventario a Excel'), URL('default','exportar_inv_excel')==URL(),URL('default','exportar_inv_excel'),[]),
				
				(T('Servidores'), URL('default','reporte_servidores')==URL(),URL('default','reporte_servidores'),[]),			
				
				]),
			]



reportes =  [
	(T('Reportes'), False, '#', [
				(T('Exportar inventario a Excel'), URL('default','exportar_inv_excel')==URL(),URL('default','exportar_inv_excel'),[]),
				(T('Servidores'), URL('default','reporte_servidores')==URL(),URL('default','reporte_servidores'),[]),]),			
				#(T('Guardias'), URL('default','reporte_guardias')==URL(),URL('default','reporte_guardias'),[]),
				#(T('Servidores Parametrizado'), URL('default','rep_serv_respc')==URL(),URL('default','rep_serv_respc'),[]),]),
			]

graficas =  [
	(T('Gráficas'), False, '#', [
				(T('Horas por BD'), URL('default','horas_por_bd')==URL(),URL('default','horas_por_bd'),[]),
				(T('Horas por Ambiente'), URL('default','horas_por_ambiente')==URL(),URL('default','horas_por_ambiente'),[]),
				(T('Horas por Analista'), URL('default','horas_por_analista')==URL(),URL('default','horas_por_analista'),[]),
				(T('Horas por Actividades'), URL('default','horas_por_actividades')==URL(),URL('default','horas_por_actividades'),[]),
				(T('Declaraciones'), URL('oracle','declaraciones')==URL(),URL('oracle','declaraciones'),[]),
            	(T('DeclaracionesXAño'), URL('oracle','declaraciones_por_anio')==URL(),URL('oracle','declaraciones_por_anio'),[]),
     ])
	]

administracion =[
	(T('Administración'), False, '#', [
            (T('Usuarios'), URL(request.application,'plugin_useradmin','index')==URL(),URL(request.application,'plugin_useradmin','index'),[]),
            (T('Grupos'), URL(request.application,'plugin_manage_groups','index')==URL(),URL(request.application,'plugin_manage_groups','index'),[]),
            (T('Threads'), URL('default','check_threads')==URL(),URL('default','check_threads'),[]),

   #(T('Control de Sesiones'), URL('default','manage_sessions')==URL(),URL('default','manage_sessions'),[]),
        ]),
		]

wiki =[
	  (T('Wiki'), False, '#', [
	        (T('Wiki'), URL('default','list_program')==URL(),URL('default','list_program'),[]),
             ]),
		]			



monitor =[
	(T('Mónitor'), False, '#', [
            (T('Parámetros'), URL('default','list_rutinas')==URL(),URL('default','list_rutinas'),[]),
            (T('Asignar Parámetros'), URL('default','asignar_rutinas')==URL(),URL('default','asignar_rutinas'),[]),
			(T('Administrar Parámetros'), URL('default','rutinas_asignadas')==URL(),URL('default','rutinas_asignadas'),[]),
			(T('Monitor ORACLE'), False, URL('default','monitor_bd', args=['9']), []), #oracle
			(T('Monitor SQLServer'), False, URL('default','monitor_bd', args=['11']), []), 
			(T('Monitor PostgreSQL'), False, URL('default','monitor_bd', args=['9']), []),
			(T('Monitor Compacto'), False, URL('default','monitor_bd_compacto', args=['9']), []),
			(T('Dashboard'), URL('default','dashboard')==URL(),URL('default','dashboard'),[]),
            (T('ErrorLog CYGNUS'), URL('oracle','consulta_log_error')==URL(),URL('oracle','consulta_log_error'),[]),
            (T('Monitor Alert Logs'), URL('oracle','monitorear_alert_logs')==URL(),URL('oracle','monitorear_alert_logs'),[]),
            (T('Estadisticas Rep Z seniatfe'), URL('oracle','consulta_seniatfe')==URL(),URL('oracle','consulta_seniatfe'),[]),
              #(T('Prueba SQLSERVER'), URL('sqlserver','index')==URL(),URL('sqlserver','index'),[]),
            #(T('Ejecutar SQL '), URL('default','ejecuta_comando_sql')==URL(),URL('default','ejecuta_comando_sql'),[]),
           
           # (T('9i'), URL('default','prueba_9i')==URL(),URL('default','prueba_9i'),[]),
        ]),
		]

monitor_OPERADOR =[
	(T('Monitor'), False, '#', [
            (T('Monitor ORACLE'), False, URL('default','monitor_bd', args=['9']), []),
			(T('Monitor SQLServer'), False, URL('default','monitor_bd', args=['11']), []),
			(T('Monitor PostgreSQL'), False, URL('default','monitor_bd', args=['8']), []),
            (T('Estadisticas Rep Z seniatfe'), URL('oracle','consulta_seniatfe')==URL(),URL('oracle','consulta_seniatfe'),[]),
            (T('ErrorLog CYGNUS'), URL('oracle','consulta_log_error')==URL(),URL('oracle','consulta_log_error'),[]),
            (T('Dashboard'), URL('default','dashboard')==URL(),URL('default','dashboard'),[]),
        ]),
		]



if auth.is_logged_in():

	if not configuration.get('app.production'):
		_app = request.application
		
		if  auth.has_membership("DBA") and auth.has_membership("ADMIN") and auth.has_membership("SYSTEM"):
			response.menu += configuracion_actividades
			response.menu += actividades_dba
			response.menu += inventario
			response.menu += monitor
			response.menu += graficas
			response.menu += dba_admin
			response.menu += administracion
			response.menu += wiki
		elif auth.has_membership("DBA") and auth.has_membership("ADMIN"):
			response.menu += configuracion_actividades
			response.menu += actividades_dba
			response.menu += inventario
			response.menu += monitor
			response.menu += graficas
			response.menu += wiki
		elif auth.has_membership("DBA") :
			response.menu += actividades_dba
			response.menu += inventario
			response.menu += monitor
			response.menu += graficas
			response.menu += reportes
			response.menu += wiki
		elif auth.has_membership("OPERADOR") :
			response.menu += monitor_OPERADOR
			
