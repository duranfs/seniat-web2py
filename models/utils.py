# coding: utf8
### required - do no delete# Define Locale
def SafeLocale():
    from locale import setlocale, LC_ALL
    try:
       #setlocale(LC_ALL,'en_US.UTF-8')
       setlocale(LC_ALL,'en_US.UTF-8')
    except:
       #setlocale(LC_ALL,'english')  
       setlocale(LC_ALL,'es_VE.UTF-8') 

def url(f,args=[]): return URL(r=request,f=f,args=args)

def button(text,action,args=[]):
    return SPAN('[',A(text,_href=URL(r=request,f=action,args=args)),']')

def link_person(person):
    return A(person.name,_href=url('view_person',person.id))

def link_guardias(persona):
		if persona:
			return A(persona.first_name+', '+persona.last_name,_href=url('view_guardias',persona.id))
		else:
			return ('')

def nombre_persona(persona):
	if persona is None:
		return ""
	return "%(first_name)s %(last_name)s" % db.auth_user(persona)

def nombre_proyecto(proy):
	if proy is None:
		return ""
	return "%(cod_proyecto.descri)s -  %(porc_completado)s " % db.asignacion(proy)

		
def estatus_relacion(relacion):
	if relacion:
		return ('PENDIENTE')
	else:
		return ('NO')
		
def link_basedatos(basedatos):
    return A(basedatos.nombre,_href=url('view_basedatos',basedatos.id))

def link_task_guardias(guardias):
    return A(guardias.start_time,_href=url('view_task_guardias',guardias.id))


# cuando da error de recursividad es que no existe el valor buscado en
# la base de datos

def link_company(company):
    return A(company.name,_href=url('view_company',company.id))


def link_servidor(servidor):
	return A(servidor.nombre,_href=url('view_servidor',servidor.id))

def link_servidor2(servidor):
	return A(servidor.nombre,_href=url('list_servidores',servidor.id))

def link_equipo(servidor):
	return A(servidor.tipo_equipo.descri,_href=url('list_servidores',servidor.id))

def link_basedatos2(basedatos):
	return A(basedatos.nombre,_href=url('list_basedatos',basedatos.id))

def link_servidor_desc(servidor):
	return A(servidor.nombre,_href=url('view_servidor',servidor.id))


def link_tipobd(basedatos):
    return A(basedatos.tipobd,_href=url('view_basedatos',basedatos.id))

def link_cuentabd(servidor):
	cant=db(db.basedatos.servidor==servidor).count()
	return (cant)

def link_cuentacust(basedato):
	cant=db(db.custodios_bd_appl.basedatos_id==basedato).count()
	return (cant)

def link_cuenta_cuentas_so(servidor):
	cant=db(db.cuentas_so.servidor_id==servidor).count()
	return (cant)

def link_cuentaesq(basedatos):
	cant=db(db.esquemas.basedatos_id==basedatos).count()
	return (cant)

def link_cuentaMatriz(basedatos):
	cant=db(db.matriz_respaldo.basedatos_id==basedatos).count()
	return (cant)

def link_cuentaMatrizPoliticaResp(basedatos):
	cant=db(db.matriz_politica_resp.basedatos_id==basedatos).count()
	return (cant)


def link_cuentaInstancias(fecha):
	cant=len(db(db.bdmon.f_corrida == fecha).select(db.bdmon.tx_instancia,distinct=True))  #forma1
	#cant=db.executesql('SELECT COUNT(DISTINCT tx_instancia) FROM bdmon;') #forma2  
	return (cant)

def link_cant_bd(servidor_id):
	import datetime
	cant=0
	#strptime(cmp, "%Y-%m-%d %H:%M:%S.%f")
	cant=db(db.basedatos.servidor==servidor_id).count()
	return A(cant)


def link_bdmon(basedatos, servidor):
	import datetime
	cant=0
	cant=db(db.bdmon.tx_instancia.upper()==basedatos.upper())(db.bdmon.tx_servidor.upper()==servidor.upper()).count()
	#if cant>1: cant=1
	return int(cant)

def link_bdmon_rutina(basedatos, servidor, rutina):
	import datetime
	cant=0
	cant=db(db.bdmon.tx_instancia.upper()==basedatos.upper())(db.bdmon.tx_servidor.upper()==servidor.upper())(db.bdmon.tx_rutina.like(rutina))\
	(db.bdmon.tx_resultado!='').count()
	#cant=db(db.bdmon.tx_instancia.upper()==basedatos.upper())(db.bdmon.tx_servidor.upper()==servidor.upper())(db.bdmon.tx_rutina.like('TBS_%')).count()
	#if cant>1: cant=1
	return int(cant)

def link_responsable(basedatos):
	basedatos_id=db(db.basedatos.nombre==basedatos).select(db.basedatos.id).first()
	responsable_id=db(db.admin_basedatos.basedatos_id==basedatos_id).select(db.admin_basedatos.admin_id).first()
	
	if responsable_id is None:
		return "Desconocido"
	else:
		nombre=db(db.auth_user.id==(responsable_id['admin_id'])).select(db.auth_user.first_name)
	return nombre

def busca_detalle_mon(basedatos):
	orden=db.bdmon.tx_rutina
	detalle=db(db.bdmon.tx_instancia==basedatos)(db.bdmon.f_corrida>=today).select(db.bdmon.tx_rutina,db.bdmon.tx_resultado,orderby=orden)
	#detalle=db(db.servidores.id>0).select()
	#etalle=db(db.bdmon.id>0).select()
	return A(detalle)

def nombre_servidor(servidor_id):
    if servidor_id is None:
        return "Unknown"
    return "%(nombre)s (id:%(id)s)" % db.servidores(servidor_id)

def nombre_basedatos(basedatos_id):
    if basedatos_id is None:
        return "Unknown"
    return "%(nombre)s (id:%(id)s)" % db.basedatos(basedatos_id)

def nombre_appl(bd, servidor_id):
	appl=db(db.basedatos.nombre==bd)(db.basedatos.servidor==servidor_id).select(db.basedatos.appl).first()
	return appl.appl

def nombre_tipobd(tipobd_id):
    if tipobd_id is None:
    	return "Unknown"
    return "%(descri)s" % db.tipobd(tipobd_id)



def datos_basedatos(basedatos, id_servidor):
	datos_basedatos=db(db.basedatos.nombre.upper()==basedatos.upper())(db.basedatos.servidor==id_servidor).select().first()
		
	if datos_basedatos is None:
		return "No existen datos para esa base de datos (datos_basedatos)"
	return datos_basedatos


def func_id_servidor(nombre):
	id_serv=db(db.servidores.nombre.upper()==nombre.upper()).select(db.servidores.id, distinct=True).first()
	return id_serv.id

def func_id_basedatos(nombre, id_servidor):
	basedatos=db(db.basedatos.nombre.upper()==nombre.upper())(db.basedatos.servidor==id_servidor).select(db.basedatos.id, distinct=True).first()
	if basedatos is None:
		return "BD no ha sido creada (func_id_basedatos)"
	return basedatos.id

def version_bd(basedatos, id_servidor):
	
	ver_id=db(db.basedatos.nombre.upper()==basedatos.upper())(db.basedatos.servidor==id_servidor).\
	select(db.basedatos.version_id).first()
	if ver_id is None:
		desc_version = 'sin version'
	else:	
		desc_version=db(db.ver.id==ver_id.version_id).select(db.ver.descri).first()

	return desc_version


def cuenta_asignacion(user):
	cant=db(db.asignacion.analista==user).count()
	return (cant)

def cuenta_subactividades(actividad):
	cant=db(db.subactividades_sd.actividad_id==actividad).count()
	return (cant)



def cuenta_asignacion_status(user, status):
	cant=db(db.asignacion.analista==user)(db.proyectos.id==db.asignacion.cod_proyecto)(db.proyectos.status==status).count()
	return (cant)
	
# and define some global variables that will make code more compact
#User, Link, Post = db.auth_user, db.link, db.post
#me, a0, a1 = auth.user_id, request.args(0), request.args(1)
#myfriends = db(Link.source==me)(Link.accepted==True)
#alphabetical = User.first_name|User.last_name
#def name_of(user): return '%(first_name)s %(last_name)s' % user

