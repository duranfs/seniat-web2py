# -*- coding: utf-8 -*-
### required - do no delete


if request.is_local:
    from gluon.custom_import import track_changes
    track_changes(True)
    
migrate = True
redefine = False

def formato_montos(field):
    try:
        valor = "{:,}".format(field)
    except (ValueError, TypeError):
        valor = field    
    return SPAN(valor, _class="montos")

def ds_bd(bd_id):
    if bd_id is None:
        return ""
    return "%(nombre)s " % db.basedatos(bd_id)
    
is_phone = IS_MATCH(r'^(\+\d{2}\-)?[\d\-]*(\#\d+)?$')
TIPOBD = ("ORACLE","POSTGRESQL","MYSQL","SQLSERVER","DB2")
UBICACION = ("CARACAS","INTEVEP","CAMPINA","UBV","DESPACHO","GUARENAS","GUATIRE","CAMPINA")
TIPOCONEX = ("SSH","TELNET","ESCRITORIO REMOTO")
TIPO_ACT = ("R","P")
AMB = ("DESARROLLO","CALIDAD","PRODUCCION","LABORATORIO","CONTINGENCIA","POR DEFINIR")
SO = ("linux","unix","aix","windows","SunOs 5.10","linux","Linux","HP-UX","SUSE","AIX","SOLARIS","aix  ","RED HAT","DEBIAN","CentOs")
STATUS_MON = ("SI","NO")
REGISTRO = ("REGISTRADO","SIN REGISTRAR")
STATUS_TAREA = ("NO INICIADO","EN CURSO","COMPLETADO")
STATUS_ASIG = ("NO INICIADO","INICIADO")
STATUS_PROYECTO = ("POR REALIZAR","ASIGNADO","EN CURSO","COMPLETADO")
SOFT_RESPALDO = ("NETWORKER","VERITAS","SIN BACKUP","A DISCO-NETW","FILESYSTEM")
TIPO_BACKUP = ("ONLINE","OFFLINE")
DOMINIO = ("SENIAT.GOV.VE","BANVENEZ.COM","BANVENEZ.CORP","BANVENQA.COM","BANVENDES.CORP")
STATUS_SERVIDOR = ("OPERATIVO","INOPERATIVO")
SN = ("SI","NO")
STATUS_MTTO = ("MTTO-SI","MTTO-NO","MTTO-PARCIAL")
IMPACTO = ("ALTO","MEDIO","BAJO")
PRIORIDAD = ("NORMAL","ALTA","BAJA")
CRITICIDAD = ("ALTA","MEDIA","BAJA")
BINARIO = ("32 BITS","64 BITS")
ASM = ("ASM-SI","ASM-NO")
RAC = ("CLUSTER-SI","CLUSTER-NO")
TASK_TYPES = ('Migracion','Apoyo','Correo', 'Reunion','Informe','Reporte de novedades','Instalacion','Configuracion','Actualizaion','Registro','Aviso','Procesar')
TASK_BASEDATOS_TYPES = ('Registro','Configuracion', 'Respaldo', 'Cambio', 'Ampliacion','Correccion','Reporte de novedades')
VERSION = ("MySql  5.5.31","PostgreSQL Ver. 8.4.13","PostgreSQL Ver. 8.3.14","PostgreSQL Ver. 8.4.18",
"PostgreSQL Ver. 8.3.9","MySql  5.0.51","oracle 8.1.6.3.0","oracle  9.0.1.3.0","PostgreSQL Ver. 9.0.5",
"oracle 9.0.1.3.0","oracle  9.2.0.1.0","PostgreSQL Ver. 9.3.5","PostGreSQL v 8.4.15","MySql 5.0.32",
"PostgreSQL Ver. 9.2.2","PostgreSQL Ver. 8.1.11","DB2 v 9.5","oracle 8.1.7.3.0","PostgreSQL Ver. 9.3",
"oracle 9.2.0.7.0","sqlserver   ","MySql 5.0.51","oracle 8.1.7.0.0","oracle 8.1.7.4.0","oracle 8.1.7.1.0",
"oracle 8.1.7.4","PostgreSQL Ver. 8.3.5","PostgreSQL Ver. 8.1.8","oracle 9.2.0.1","PostGreSQL v 9.1.2",
"PostgreSQL Ver. 9.2.4","oracle 7.3.4.2","PostgreSQL Ver. 8.1.17","oracle  9.2.0.3.0","oracle 9.2.0.8",
"MySql 5.5.30","PostgreSQL Ver. 9.3.2","oracle 9.2.0.3.0","Oracle 9.2.0.8","oracle 9.2.0.4","oracle 9.2.0.8.0",
"MariaDB 5.5.32","oracle 9.2.0.4.0","oracle  9.2.0.6.0","postgres-8.1","PostgreSQL Ver. 8.1.9","oracle 8.1.7.2",
"PostgreSQL Ver. 9.2.8","PostgreSQL Ver. 9.1.4","MySql  4.1.11","MySql 5.0.77","PostGreSQL v 9.4.6",
"oracle 10.2.0.4.0","MySql 5.1.63","MariaDB 5.5.33","PostgreSQL Ver. 8.1.19","oracle 9.2.0.6.0",
"PostgreSQL Ver. 8.3","PostGreSQL v 9.0.5")

ESTRUCTURA = ('config', 'tnsnames', 'listener', 'estructura tablespaces',
              'estructura datafiles', 'filesystem', 'respaldo', 'crontab')
      
def utftolatin(text):
    try:
        return unicode(text, "utf-8").encode("latin-1")
    except TypeError:
        # None es ""
        return ""

# Formata moeda ###
def Money(price, formated=True):
	"""
	>>> print Money(10000)
	$ 10.000,00
	>>> print Money(10000,False)
	10.000,00
	"""
	SafeLocale()
	from locale import currency
	if price:
		if formated:
			return SPAN('Bs. %s' % currency(price, grouping=True, symbol=False), _class="montos")
		else:
			return currency(price, grouping=False, symbol=False).replace(',','')
	else:
		return SPAN('Bs. %s' % currency(price, grouping=True, symbol=False), _class="montos")

    
def Date(data,formato=1):
    from datetime import datetime
    """    
    >>> SafeLocale()
    >>> from datetime import datetime
    >>> date = datetime.strptime('2010-08-01','%Y-%m-%d')
    >>> print Date(date)
    01/08/2010
    >>> print Date(date,2)
    Sun, 01 Aug of 2010
    >>> print Date(date,3)
    Sunday, 01 august of 2010
    """
    if formato == 2:
        format="%a, %d %b of %Y"
    elif formato == 3:
        format="%A, %d %B of %Y"
    else:
        format="%d/%m/%Y"
        
    return data.date().strftime(format)
	
	
def radioboxes(field,value):
    items=[DIV(name,INPUT(_type='radio',_value=key,_name=field.name,value=value))
           for key,name in field.requires.options()]
    return DIV(*items)

import datetime
week = datetime.timedelta(days=7)


# def fullname(user_id):
#    if user_id is None:
#        return "Unknown"s
#    return "%(first_name)s %(last_name)s (id:%(id)s)" % db.auth_user(user_id)


def show_status(status,row=None):
    return SPAN(status,_class=status)

if auth.is_logged_in():
   me=auth.user.id
else:
   me=None

#---- audita visitas a la aplicacion --------------------------------
# default timeout is 2 minutes
     
import datetime
     
VISITED_TIMEOUT = datetime.timedelta(0, 0, 0, 0, 2)
     
if not session.visited:
	session.visited = dict()
     
session.visited.update({request.url: request.now})
     
def recently_visited(a, c, f):
	url = URL(a=request.application, c=c, f=f)
	if url in session.visited:
		if request.now - session.visited[url] < VISITED_TIMEOUT:
			return True
	return False
#--------------------------------------------------------------------

db.define_table('company',
    Field('name'),
    Field('url'),
    Field('address'),
    Field('phone'),
    Field('fax'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False))

db.company.name.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'company.name')]
db.company.url.requires=IS_EMPTY_OR(IS_URL())
db.company.phone.requires=is_phone
db.company.fax.requires=is_phone

db.define_table('persona',
    Field('name'),
    Field('company',db.company),
    Field('role'),
    Field('address'),
    Field('phone'),
    Field('email'),
    Field('ext'),
    Field('fax'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False),
    format='%(nombre)s',
    migrate=migrate)


db.persona.name.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'persona.name'),IS_UPPER()]
db.persona.company.requires=IS_IN_DB(db,'company.id','%(name)s')
db.persona.phone.requires=is_phone
db.persona.fax.requires=is_phone


##- control de actividades ---------------------------------------------


db.define_table('proyectos',
	Field('descri', 'string', label='Descripcion'),
	Field('status', 'string',default='POR REALIZAR'),
	Field('gerencia', 'string', default='PM'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False,label=T('Creado por'),),
    Field('created_on','date',default=request.now,writable=False,readable=False,label=T('Creado en')),
	format='%(descri)s',
	migrate=True)
db.proyectos.descri.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'proyectos.descri')]
db.proyectos.status.requires=IS_IN_SET(STATUS_PROYECTO)
dpto=['PM','ALM','COR']
db.proyectos.gerencia.requires=IS_IN_SET(dpto)
db.proyectos._plural='Proyectos'
db.proyectos._singular='Proyecto'
db.proyectos.status.represent = show_status


db.define_table('asignacion',
	Field('cod_proyecto', db.proyectos),
	Field('analista', db.auth_user),
	Field('fecha_asig','date',  label='Fecha Asignacion'),
	Field('fecha_vcto','date',  label='Fecha de Vencimiento'),
	Field('prioridad','string', default='NORMAL'),
	Field('status','string', default='NO INICIADO'),
	Field('porc_completado', 'double', default=0.00),
	Field('horas_ejecutadas', 'double', default=0.00),
	format='%(analista)s',
	migrate=True)
	
db.asignacion.porc_completado.represent = formato_montos
db.asignacion.horas_ejecutadas.represent = formato_montos
db.asignacion.cod_proyecto.requires = IS_IN_DB(db,'proyectos.id','%(descri)s')
db.asignacion._plural='Asignaciones'
db.asignacion._singular='Asignacion'
db.asignacion.prioridad.requires=IS_IN_SET(PRIORIDAD)
db.asignacion.status.requires=IS_IN_SET(STATUS_ASIG)
db.asignacion.analista.requires = IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s',zero=T('<Empty>'))


db.define_table('actividades',
	Field('cod_asig', db.asignacion, requires = IS_IN_DB(db,'asignacion.id','%(cod_proyecto.descri)s %(analista)s')),
	Field('descripcion', 'text', requires=CLEANUP(''), 
	notnull=False,length=600, label='Actividades'),
	Field('fecha_inicio','date', notnull=True,default=request.now, label='Fecha'),
	Field('hora_inicio','string', notnull=True, default='08:00 AM',  label='Hora inicio de Ejecución'),
	Field('hora_fin','string', notnull=True, default='11:58 AM',  label='Hora fin de Ejecución'),
	Field('horas_diurnas','double', default=0.00),
	Field('horas_nocturnas','double', default=0.00),
	Field('horas_diurnas_r','double', default=0.00),
	Field('horas_nocturnas_r','double', default=0.00),
	Field('tipo', 'string',  label='Tipo', default='P',requires=IS_IN_SET(TIPO_ACT)),
	Field('producto','string', default='CORREO', requires=IS_IN_SET(['INFORME','CORREO','DOCUMENTO','CC','WHATSAPP'])),
	Field('completado', 'string', default='NO COMPLETADA', requires=IS_IN_SET(['COMPLETADA','NO COMPLETADA'])),
	format='%(cod_asig)s ',
	migrate=True)

#db.actividades.descripcion.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'actividades.descripcion')]
db.actividades.horas_diurnas.represent = formato_montos
db.actividades.cod_asig.requires = IS_IN_DB(db,'asignacion.id','%(cod_proyecto)s %(analista)s')
db.actividades._plural='Actividades'
db.actividades._singular='Actividad'

#db.actividades.porc_completado.requires =  [ IS_FLOAT_IN_RANGE(0, 100), error_message='must be prime and less than 10']
#db.actividades.descripcion.requires=[IS_NOT_EMPTY(),IS_UPPER()]


#--------------------------------- solutor delta -----------------------------------

db.define_table('ambiente',
    Field('descri',label=T('Descripcion')), auth.signature,
    format='%(descri)s',
    migrate=migrate)
db.ambiente.descri.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'ambiente.descri'),IS_UPPER()]
db.ambiente._plural='Ambientes'
db.ambiente._singular='Ambiente'


db.define_table('subproyectos',
	Field('descri', 'string', length=60, label='Descripcion', represent=lambda x: MARKMIN(x),required=True),
	Field('proyecto', db.proyectos),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False,label=T('Creado por'),),
    Field('created_on','date',default=request.now,writable=False,readable=False,label=T('Creado en')),

	format='%(descri)s',
	migrate=True)
#db.subproyectos.descri.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'subproyectos.descri')]
db.subproyectos._plural='Subproyectos'
db.subproyectos._singular='Subproyecto'



#---------------------------------------------------------------------



db.define_table('task',
    Field('title'),
    Field('task_type'),
    Field('persona',db.auth_user,default=None),
    Field('description','text'),
    Field('start_time','date'),
    Field('stop_time','date'),
    Field('status','string', default='PENDIENTE'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False,label=T('Creado por'),),
    Field('created_on','date',default=request.now,writable=False,readable=False,label=T('Creado en')),
    format='%(title)s - %(status)s',
    migrate=migrate)

db.task.title.requires=IS_NOT_EMPTY()
db.task.task_type.requires=IS_IN_SET(TASK_TYPES)

db.task.persona.requires=IS_IN_DB(db,'auth_user.id','%(first_name)s')
db.task.start_time.default=request.now
db.task.stop_time.default=request.now
db.task.status.requires=IS_IN_SET(STATUS_TAREA)

db.task.created_on.represent = lambda v,row: prettydate(v)
db.task.start_time.represent = lambda v,row: SPAN(prettydate(v),_class='overdue' if v and v<datetime.date.today() else None)
db.task.stop_time.represent = lambda v,row: SPAN(prettydate(v),_class='overdue' if v and v<datetime.date.today() else None)


db.define_table('bitacora',
    Field('persona',db.persona),
    Field('body','text'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False),
    format='%(body)s',
    migrate=migrate)

db.bitacora.persona.requires=IS_IN_DB(db,'persona.id','%(name)s')
db.bitacora.body.requires=IS_NOT_EMPTY()


db.define_table('ubicacion',
    Field('descri',label=T('Descripcion')), 
    Field('created_by',db.auth_user,default=me,writable=False,readable=False,label=T('Creado por'),),
    Field('created_on','date',default=request.now,writable=False,readable=False,label=T('Creado en')),
    auth.signature,
    format='%(descri)s',
    migrate=migrate)
    
db.ubicacion.descri.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'ubicacion.descri'),IS_UPPER()]
db.ubicacion._plural='Area/Ubicacion'
db.ubicacion._singular='Area/Ubicacion'



db.define_table('so',
    Field('descri',label=T('Descripcion')), 
    Field('created_by',db.auth_user,default=me,writable=False,readable=False,label=T('Creado por'),),
    Field('created_on','date',default=request.now,writable=False,readable=False,label=T('Creado en')),
    auth.signature,
    format='%(descri)s',
    migrate=migrate)
db.so.descri.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'so.descri'),IS_UPPER()]
db.so._plural='S.O.'
db.so._singular='S.O.'


db.define_table('almacen',
	Field('descri'),
	format='%(descri)s',
    migrate=True, redefine=redefine)
db.almacen.descri.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'almacen.descri'),IS_UPPER()]


db.define_table('tipo_equipos',
	Field('descri'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False,label=T('Creado por'),),
    Field('created_on','date',default=request.now,writable=False,readable=False,label=T('Creado en')),
	format='%(descri)s',
    migrate=True, redefine=redefine)
db.tipo_equipos.descri.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'tipo_equipos.descri'),IS_UPPER()]

db.define_table('servidores',
	Field('tipo_equipo', db.tipo_equipos, ondelete='RESTRICT'),
	Field('almacen', db.almacen, ondelete='RESTRICT'),
    Field('nombre'),
    Field('ip'),
    Field('rac'),
    Field('ambiente_id', db.ambiente, ondelete='RESTRICT'),
    Field('so_id', db.so, ondelete='RESTRICT'),
    Field('tipoconex'),
    Field('status_mon', type='string',label=T('Monitoreado')),
    Field('criticidad', label=T('criticidad')),
    Field('dominio'),
    Field('obs','text'),
    Field('mtto_logs','text', default='MTTO-NO'),
    Field('nombre_alias', type='string',label=T('Alias Scan')),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False, ondelete='RESTRICT'),
    Field('created_on','datetime',default=request.now,writable=False,readable=False),
    Field('status','text', default='OPERATIVO'),
    auth.signature,
    format='%(nombre)s',
    migrate=migrate)
    
db.servidores.id.readable=db.servidores.id.writable=False
db.servidores.rac.default="CLUSTER-NO"
db.servidores.rac.requires=IS_IN_SET(RAC)
db.servidores.tipoconex.requires=IS_IN_SET(TIPOCONEX)
#db.servidores.dominio.requires=IS_IN_SET(DOMINIO)
db.servidores.status.requires=IS_IN_SET(STATUS_SERVIDOR)
db.servidores.criticidad.default="ALTA"
db.servidores.criticidad.requires=IS_IN_SET(CRITICIDAD)
db.servidores.so_id.default=16
db.servidores.so_id.requires=IS_IN_DB(db,'so.id','%(descri)s')
db.servidores.ambiente_id.default=4
db.servidores.ambiente_id.requires=IS_IN_DB(db,'ambiente.id','%(descri)s')
db.servidores.nombre.requires=[IS_NOT_EMPTY(),IS_UPPER()]
db.servidores.nombre.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db, 'servidores.nombre'),IS_UPPER()]
db.servidores.tipoconex.default="SSH"
db.servidores.status_mon.requires=IS_IN_SET(STATUS_MON)
db.servidores.status_mon.default="NO"
db.servidores.status_mon.represent = show_status
db.servidores.mtto_logs.default="MTTO-NO"
db.servidores.mtto_logs.requires=IS_IN_SET(STATUS_MTTO)
db.servidores.mtto_logs.represent = show_status
db.servidores.nombre_alias.represent = show_status
db.servidores.tipo_equipo.default=19
db.servidores.tipo_equipo.requires=IS_IN_DB(db,'tipo_equipos.id','%(descri)s')
db.servidores.almacen.requires=IS_IN_DB(db,'almacen.id','%(descri)s')

db.define_table('tipobd',
    Field('descri',label=T('Descripcion')), 
    Field('created_by',db.auth_user,default=me,writable=False,readable=False,label=T('Creado por'),),
    Field('created_on','date',default=request.now,writable=False,readable=False,label=T('Creado en')),
    #Field('orden', type='integer'),
    auth.signature,
    format='%(descri)s',
    migrate=migrate)

db.tipobd.descri.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'tipobd.descri')]
db.tipobd._plural='Tipos de Base de Datos'
db.tipobd._singular='Tipo de Base de Datos'



db.define_table('ver',
    Field('descri',label=T('Descripcion')), 
    Field('created_by',db.auth_user,default=me,writable=False,readable=False,label=T('Creado por'),),
    Field('created_on','date',default=request.now,writable=False,readable=False,label=T('Creado en')),
    auth.signature,
    format='%(descri)s',
    migrate=migrate)
db.ver.descri.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'ver.descri'),IS_UPPER()]
db.ver._plural='veres'
db.ver._singular='ver'

db.define_table('estadobd',
    Field('descri',label=T('Descripcion')), 
    Field('created_by',db.auth_user,default=me,writable=False,readable=False,label=T('Creado por'),),
    Field('created_on','date',default=request.now,writable=False,readable=False,label=T('Creado en')),
    auth.signature, format='%(descri)s',

    migrate=migrate)
db.estadobd.descri.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'estadobd.descri'),IS_UPPER()]
db.estadobd._plural='Estatus'
db.estadobd._singular='Estatus'

#-------------------------------------------------------------------------------------------
db.define_table('custodios_appl',
	Field('nombres'),
	Field('cargo'),
	Field('extension'),
	format='%(nombres)s',
	migrate=migrate
)
db.custodios_appl.nombres.requires=[IS_UPPER(),IS_NOT_IN_DB(db,'custodios_appl.nombres'),IS_NOT_EMPTY()]

db.define_table('basedatos',
	Field('nombre'),
	Field('servidor',db.servidores, ondelete='CASCADE'),
	Field('tipobd_id', db.tipobd, ondelete='RESTRICT'),
	Field('version_id', db.ver, ondelete='RESTRICT'),
	Field('puerto'),
	Field('quien_creo', db.auth_user, ondelete='RESTRICT'),
	Field('estado_id', db.estadobd, ondelete='RESTRICT'),
	Field('criticidad'),
	Field('appl','text'),
	Field('home'),
	Field('ambiente_id', db.ambiente, ondelete='RESTRICT'),
	Field('binario', default='32 BITS'),
	Field('asm', default='ASM-NO'),
	Field('fecha_creacion', 'date'),
	Field('soft_respaldo', type='string',label=T('Software de Respaldo'), default='NETWORKER'),
	Field('f_cambio_netw_veritas', 'date'),
	Field('status_mon', type='string',label=T('Monitoreada'), default='NO'),
	Field('obs','text', label='Observacion',comment=A('Sintaxis de la observacion',_href='http://web2py.com/examples/static/markmin.html')),
	Field('created_by',db.auth_user,default=me,writable=False,readable=False, ondelete='RESTRICT'),
	Field('created_on','datetime',default=request.now,writable=False,readable=False),
	auth.signature,
	format='%(nombre)s',
	migrate=migrate, redefine=redefine
	#primarykey=['db.basedatos.id','db.basedatos.servidor']
	)

db.basedatos.id.readable=db.basedatos.id.writable=False
db.basedatos._plural='Base de datos'
db.basedatos._singular='Base de datos'
db.basedatos.nombre.requires=[IS_NOT_EMPTY(),IS_UPPER()]
db.basedatos.servidor.requires=IS_IN_DB(db,'servidores.id','%(nombre)s')
db.basedatos.tipobd_id.default=9
db.basedatos.tipobd_id.requires=IS_IN_DB(db,'tipobd.id','tipobd.descri')
db.basedatos.estado_id.default=4
db.basedatos.estado_id.requires=IS_IN_DB(db,'estadobd.id','estadobd.descri')
db.basedatos.version_id.requires=IS_IN_DB(db,'ver.id','ver.descri')
db.basedatos.quien_creo.default=me
db.basedatos.quien_creo.requires=IS_IN_DB(db,'auth_user.id','auth_user.first_name')
db.basedatos.ambiente_id.default=4
db.basedatos.ambiente_id.requires=IS_IN_DB(db,'ambiente.id','%(descri)s')
db.basedatos.criticidad.default="ALTA"
db.basedatos.criticidad.requires=IS_IN_SET(CRITICIDAD)
db.basedatos.binario.requires=IS_IN_SET(BINARIO)
db.basedatos.binario.widget = SQLFORM.widgets.radio.widget
db.basedatos.asm.requires=IS_IN_SET(ASM)
db.basedatos.asm.widget = SQLFORM.widgets.radio.widget
db.basedatos.status_mon.requires=IS_IN_SET(STATUS_MON)
db.basedatos.soft_respaldo.default="FILESYSTEM"
db.basedatos.soft_respaldo.requires=IS_IN_SET(SOFT_RESPALDO)
db.basedatos.status_mon.default="NO"
db.basedatos.status_mon.represent = show_status
db.basedatos.soft_respaldo.represent = show_status
db.basedatos.fecha_creacion.default=request.now



db.define_table('actividades_sd',
	Field('cod_proy', db.proyectos, ondelete='RESTRICT'),
	Field('cod_subp', db.subproyectos, ondelete='RESTRICT'),
	Field('cod_servidor', db.servidores, ondelete='RESTRICT'),
	Field('cod_bd', db.basedatos, ondelete='RESTRICT'),
	Field('descripcion', 'text', requires=CLEANUP(''),notnull=False,length=600, label='Actividades'),
	Field('fecha_inicio','datetime', notnull=True,default=request.now, label='Fecha hora inicio actividad'),
    Field('fecha_fin','datetime', notnull=True,default=request.now, label='Fecha hora fin actividad'),
	Field('horas_laboradas','double', default=0.00),
    Field('horas_extras','double', default=0.00),
	Field('tipo', 'string',  label='Tipo', default='P',requires=IS_IN_SET(TIPO_ACT)),
	Field('producto','string', default='CORREO', requires=IS_IN_SET(['INFORME','CORREO','DOCUMENTO','CC','WHATSAPP','LLAMADA'])),
	Field('completado', 'string', default='ABIERTA', requires=IS_IN_SET(['ABIERTA','CERRADA','ABIERTA CON SUBACTIVIDADES'])),
	Field('ambiente_id', db.ambiente, ondelete='RESTRICT'),
	Field('analista', db.auth_user, ondelete='RESTRICT'),
    Field('incid_bd', type='boolean', default=False),
    Field('incid_otros', type='boolean', default=False),
    Field('obs_otros', type='text', length=300, lable='Observaciones incidencia otros', default=False),
    Field('bd_afecta', type='boolean', default=False),
    Field('otros_afecta', type='boolean', default=False),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False,label=T('Creado por')),
    Field('created_on','date',default=request.now,writable=False,readable=False,label=T('Creado en')),
    Field('fecha_cierre','date', default=None, label='Fecha_cierre'),
    Field('cerrada_por',db.auth_user,default=me,writable=False,readable=False,label=T('cerrada por')),
    
    format='%(analista)s',
	migrate=True)

db.actividades_sd.ambiente_id.requires=IS_IN_DB(db,'ambiente.id','%(descri)s')
db.actividades_sd.analista.requires = IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s',zero=T('<Empty>'))
#db.actividades_sd.descripcion.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'actividades_sd.descripcion')]
db.actividades_sd._plural='Actividades'
db.actividades_sd._singular='Actividad'


db.define_table('subactividades_sd',
    Field('actividad_id', db.actividades_sd, ondelete='RESTRICT'),
    Field('cod_proy', db.proyectos, ondelete='RESTRICT'),
    Field('cod_subp', db.subproyectos, ondelete='RESTRICT'),
    Field('cod_servidor', db.servidores, ondelete='RESTRICT'),
    Field('cod_bd', db.basedatos, ondelete='RESTRICT'),
    Field('descripcion', 'text', requires=CLEANUP(''),notnull=False,length=600, label='Actividades'),
    Field('fecha_inicio','datetime', notnull=True,default=request.now, label='Fecha hora actividad'),
    Field('fecha_fin','datetime', notnull=True,default=request.now, label='Fecha hora fin actividad'),
    Field('horas_laboradas','double', default=0.00),
    Field('horas_extras','double', default=0.00),
    Field('tipo', 'string',  label='Tipo', default='P',requires=IS_IN_SET(TIPO_ACT)),
    Field('producto','string', default='CORREO', requires=IS_IN_SET(['INFORME','CORREO','DOCUMENTO','CC','WHATSAPP','LLAMADA'])),
    Field('completado', 'string', default='ABIERTA', requires=IS_IN_SET(['ABIERTA','CERRADA'])),
    Field('analista', db.auth_user, ondelete='RESTRICT'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False,label=T('Creado por'),),
    Field('created_on','date',default=request.now,writable=False,readable=False,label=T('Creado en')),
    format='%(analista)s',
    migrate=True)

db.subactividades_sd.analista.requires = IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s',zero=T('<Empty>'))
db.subactividades_sd.actividad_id.requires=IS_IN_DB(db,db.actividades_sd.id,'%(descripcion)s')
db.subactividades_sd._plural='SubActividades'
db.subactividades_sd._singular='SubActividad'


db.define_table('log_actividades_sd',
    Field('actividad', db.actividades_sd),
    Field('analista', db.auth_user),
    Field('fecha','datetime',default=request.now,writable=False,readable=False,label=T('fecha')),
    Field('status', 'string'),
    format='%(analista)s',
    migrate=True)
    

#-------------------------------------------------------------------------------------------
db.define_table('matriz_respaldo',
	Field('servidor_id',db.servidores),
	Field('basedatos_id',db.basedatos),
	Field('descri','string'),
	Field('tipo_backup','string',length=10),
	Field('b_archive','string', length=1),
	Field('ret_b_archive','string', length=5),
	Field('b_full','string',length=1),
	Field('ret_b_full','string',length=5),
	Field('b_full_boveda_sem','string',length=1),
	Field('ret_b_full_boveda_sem','string',length=5),
	Field('b_full_boveda_men','string',length=1),
	Field('ret_b_full_boveda_men','string',length=5),
	Field('networker','string',length=10),
	Field('rman_ver','string',length=10),
	format='%(descri)s',
    migrate=migrate)

db.matriz_respaldo.servidor_id.requires = IS_IN_DB(db,'servidores.id','%(nombre)s')
db.matriz_respaldo.basedatos_id.requires = IS_IN_DB(db,'basedatos.id','%(nombre)s')
db.matriz_respaldo.tipo_backup.requires=IS_IN_SET(TIPO_BACKUP)


#-------------------------------------------------------------------------------------------
db.define_table('tipo_politica_resp',
    Field('descri',label=T('Descripcion')), auth.signature,
    format='%(descri)s',
    migrate=migrate)
db.tipo_politica_resp.descri.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'tipo_politica_resp.descri'),IS_UPPER()]
db.tipo_politica_resp._plural='Tipo Politica Respaldo'
db.tipo_politica_resp._singular='Tipo Pol Resp'
# #-------------------------------------------------------------------------------------------
# db.define_table('matriz_politica_resp',
	# Field('servidor_id',db.servidores),
	# Field('basedatos_id',db.basedatos),
	# Field('descri','string'),
	# Field('tipo_backup','string',length=10),
	# Field('tipo_politica_resp_id',db.tipo_politica_resp),
	# Field('retencion','string', length=5),
	# format='%(descri)s',
    # migrate=migrate)

# db.matriz_politica_resp.servidor_id.requires = IS_IN_DB(db,'servidores.id','%(nombre)s')
# db.matriz_politica_resp.basedatos_id.requires = IS_IN_DB(db,'basedatos.id','%(nombre)s')
# db.matriz_politica_resp.basedatos_id.requires = IS_IN_DB(db,'tipo_politica_resp.id','%(descri)s')

#-------------------------------------------------------------------------------------------
db.define_table('basedatos_estructura',
	Field('nombre','string'),
	Field('tbs'),
	Field('datafiles'),
	Field('espacio', type='double'),
	Field('sp_ocupado', type='double'),
	Field('sp_libre', type='double'),
	Field('porc_ocupado', type='string'),
	Field('porc_libre', type='double'),
	Field('fecha_act','datetime'),
	format='%(nombre)s',
    migrate=True
    )

#-------------------------------------------------------------------------------------------

db.define_table('custodios_bd_appl',
	Field('basedatos_id',db.basedatos),
	Field('custodio_id',db.custodios_appl),
	Field('created_by',db.auth_user,default=me,writable=False,readable=False),
	Field('created_on','datetime',default=request.now,writable=False,readable=False),
	auth.signature,
    migrate=migrate)

db.custodios_bd_appl.basedatos_id.requires = IS_IN_DB(db,'basedatos.id','%(nombre)s')
db.custodios_bd_appl.custodio_id.requires = IS_IN_DB(db,'custodios_appl.id','%(nombres)s')

#-------------------------------------------------------------------------------------------

db.define_table('esquemas',
	Field('basedatos_id',db.basedatos),
	Field('nombre'),
	Field('created_by',db.auth_user,default=me,writable=False,readable=False),
	Field('created_on','datetime',default=request.now,writable=False,readable=False),
	auth.signature,
	format='%(nombre)s',
    migrate=migrate)

db.esquemas.basedatos_id.requires = IS_IN_DB(db,'basedatos.id','%(nombre)s')

#-------------------------------------------------------------------------------------------

db.define_table('cuentas_so',
	Field('servidor_id',db.servidores),
	Field('cuenta'),
	Field('clave'),
	Field('clave_anterior'),
	Field('created_by',db.auth_user,default=me,writable=False,readable=False),
	Field('created_on','datetime',default=request.now,writable=False,readable=False),
	auth.signature,
	format='%(cuenta)s',
    migrate=migrate)

db.cuentas_so.servidor_id.requires = IS_IN_DB(db,'servidores.id','%(nombre)s')
#-------------------------------------------------------------------------------------------

db.define_table('log_cuentas_so',
    Field('cuenta_so_id',db.cuentas_so),
    Field('body','text', represent=lambda x: MARKMIN(x),
          comment='Registro de actividades o novedades'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False),
    auth.signature,
    format='%(id)s',
    migrate=migrate)

db.log_cuentas_so.cuenta_so_id.requires=IS_IN_DB(db,'cuentas_so.id','%(cuenta)s')
db.log_cuentas_so.body.requires=IS_NOT_EMPTY()





def servidor(serv_id):
    if serv_id is None:
        return "Unknown"
    return "%(nombre)s (id:%(id)s)" % db.servidores(serv_id)


db.define_table('admin_basedatos',
	Field('admin_id',db.auth_user),
	Field('servidor_id',db.servidores),
	Field('basedatos_id',db.basedatos),
	Field('fch_asignacion','date'),
	Field('observacion','text', widget=SQLFORM.widgets.text.widget),
	Field('created_by',db.auth_user,default=me,writable=False,readable=False),
	Field('created_on','datetime',default=request.now,writable=False,readable=False),
	auth.signature,
	format='%(admin_id)s',
    migrate=migrate)



#db.admin_basedatos.basedatos_id.widget = cascade.widget

db.admin_basedatos.admin_id.requires = IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s',zero=T('<Empty>'))
db.admin_basedatos.basedatos_id.requires = IS_IN_DB(db,'basedatos.id',db.basedatos._format)
#db.admin_basedatos.basedatos_id.represent = lambda basedatos_id: db.basedatos(basedatos_id).id 

#db.admin_basedatos.basedatos_id.requires = IS_IN_DB(db,'basedatos.id','%(nombre)s',distinct=True)

db.define_table('task_basedatos',
    Field('basedatos',db.basedatos,default=None),
    Field('titulo'),
    Field('task_type'),
    Field('start_time','datetime'),
    Field('end_time','datetime'),
    Field('duracion','string'),
    Field('description','text', represent=lambda x: MARKMIN(x)),
    Field('solucion','text', represent=lambda x: MARKMIN(x)),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False),
    auth.signature,
    format='%(titulo)s',
    migrate=migrate)

db.task_basedatos.titulo.requires=IS_NOT_EMPTY()
db.task_basedatos.task_type.requires=IS_IN_SET(TASK_BASEDATOS_TYPES)
db.task_basedatos.basedatos.requires=IS_IN_DB(db,'basedatos.id','%(nombre)s')
db.task_basedatos.start_time.default=request.now
db.task_basedatos.end_time.default=request.now



db.define_table('log_basedatos',
    Field('basedatos',db.basedatos),
    Field('body','text',
          comment='Registro de actividades o novedades'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False),
    auth.signature,
    format='%(basedatos)s',
    migrate=migrate)

db.log_basedatos.basedatos.requires=IS_IN_DB(db,'basedatos.id','%(nombre)s')
db.log_basedatos.body.requires=IS_NOT_EMPTY()

        
db.define_table('documentos',
	Field('basedatos',db.basedatos),
	Field('estructura', requires=IS_IN_SET(ESTRUCTURA), default="config"),
	Field('body','text', represent=lambda x: MARKMIN(x),required=True),
	#Field('file','upload'),
	Field('created_by',db.auth_user,default=me,writable=False,readable=False),
	Field('created_on','datetime',default=request.now,writable=False,readable=False),
	auth.signature,
	format='%(basedatos)s',
	migrate=migrate
)
db.documentos.basedatos.requires=IS_IN_DB(db,'basedatos.id','%(nombre)s')



db.define_table('bdmon',
	Field('f_corrida','date', default=request.now),
    Field('tx_ambiente','string'),
    Field('tx_servidor','string'),
    Field('tx_tipobd','string'),
    Field('tx_puerto','string'),
    Field('tx_instancia','string'),
    Field('tx_rutina', 'string'),
    Field('tx_comando', 'text'),
    Field('tx_resultado', type='text'),
    Field('tx_resultado_detalle', type='text'),
    Field('status', type='string'),
    Field('created_on','datetime',default=request.now,writable=False,readable=False),
    auth.signature,
    format='%(f_corrida)s',
    migrate=migrate)


db.define_table('rutinas',
    Field('nombre', 'string', required=True, label='Nombre de la rutina'),
    Field('descripcion', 'text', label='Descripción',
        represent=lambda x: MARKMIN(x), 
        widget=lambda field, value: SQLFORM.widgets.text.widget(field, value, _rows=5, _cols=150)),
    Field('sql_code', 'text', required=True, label='Código SQL',
        represent=lambda x: MARKMIN(x), 
        unique=True,
        widget=lambda field, value: SQLFORM.widgets.text.widget(field, value, _rows=15, _cols=150)),
    Field('activo', 'boolean', default=True, label='Activo'),
    auth.signature,
    format='%(nombre)s',
    migrate=migrate)


db.rutinas.sql_code.requires = IS_NOT_EMPTY()


STATUS = ("HABILITADO","DESHABILITADO")
TIPO_COMANDO = ("BD","SO")

db.define_table("rutina_status",
	Field("rutina", db.rutinas),
	Field("servidor_id",db.servidores),
	Field("tipobd_id",db.tipobd,default=9),
	Field("status",type="string",default="HABILITADO", requires=IS_IN_SET(STATUS)),
	Field("resaltado",type="string",default="SI",requires=IS_IN_SET(SN)),
	
	auth.signature,
	format='%(rutina)s',
    migrate=migrate)

db.rutina_status.rutina.requires=IS_IN_DB(db,'rutinas.id','rutinas.nombre')
db.rutina_status.servidor_id.requires=IS_IN_DB(db,'servidores.id','servidores.nombre')
db.rutina_status.tipobd_id.requires=IS_IN_DB(db,'tipobd.id','tipobd.descri')
db.rutina_status._plural='Rutinas'
db.rutina_status._singular='Rutina'

db.rutina_status.status.represent = show_status

#requires = IS_DATE(format=('%Y-%m-%d')),



db.define_table('tipo_guardia',
    Field('descri',label=T('Descripcion')), auth.signature,
    format='%(descri)s',
    migrate=migrate)
db.tipo_guardia.descri.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'tipo_guardia.descri'),IS_UPPER()]
db.tipo_guardia._plural='Tipo de Guardia'
db.tipo_guardia._singular='Tipos de Guardias'


db.define_table('guardias',
    Field('id','id'),  
    Field('tipo_guardia', db.tipo_guardia),     
    Field('f_fch_inicio',  'date',
          label=T('Fecha Inicio')),
    Field('f_fch_fin',  'date',
          label=T('Fecha Fin')),
	Field('f_quien_toca', 'reference auth_user', 
          label=T('A quien le toca')),
    Field('f_backup', 'reference auth_user', 
          label=T('Backup')),
    Field('registrado_tso', 'string', requires=IS_IN_SET(REGISTRO),
          label=T('TSO_GUARDIAS')),
    Field('created_on','date',default=request.now,
          label=T('Created On'),writable=False,readable=False),
    Field('modified_on','date',default=request.now,
          label=T('Modified On'),writable=False,readable=False,
          update=request.now),
    Field('created_by',db.auth_user,default=auth.user_id,
          label=T('Created By'),writable=False,readable=False),
    Field('modified_by',db.auth_user,default=auth.user_id,
          label=T('Modified By'),writable=False,readable=False,
          update=auth.user_id), 
    migrate=migrate
    )

db.guardias.id.readable=db.guardias.id.writable=False

db.guardias.tipo_guardia.requires=IS_IN_DB(db,'tipo_guardia.id','tipo_guardia.descri')    
db.guardias.f_quien_toca.requires = IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s',zero=T('<Empty>'))
db.guardias.f_backup.requires = IS_IN_DB(db,db.auth_user.id,'%(first_name)s %(last_name)s',zero=T('<Empty>'))
db.guardias.registrado_tso.represent = show_status

db.guardias.created_on.represent = lambda v,row: prettydate(v)
#db.guardias.f_fch_inicio.represent = lambda v,row: SPAN(prettydate(v),_class='overdue' if v and v<datetime.date.today() else None)
#db.guardias.f_fch_fin.represent = lambda v,row: SPAN(prettydate(v),_class='overdue' if v and v<datetime.date.today() else None)

db.guardias._plural='Guardias'
db.guardias._singular='Guardia'



task_guardias = db.define_table('task_guardias',
    Field('task_type',label='Tipo de Tarea'),
    Field('title',label='Titulo'),
    Field('guardia_id',db.guardias,default=None),
    Field('start_time','datetime',label='Inicio'),
    Field('end_time','datetime',label='Fin'),
    Field('duracion','string'),
    Field('impacto','string'),
    Field('body','text',represent=lambda x: MARKMIN(x),comment='Descripcion',label='Texto'),
    Field('solucion','text',represent=lambda x: MARKMIN(x),comment='Registro de solucion'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','date',default=request.now,writable=False,readable=False),
    auth.signature,
    format='%(task_type)s',
    migrate=migrate)

db.task_guardias.title.requires=IS_NOT_EMPTY()
db.task_guardias.task_type.requires=IS_IN_SET(TASK_BASEDATOS_TYPES)
db.task_guardias.guardia_id.requires=IS_IN_DB(db,'guardias.id','%(f_quien_toca)s')
db.task_guardias.start_time.default=request.now
db.task_guardias.end_time.default=request.now
db.task_guardias.impacto.requires=IS_IN_SET(IMPACTO)

#db.task_guardias.created_on.represent = lambda v,row: prettydate(v)
#db.task_guardias.start_time.represent = lambda v,row: SPAN(prettydate(v),_class='overdue' if v and v<datetime.date.today() else None)
#db.task_guardias.end_time.represent = lambda v,row: SPAN(prettydate(v),_class='overdue' if v and v<datetime.date.today() else None)


#########################################################################
## Setup Auth Groups
#########################################################################

if db(db.auth_group.role=="admin").count() == 0:
    auth.add_group(role = 'admin')
    auth.add_group(role = 'dba')
    auth.add_group(role = 'consulta')
    auth.add_group(role = 'add_servidor')
    auth.add_group(role = 'add_basedatos')
    auth.add_group(role = 'system')
    auth.add_group(role = 'ADMINISTRADOR ORACLE')
    auth.add_group(role = 'ADMINISTRADOR POSTGRESQL')
    auth.add_group(role = 'ADMINISTRADOR MYSQL')
    auth.add_group(role = 'ADMINISTRADOR SQLSERVER')
    
    


# -------   wiki --------------------------------------------------------------------------

db.define_table('program',
    Field('name', length=1000, 
          represent=lambda x: MARKMIN(x), 
          unique=True,
          widget=lambda field, value: SQLFORM.widgets.text.widget(field, value, _rows=1, _cols=100)),
    format='%(name)s',
    migrate=migrate)
                
db.define_table('learning_goal',
                Field('program',db.program,writable=False,label='Titulo'),                
                Field('body','text', represent=lambda x: MARKMIN(x), label='Texto',comment=A('Sintaxis de la wiki',_href='http://web2py.com/examples/static/markmin.html')),
                #Field('f_what','list:string',label='Que'),
                #Field('f_how','list:string',label='Como'),
                #Field('examples','list:string',label='Ejemplos'),
                format='%(program)s',
                migrate=migrate)

if not db(db.program).count():
    programs=['Respaldo Oracle', 'Respaldo Mysql','Respaldo postgresql']
    for program in programs:
        db.program.insert(name=program)


db.define_table('oracle_tps',
    Field('fecha_hora', 'datetime', required=True),
    Field('hora', 'string', required=True),
    Field('tps', 'integer', required=True),
    Field('base_datos', 'string', required=True),
    migrate='oracle_tps.table'
)

#-----------------------------------------------


#---------------------reports fpdf


     
    # we change the scaffolding model a bit because of this issue
    # html: http://code.google.com/p/web2py/issues/detail?id=1338
    # the code below is a modified version of the function at
    # gluon.contrib.generics
     
def pyfpdf_from_html(html):
        import os
        from gluon.contrib.fpdf import FPDF, HTMLMixin
        def image_map(path):
            if path.startswith('/%s/static/' % request.application):
                return os.path.join(request.folder,
                                    path.split('/', 2)[2])
            return 'http%s://%s%s' % (request.is_https and 's' or '',
                                      request.env.http_host, path)
     
        class MyFPDF(FPDF, HTMLMixin):
            pass
     
        pdf = MyFPDF()
        pdf.add_page()
        pdf.write_html(html, image_map=image_map)
        return XML(pdf.output(dest='S'))


db.define_table('historico_metricas',
    Field('bdmon_id', 'reference bdmon'),
    Field('servidor', 'string'),
    Field('instancia', 'string'),
    Field('comando', 'text'),
    Field('resultado', 'double'),
    Field('detalle', 'text'),
    Field('fecha_hora', 'datetime'),
    Field('tipo', 'string'),  # Puede ser "automatico" o "manual"
    migrate=False)


db.define_table('external_db_connections',
    Field('name'),
    Field('tipobd_id', db.tipobd),
    Field('host'),
    Field('username'),
    Field('password', 'password'),  # Se guarda cifrado
    Field('database_name'),
    Field('port', 'integer'),
    Field('is_active', 'boolean', default=True),
)