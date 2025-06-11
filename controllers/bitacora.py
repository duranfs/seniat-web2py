
@auth.requires_login()
def bitacora_actividades_sd():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#bitacora').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	#actividad =  request.vars.get('actividad')
	me = auth.user_id	
	
	a=db.actividades_sd
	b=db.subactividades_sd

	form=crud.create(a)
	#rows = db(a.completado !='CERRADA').select()
	#rows = db(a.id == b.actividad_id).select(a.ALL, distinct=True)
	rows = db(a.id>0)(a.completado !='CERRADA').select(a.ALL, distinct=True)
	return dict(form=form, rows=rows, script=script)



def agregar_subactividad():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#subactividades').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')

	NO_MOSTRAR_BD = (2,3,4,7)

	actividad_id=0
	var_proyecto=""
	var_subproyecto=""
	var_descripcion=""
	var_status=""
	if request.vars and 'actividad_id' in request.vars and request.vars.actividad_id:
		actividad_id=request.vars.get('actividad_id')
		var_proyecto=request.vars.get('proyecto')
		var_subproyecto=request.vars.get('subproyecto')
		var_descripcion=request.vars.get('desc')
		var_status=request.vars.get('status')
	else:
		actividad_id=session.actividad
		var_proyecto=session.var_proyecto
		var_subproyecto=session.var_subproyecto
		var_descripcion=session.var_descripcion
		var_status=session.var_status

	proyectos = [OPTION(str(datos.descri),_value=datos.id) 
	for datos in db(db.proyectos.id>0)(db.proyectos.status != 'COMPLETADO').select(db.proyectos.ALL)]
	
	campossubActividades_sd = [
		#INPUT(_name='actividad_id', _type='integer'),
		SELECT(*proyectos,**dict(_name="cod_proy")),
		INPUT(_name='cod_subp', _type='integer'),
		INPUT(_name='cod_servidor', _type='integer'),
		INPUT(_name='cod_bd', _type='integer'),
		INPUT(_name='descripcion', _type='textarea'),
		INPUT(_name='fecha_inicio', _type='datetime'),
		INPUT(_name='fecha_fin', _type='datetime'),
		INPUT(_name='hora_inicio', _type='sting', _requires=IS_TIME(error_message='Hora no valida')	, default='08:00'),
		INPUT(_name='hora_fin', _type='sting', _requires=IS_TIME(error_message='Hora no valida')	, default='12:30'),
		INPUT(_name='horas_laboradas', _type='double',  _default=0.00),
		INPUT(_name='horas_extras', _type='double',  _default=0.00),
		INPUT(_name='tipo', _type='string', _default='P', _requires=IS_IN_SET(TIPO_ACT)),
		INPUT(_name='producto', _type='list', _default='INFORME' ),
		INPUT(_name='completado', _type='string:list', _default='CERRADA' ),
		INPUT(_name='analista', _type='integer', _default=auth.user_id ),]

	formasubAct = FORM(*campossubActividades_sd)
	
	if formasubAct.accepts(request.vars,formname='formaHTML', keepvalues=False):
		datossubActividades_sd = db.subactividades_sd._filter_fields(formasubAct.vars)
		datossubActividades_sd['actividad_id'] = actividad_id
		datossubActividades_sd['cod_proy'] = formasubAct.vars.cod_proy
		datossubActividades_sd['cod_subp'] = formasubAct.vars.cod_subp
		datossubActividades_sd['cod_servidor'] = formasubAct.vars.cod_servidor
		datossubActividades_sd['cod_bd'] = formasubAct.vars.cod_bd
		datossubActividades_sd['descripcion'] = formasubAct.vars.descripcion
		datossubActividades_sd['fecha_inicio'] = formasubAct.vars.fecha_inicio
		datossubActividades_sd['fecha_fin'] = formasubAct.vars.fecha_fin
		datossubActividades_sd['analista'] = me

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

		if formasubAct.vars.completado == 'CERRADA' and formasubAct.vars.horas_laboradas == '0.00' and formasubAct.vars.horas_extras == '0.00':
			session.flash='Actividad sin horas laboradas, por favor verifique!'

		#if formasubAct.vars.horas_laboradas == '0:00:00':
		#	session.flash='Actividad sin horas laboradas, por favor verifique!'

		if e_fch1_rango_act>0 or e_fch2_rango_act>0 or e_fch1_rango_sact>0 or e_fch2_rango_sact>0:
			session.flash='Existe actividad o subactividad cargadas en el mismo rango de horas! (' + str(fecha1) + ' -- ' + str(fecha2) + ')'

		else:
			existen_fechas_dentro_rango_act=db(db.actividades_sd.fecha_inicio>=fecha1)(db.actividades_sd.fecha_fin<=fecha2)\
			(db.actividades_sd.analista==me).count()

			existen_fechas_dentro_rango_subact=db(db.subactividades_sd.fecha_inicio>=fecha1)(db.subactividades_sd.fecha_fin<=fecha2)\
			(db.subactividades_sd.analista==me).count()

			if existen_fechas_dentro_rango_act>0 or existen_fechas_dentro_rango_subact>0:
				session.flash='Existe actividad o subActividad dentro del rango de horas indicadas!'
			else:
				ActividadesInsertado = db.subactividades_sd.insert(**datossubActividades_sd)
				db(db.actividades_sd.id == actividad_id).update(completado='ABIERTA CON SUBACTIVIDADES')
				db.commit()
				session.flash='Registro insertado'
				redirect(URL('agregar_subactividad')) #evita que se dupliquen los registros al refrescar la pagina
		
	proyectos = db(db.proyectos.id >0)(db.proyectos.status != 'COMPLETADO').select(db.proyectos.ALL, orderby=db.proyectos.descri)
	subproyectos=db(db.subproyectos.id>0).select(db.subproyectos.ALL, orderby=db.subproyectos.descri)
	if request.vars.cod_proy:
		subproyectos = db(db.subproyectos.proyecto==request.vars.cod_proy).select(db.subproyectos.ALL, orderby=db.subproyectos.descri)
	else:
		subproyectos = db(db.subproyectos.proyecto>0).select(db.subproyectos.ALL, orderby=db.subproyectos.descri)

	datos_actividad=db.actividades_sd[actividad_id]
	
	# importante para agregar
	session.var_proyecto=var_proyecto
	session.var_subproyecto=var_subproyecto
	session.var_descripcion=var_descripcion
	session.actividad=actividad_id
	session.var_status=var_status

	servidores=db(db.servidores.id>0)(db.servidores.status=='OPERATIVO').select(db.servidores.ALL, orderby=db.servidores.nombre)
	if request.vars.cod_servidor:
		
		basedatos = db((db.basedatos.servidor==request.vars.cod_servidor) & (db.basedatos.estado_id.belongs(NO_MOSTRAR_BD) ))\
		.select(db.basedatos.ALL, orderby=db.basedatos.nombre)
	else:
		basedatos = db((db.basedatos.servidor==1) & (db.basedatos.estado_id.belongs(NO_MOSTRAR_BD) ))\
		.select(db.basedatos.ALL, orderby=db.basedatos.nombre)

	appl = db(db.basedatos.id>0)(db.basedatos.appl != 'None').\
	select(db.basedatos.nombre, db.basedatos.appl, db.basedatos.servidor, distinct=True, orderby="nombre")
	return dict(script=script, proyectos=proyectos, subproyectos=subproyectos, da=datos_actividad, \
		 var_proyecto=var_proyecto,var_subproyecto=var_subproyecto,var_descripcion=var_descripcion, servidores=servidores, basedatos=basedatos, appl=appl, var_status=var_status)


def func_bd_bitacora():
	NO_MOSTRAR_BD = (2,3,4,7)
	basedatos = db((db.basedatos.servidor==request.vars.cod_servidor) & (db.basedatos.estado_id.belongs(NO_MOSTRAR_BD) ))\
	.select(db.basedatos.ALL, orderby=db.basedatos.nombre)
	result = ""
	for datos in basedatos:
		result += "<option value='" + str(datos.id) + "'>" + datos.nombre + "</option>"  
	return XML(result)


def func_sac_sd():
	#fecha = request.vars.fecha_inicio;
	if request.vars and 'actividad_id' in request.vars and request.vars.actividad_id:
		actividad = request.vars.actividad_id;
	else:
		actividad = session.actividad;	

	total_horas=0;
	total_extra=0;
	cant_act=0;

	subactividades_sd = db(db.subactividades_sd.id>0)\
	(db.subactividades_sd.actividad_id==actividad)\
	.select(orderby=~db.subactividades_sd.fecha_inicio)

	format_date = '%d-%m-%Y %H:%M%p'

	if subactividades_sd:
		# cambia a 100% para que el detalle quede bien 
		tablaHTML = "<table cellpadding='6' id='' style='width:100%; font-size: 12px; ' class='table-bordered '>"
		tablaHTML +="<col style='width:5%;'>"
		tablaHTML +="<col style='width:10%;'>"
		tablaHTML +="<col style='width:10%;'>"
		tablaHTML +="<col style='width:40%'>"
		tablaHTML +="<col style='width:8%'>"
		tablaHTML +="<col style='width:8%'>"
		tablaHTML +="<col style='width:5%'>"
		tablaHTML +="<col style='width:3%'>"
		tablaHTML +="<col style='width:3%'>"
		
		tablaHTML +="<thead> <tr rowspan='1'><th colspan='4'>Descripción</th><th colspan='2' style='text-align: center;'>Fechas</th><th colspan='1' style='text-align: center;'>Total</th><th colspan='1' style='text-align: center;'>Extra</th><th colspan='1' style='text-align: center;'>Tipo</th> </tr>"
		tablaHTML +="</thead>"
		tablaHTML +="<tbody>"
		for datos in subactividades_sd:
			tablaHTML +="<tr>"
			tablaHTML +="<td>" + str(datos.analista.first_name) + "</td>"
			tablaHTML +="<td>" + str(datos.cod_proy.descri) + "</td>"
			tablaHTML +="<td>" + str(datos.cod_subp.descri) + "</td>"
			tablaHTML +="<td>" + "<a style='color: black;  font-weight: bold; ont-size: 16px;' href='editar_subactividades?subact=" + str(datos.id) +  " '>"  + str(datos.descripcion) + "</a>" + "</td>"
			tablaHTML +="<td>" + str(datos.fecha_inicio.strftime(format_date)) + "</td>"
			tablaHTML +="<td>" + str(datos.fecha_fin.strftime(format_date)) + "</td>"
			tablaHTML +="<td style='color: red; font-weight: bold; font-size: 12px;'>" + str(datos.horas_laboradas) + "</td>"
			tablaHTML +="<td style='color: red; font-weight: bold; font-size: 12px;'>" + str(datos.horas_extras) + "</td>"
			tablaHTML +="<td>" + str(datos.tipo) + "</td>"
			tablaHTML +="</tr>"
			total_horas = total_horas + datos.horas_laboradas;
			total_extra = total_extra + datos.horas_extras;
			cant_act +=1
	
		tablaHTML +="</tbody>"
		tablaHTML +="<tfoot>"
		tablaHTML +="<tr>"
		tablaHTML +="<th style='font-size: 14px; font-color=#40b5e1' id='total' colspan='6' >Total horas:</th>"
		tablaHTML +='<td colspan="" style="color: red; font-weight: bold; font-size: 14px;">' + str(total_horas) + '</td>'
		tablaHTML +='<td colspan="" style="color: red; font-weight: bold; font-size: 14px;">' + str(total_extra) + '</td>'
		tablaHTML +='<td style="color: black; font-weight: bold; font-size: 18px;">'+str(cant_act)+'</td>'
		tablaHTML +="</tr>"
		tablaHTML +="</tfoot>"

		tablaHTML +="</table>"
		return XML(tablaHTML)
	return XML("")




def subproyecto():
    subproyectos = db(db.subproyectos.proyecto==request.vars.cod_proy).select(db.subproyectos.ALL, orderby=db.subproyectos.descri)
    result = ""
    for subproyecto in subproyectos:
        result += "<option value='" + str(subproyecto.id) + "'>" + subproyecto.descri + "</option>"  
    return XML(result)


def editar_subactividades():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#editar_subactividades').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	
	subact_id=request.args(0)
	fecha = request.vars.fecha_inicio;
	subact=request.vars.subact
	query = (db.subactividades_sd.id==request.vars.subact)
	subactividad_id=request.vars.subact
	actividad_reg=db.subactividades_sd[subactividad_id] or redirect(error_page)
	db.subactividades_sd.actividad_id.writable=False
	db.subactividades_sd.actividad_id.readable=False
	db.subactividades_sd.cod_proy.writable=False
	db.subactividades_sd.cod_proy.readable=False
	db.subactividades_sd.cod_subp.writable=False
	db.subactividades_sd.cod_subp.readable=False
	form=crud.update(db.subactividades_sd, actividad_reg.id, next=url('agregar_subactividad'))

	return 	locals()



@auth.requires_login()
def estatus_actividad():
	me = auth.user_id
	if request.vars and 'actividad_id' in request.vars and request.vars.actividad_id:
		if request.vars.get('st') in ('CERRADA'):
			actividad=db.actividades_sd[request.vars.get('actividad_id')]
			if actividad:
				if actividad.completado in ('CERRADA'):
					 #raise HTTP(500, "La tabla de clientes está vacía")
					session.flash = \
					T("La actividad nro: %(actividad_id)s ya esta %(completado)s") % \
					dict(completado=actividad.completado,	actividad_id=request.vars.get('actividad_id'))
				else:
					actividad.update_record(completado=request.vars.get('st'), fecha_cierre=request.now, cerrada_por=me)
					#items = db(db.item.factura_id==factura.id).select()
					#total = 0.00
					#for item in items:
					#	aumenta_inventario(item.producto_id, '+',item.cantidad)
					session.flash = \
					T("Actividad %(actividad_id)s %(completado)s con exito!") % \
					dict(completado=request.vars.get('st'),	actividad_id=request.vars.get('actividad_id'))
	#return "$('#votes').html('%s');$('.flash').html('%s').slideDown();" % (factura.status,'hola')
	redirect(URL(f="bitacora_actividades_sd"))


@auth.requires_login()
def status_actividad():
	me = auth.user_id
	if request.vars and 'actividad_id' in request.vars and request.vars.actividad_id:
		actividad=db.actividades_sd[request.vars.get('actividad_id')]
		if actividad:
			if request.vars.get('st') == ('ABIERTA') :
				actividad.update_record(completado='ABIERTA', fecha_cierre=request.now, cerrada_por=me)
			else:
				if request.vars.get('st') == ('CERRADA'):
					actividad.update_record(completado='CERRADA', fecha_cierre=request.now, cerrada_por=me)

			c=db.log_actividades_sd
			campos=["actividad","analista","fecha","status"]
			valores=[actividad.id, me, request.now, request.vars.get('st')]
			data=dict(zip(campos, valores))
			c.insert(**data)
			session.flash = \
			T("Actividad %(actividad_id)s %(completado)s con exito!") % \
			dict(completado=request.vars.get('st'),	actividad_id=request.vars.get('actividad_id'))
	redirect(URL(f="bitacora_actividades_sd"))

@auth.requires_login()
def list_subactividades_sd():
	form=crud.create(db.subactividades_sd)
	query = db.subactividades_sd.id>0
	rows = db(query).select(orderby=db.subactividades_sd.analista|db.subactividades_sd.fecha_inicio)
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#subactividades').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	return dict(form=form, rows=rows, script=script)

def editar_subactividades_sd():
	subact_id=request.args(0)
	#db.subactividades_sd.actividad_id.writable=False
	#db.subactividades_sd.actividad_id.readable=False
	db.subactividades_sd.actividad_id.writable=False
	db.subactividades_sd.cod_proy.writable=False
	db.subactividades_sd.cod_proy.readable=False
	db.subactividades_sd.cod_subp.writable=False
	db.subactividades_sd.cod_subp.readable=False
	actividad_id = db.subactividades_sd(subact_id) or redirect(URL('list_subactividades_sd'))
	form = crud.update(db.subactividades_sd,subact_id,next='list_subactividades_sd')
	return locals()


