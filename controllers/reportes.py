def valida_fechas2(formaOP):
    if formaOP.vars.desde > formaOP.vars.hasta:
        formaOP.errors.desde = 'Fechas erradas'
        formaOP.errors.hasta = 'Fechas erradas'

# -- list actividades solutor 

def func_count_subA(actividad_id):
	cantidad = db(db.subactividades_sd.actividad_id==actividad_id).count()
	return cantidad

def convert_date(date_time): 
	import datetime
	format = '%Y-%m-%d' # The format 
	datetime_str = datetime.datetime.strptime(date_time, format) 
	return datetime_str.strftime('%m%d%Y')

def set_excel_style(name, height, bold=False):
    """Set excel style.
    """
    style = xlwt.XFStyle() # 初始化样式
    font = xlwt.Font() # 为样式创建字体
    font.name = name # 例如'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height
    if bold:
        borders = xlwt.Borders()
        borders.left = 6
        borders.right = 6
        borders.top = 6
        borders.bottom = 6
        style.borders = borders
    style.font = font
    return style 
    

@auth.requires_login()
def reporte_sd():
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
		INPUT(_name='desde', _type='datetime-local'),
		INPUT(_name='hasta', _type='datetime-local'),
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
		from xlwt import Font
		from xlwt import XFStyle
		#from xlwt import *
	
		format_date = '%d-%m-%Y %H:%M%p'

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
	
		style2 = xlwt.easyxf('font: name Times New Roman, color-index blue, bold on',
		num_format_str='#,##0.00')
    
		texto = XFStyle()
		texto = xlwt.easyxf('align: wrap on, vert center, horiz left')
		texto.alignment.wrap = 1
		texto.borders = border
		
		textoC = XFStyle()
		textoC = xlwt.easyxf('align: wrap on, vert center, horiz center')
		textoC.alignment.wrap = 1
		textoC.borders = border
		
		textoB = XFStyle()
		textoB = xlwt.easyxf('font: bold on')
		textoB.alignment.wrap = 1
		textoB.borders = border
		
		fecha = xlwt.easyxf('align: wrap on, vert center, horiz center')
		fecha.num_format_str = 'DD-MM-YYYY'
		fecha.borders = border
		
		hora = xlwt.easyxf('align: wrap on, vert center, horiz center',num_format_str='#,##0.00')
		hora.borders = border
	
		horaB = xlwt.easyxf('font: name Times New Roman, color-index blue, bold on',num_format_str='#,##0.00')
		horaB.borders = border
	
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
		subactividad = ws.col(10)
		status = ws.col(11)
		tot = ws.col(12)
		extra = ws.col(13)
		incid_bd = ws.col(14)
		bd_afecta = ws.col(15)
		incid_otros = ws.col(16)
		otros_afecta = ws.col(17)
		obs_otros = ws.col(18)
		id_act = ws.col(19)
		
		analista.width = 200*20
		ambiente.width = 200*20
		tipo.width = 200*20
		fec1.width = 200*20
		fec2.width = 200*20
		proy.width = 600*20
		servidor.width = 400*20
		bd.width = 350*20
		subp.width = 400*20
		desc.width = 700*20
		subactividad.width = 700*20
		status.width = 450*20
		tot.width = 130*20
		extra.width = 130*20
		incid_bd.width = 130*20
		bd_afecta.width = 130*20
		incid_otros.width = 130*20
		otros_afecta.width = 130*20
		obs_otros.width = 600*20
		id_act.width = 130*20
		
		top_row = 0
		bottom_row = 0
		left_column = 0
		right_column = 1
		#ws.write_merge(top_row, bottom_row, left_column, right_column, 'Long Cell')

		des_tipo=''

		head1 = ['Analista','Ambiente','Tipo','Fecha Inicio', 'Fecha fin', 'Servidor','BD','Proyecto', 'Sub-Proyecto',\
		'Descripcion Actividad','SubActividad','Estatus','Total Horas','Horas extras','Incidencia-BD','Afecta BD','Incidencia-Otros','Afecta BD','Obs Otros','ID Actividad']
		for index, value in enumerate(head1):
			ws.write(0, index, value, encab)
		

		a=db.actividades_sd
		b=db.subactividades_sd

		query=(a.fecha_inicio >= desde)&(a.fecha_inicio <= hasta)|(a.completado.contains('ABIERTA'))

		rows = db(query)\
			.select(a.id, a.tipo, a.ambiente_id,a.analista,a.fecha_inicio, a.fecha_fin,a.cod_proy,a.cod_subp,a.descripcion,a.horas_laboradas,\
			a.horas_extras, a.cod_servidor,a.cod_bd,a.incid_bd,a.incid_otros, a.completado, a.obs_otros, a.bd_afecta, a.otros_afecta, orderby=a.analista|a.fecha_inicio)

		row = 1
		col = 0
		w_analista=''
		

		for index, r in enumerate(rows):

			if r.tipo == 'R':
				des_tipo='REMOTO'
			else:
				des_tipo='PRESENCIAL'

			ws.write (row, 0, r.analista.first_name +' '+r.analista.last_name , texto)
			ws.write (row, 1, r.ambiente_id.descri, texto)
			ws.write (row, 2, des_tipo, texto)
			ws.write (row, 3, r.fecha_inicio.strftime(format_date), fecha)
			ws.write (row, 4, r.fecha_fin.strftime(format_date), fecha)
			
			if r.cod_servidor >0:
				ws.write (row, 5, r.cod_servidor.nombre, texto)
			else:
				ws.write (row, 5, r.cod_servidor, texto)
			
			if r.cod_bd >0:
				ws.write (row, 6, r.cod_bd.nombre, texto)
			else:
				ws.write (row, 6, r.cod_bd, texto)
	
			ws.write (row, 7, r.cod_proy.descri, texto)

			if r.cod_subp >0:
				ws.write (row, 8, r.cod_subp.descri, texto)
			else:
				ws.write (row, 8, r.cod_subp, texto)

			ws.write (row, 9, r.descripcion, texto)
					
			st=db(a.id==r.id)(a.completado.contains('ABIERTA')).count()
			subact_mes=db(b.actividad_id==r.id)(b.fecha_inicio >= desde)(b.fecha_inicio <= hasta).count()

			if st>0 and subact_mes==0 and func_count_subA(r.id)>0:
				ws.write (row, 10, '<<<< Esta actividad no tiene Sub-actividades registradas en el mes >>>>',textoB)

			ws.write (row, 11, r.completado, texto)

			
			# if r.horas_extras>0:
			# 	#ws.write (row, 12, r.horas_laboradas - r.horas_extras, hora )	activar proximo mes
			# 	ws.write (row, 12, 0, hora )				
			# 	ws.write (row, 13, r.horas_extras, hora)
			# else:	
			# 	if func_count_subA(r.id)>0:
			# 		ws.write (row, 12, 0, hora)
			# 	else:
			# 		ws.write (row, 12, r.horas_laboradas, hora)
			# 	ws.write (row, 13, 0, hora)
			
			if func_count_subA(r.id)>0:
				ws.write (row, 12, 0, hora)
			else:
				ws.write (row, 12, r.horas_laboradas, hora)
			
			ws.write (row, 13, r.horas_extras, hora)
			
		
			if r.incid_bd:
				ws.write (row, 14, 'X', texto)
			else:
				ws.write (row, 14, '', texto)

			if r.bd_afecta:
				ws.write (row, 15, 'X', texto)
			else:
				ws.write (row, 15, '', texto)

			if r.incid_otros:
				ws.write (row, 16, 'X', texto)
			else:
				ws.write (row, 16, '', texto)
			
			if r.otros_afecta:
				ws.write (row, 17, 'X', texto)
			else:
				ws.write (row, 17, '', texto)
					
			ws.write (row, 18, r.obs_otros, texto)


			if func_count_subA(r.id)>0:
				ws.write (row, 19, r.id, texto)
			else:	
				ws.write (row, 19, '', )

			w_analista = r.analista
			
			query=(b.actividad_id==r.id)&(b.fecha_inicio >= desde)&(b.fecha_inicio <= hasta)			
			for sub in db(query).select(b.analista, b.fecha_inicio, b.fecha_fin, b.horas_laboradas, \
				b.horas_extras, b.completado, b.descripcion,  b.tipo, b.cod_bd, b.cod_servidor, orderby=b.fecha_inicio):
				row +=1
				if sub.tipo == 'R':
					des_tipo='REMOTO'
				else:
					des_tipo='PRESENCIAL'



				ws.write (row, 0,  sub.analista.first_name +' '+sub.analista.last_name, texto)

				amb=db(db.basedatos.id==sub.cod_bd).select(db.basedatos.ambiente_id).first()
				
				if amb:
					ws.write (row, 1,  amb.ambiente_id.descri, texto)
				else:
					desc_amb=''
					ws.write (row, 1,  desc_amb, texto)

				ws.write (row, 2,  des_tipo, texto)
				ws.write (row, 3,  sub.fecha_inicio.strftime(format_date), fecha)
				ws.write (row, 4,  sub.fecha_fin.strftime(format_date), fecha)

				if sub.cod_servidor >0:
					ws.write (row, 5, sub.cod_servidor.nombre, texto)
				else:
					ws.write (row, 5, sub.cod_servidor, texto)
				
				if sub.cod_bd >0:
					ws.write (row, 6, sub.cod_bd.nombre, texto)
				else:
					ws.write (row, 6, sub.cod_bd, texto)

				ws.write (row, 10, sub.descripcion,textoB)
				ws.write (row, 11, sub.completado, texto)

				# if sub.horas_extras>0:
				# 	#ws.write (row, 12, sub.horas_laboradas - sub.horas_extras, hora) activar proximo mes
				# 	ws.write (row, 12, 0, hora)
				# 	ws.write (row, 13, sub.horas_extras, hora)
				# else:
				# 	ws.write (row, 12, sub.horas_laboradas, hora)
				# 	ws.write (row, 13, 0, hora)
				
				ws.write (row, 12, sub.horas_laboradas, hora)
				ws.write (row, 13, sub.horas_extras, hora)
				
				
			row +=1
		
		row =1
		
		nombre=db.auth_user[me]
		from datetime import datetime
		fecha=(hasta)

		response.headers['Content-Type']='application/vnd.ms-excel'
		response.headers['Content-disposition'] = 'attachment; filename=%s %s - %s - GL DyA.xls' % (nombre.first_name.upper(), nombre.last_name.upper(), fecha) 
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

