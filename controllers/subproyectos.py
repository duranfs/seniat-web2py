
def get_rows_subp(cod_subp):
	query = (db.actividades_sd.cod_subp==cod_subp)
	rows = db(query).count()
	return  (rows)


auth.add_permission(1, 'edit', db.auth_user)
@auth.requires(auth.has_membership('ADMIN'))
@auth.requires_login()
def crear_subproyectos():
	response.files.append(URL(request.application,'static','data_table.css'))
	response.files.append(URL(request.application,'static/DataTables/media/js','jquery.DataTables.min.js'))
	script = SCRIPT('''$(document).ready(function(){
	oTable = $('#subproyectos').dataTable({"bStateSave": true,"sPaginationType": "full_numbers"});
	});''')
	rows=None
	cod_proy = request.vars.get('cod_proy')
	proyectos = db(db.proyectos.id >0)(db.proyectos.status != 'COMPLETADO').select(db.proyectos.ALL, orderby=db.proyectos.descri)
	subproyectos = db(db.subproyectos.proyecto==request.vars.cod_proy).select(db.subproyectos.ALL,orderby=db.subproyectos.proyecto|db.subproyectos.id)

	camposSubproyetos = [
		###########################################
		# Subproyecto
		INPUT(_name='descri', _type='string'),
		INPUT(_name='proyecto', _type='integer'),
	]

	
	formaSP = FORM(*camposSubproyetos)
	if formaSP.accepts(request.vars,formname='formaSPHTML',  keepvalues=True):
		datosSP = db.subproyectos._filter_fields(formaSP.vars)
		datosSP['proyecto'] = cod_proy
		SPinsertado = db.subproyectos.insert(**datosSP)
		redirect(URL('subproyectos','crear_subproyectos',''))
		response.flash = 'Procesado con Éxito' 
	elif formaSP.errors:
		import copy
		myerrors=copy.copy(formaSP.errors)
		response.flash = myerrors
		#session.flash="Error al llenar la forma"
	else:
		pass
	datossubp=db(db.proyectos.id == db.subproyectos.proyecto)(db.proyectos.status != 'COMPLETADO').select(db.subproyectos.proyecto,db.subproyectos.descri)
	return dict(subproyectos=subproyectos, proyectos=proyectos, script=script, datossubp=datossubp)
	
def subp_dropdown():
	subproyectos = db(db.subproyectos.proyecto==request.vars.cod_proy).select(db.subproyectos.ALL)
	result = ""
	for subproyecto in subproyectos:
		result += "<option value='" + str(subproyecto.id) + "'>" + subproyecto.descri + "</option>"  
	return XML(result)


def subp_tabla():
	subproyectos = db(db.subproyectos.proyecto==request.vars.cod_proy).select(db.subproyectos.ALL, orderby=db.subproyectos.proyecto|db.subproyectos.id)
	result = ""
	result += "<table id='subproyectosxx' style='width: 100%' class='smarttablexx tablex datatablesx_table' border='2px'>"
	result += "<col style='width: 5%;'></col>"
	result += "<col style='width: 50%;'></col>"
	result += "<col style='width: 5%;'></col>"
	result += "<col style='width: 5%;'></col>"
	result += "<thead>"
	result += "<tr>"
	result += "<th>ID</th>"
	result += "<th>Descripcion</th>"
	result += "<th>Cant</th>"
	result += "<th style='text-align: center;'>Accion</th>"
	result +="</tr>"    
	result +="</thead>"
	result +="<tbody>"
	for subproyecto in subproyectos:
		result +="<tr>"
		result +="<td>" + str(subproyecto.id) + "</td>"
		result +="<td>" + str(subproyecto.descri) + "</td>"
		result +="<td>" + str(get_rows_subp(subproyecto.id)) + "</td>"
		result +="<td>" 
		result +="<a style='text-align: center;' href=editar_subproyectos2?subproyecto_id=" + str(subproyecto.id) 
		result +="><img style='border:0;width:=30px;height:20px;' "
		result +="alt='Editar' src='/bdvinv_python3/static/images/edit-1.ico')> "
		result +="</a>"
		result +="</td>"
		result +="</tr>"
	result +="</tbody>"
	result +="</table>"
	return XML(result)


def editar_subproyectos():
	subproyecto_id = request.vars.get('subproyecto_id')
	db.subproyectos.proyecto.enable=False
	db.subproyectos.proyecto.writable=False
	detalle = db.subproyectos[subproyecto_id]
	crud.messages.record_updated = 'Registro actualizado'
	form=crud.update(db.subproyectos, detalle, ondelete=valida_actividades(subproyecto_id))
	if form.accepts(request):
		redirect(URL('subproyectos','crear_subproyectos' ))
	return dict(form=form)


def editar_subproyectos2():
	result=''
	subproyecto_id = request.vars.get('subproyecto_id')
	db.subproyectos.proyecto.enable=False
	db.subproyectos.proyecto.writable=False
	detalle = db.subproyectos[subproyecto_id]
	
	form=SQLFORM(db.subproyectos, detalle, deletable=True)
	form.process(dbio=False)
	if form.accepted:
		if form.deleted:
			registros = db(db.actividades_sd)(db.actividades_sd.cod_subp==subproyecto_id).count()
			if registros and (registros > 0): 
				session.flash='No se puede borrar el subproyecto = ' + str(detalle.descri) + ' Hay ' +str(registros) + ' actividades cargadas'
			else:
				#form.record.delete()
				db(db.subproyectos.id == subproyecto_id).delete()
		else:
			form.record.update_record(**form.vars)
		redirect(URL('subproyectos','crear_subproyectos' ))
	return dict(form=form)


def valida_actividades(subproyecto_id):
	registros = db(db.actividades_sd)(db.actividades_sd.cod_subp==subproyecto_id).count()
	if registros and (registros > 0): 
		session.flash='Hay actividades'
	return False