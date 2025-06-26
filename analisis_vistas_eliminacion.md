# ANÁLISIS DE VISTAS PARA ELIMINACIÓN - SENIAT PYTHON3

## ESTADO ACTUAL
**Total de archivos HTML**: 197 archivos
**Archivos optimizados**: 5

## CLASIFICACIÓN POR PRIORIDAD

### ✅ VISTAS OPTIMIZADAS (MANTENER)
- `dashboard_optimized.html`
- `list_basedatos_optimized.html`
- `monitor_graf_optimized.html`
- `list_servidores.html` (ya optimizado)
- `crear_actividades_sd_optimized.html`

### 🔴 VISTAS PRINCIPALES EN USO (OPTIMIZAR PRÓXIMAMENTE)
- `list_actividades_sd.html`
- `crear_proyectos.html`
- `list_proyectos.html`
- `user.html`
- `view_servidor.html`
- `view_basedatos.html`
- `edit_servidor.html`
- `edit_basedatos.html`
- `index.html`
- `claves.html`

### 🟡 VISTAS SECUNDARIAS (REVISAR USO)
- `list_cuentas_so.html`
- `list_custodios.html`
- `list_actividades.html`
- `crear_actividades.html`
- `list_claves.html`
- `monitor.html`
- `chart.html`
- `reporte_actividades.html`

### ❌ CANDIDATOS PARA ELIMINACIÓN INMEDIATA

#### **Archivos de versiones duplicadas/obsoletas:**
- `dashboard.html` (reemplazado por dashboard_optimized.html)
- `list_basedatos.html` (reemplazado por list_basedatos_optimized.html)
- `monitor_graf.html` (reemplazado por monitor_graf_optimized.html)
- `monitor_graf-v-ant.html` (versión anterior)
- `monitor_graf - copia.html` (copia de backup)
- `list_servidores2.html` (duplicado)
- `list_servidores_optimized.html` (duplicado, usar list_servidores.html)
- `crear_actividades_sd.html` (reemplazado por crear_actividades_sd_optimized.html)

#### **Archivos de copias y backups:**
- `list_bd_online_grafica - copia.html`
- `lista_bd_servidores - copia.html`
- `exportar_inv_excel2.html`
- `list_actividades_solutor2.html`
- `list_detalle_act2.html`
- `list_detalle_act3.html`
- `list_detalle_act4.html`
- `reporte_novedadesx.html`
- `tabla2.html`

#### **Funcionalidades no implementadas/utilizadas:**
- `asignacion.html`
- `calendar.html`
- `ckeditor.html`
- `conectar.html`
- `createReport.html`
- `editable_grid.html`
- `ejecuta_comando_sql.html`
- `chart_pygal.html`
- `plot_pygal.html`
- `rutinas.html`
- `edit_rutina_status.html`
- `list_rutina_status.html``
- `view_rutina_status.html`


#### **Páginas de prueba/desarrollo:**
- `prueba_9i.html`
- `tabla.html`
- `content.html`
- `edita.html`
- `editItem.html`
- `herpos.html`
- `persona.html`

#### **Formularios específicos no usados:**
- `form_crecimiento_bd.html`
- `form_crecimiento_tbs.html`
- `form_dashboard.html`
- `g_crecimiento_diario.html`

#### **Reportes específicos probablemente no usados:**
- `bd_pdf.html`
- `confirmation_pdf.html`
- `csvExport_aut.html`
- `excel_report.html`
- `pie.html`
- `rep_logs_basedatos_pantalla.html`
- `rep_logs_cuentas_so_pantalla.html`
- `rep_novedades_pantalla.html`
- `rep_serv_conf.html`
- `rep_serv_resp.html`
- `rep_serv_respc.html`
- `rep_serv_vers.html`


## RECOMENDACIÓN DE ELIMINACIÓN POR LOTES

### **Lote 1 - Duplicados y copias (ELIMINAR INMEDIATAMENTE)**
```
dashboard.html
list_basedatos.html
monitor_graf.html
monitor_graf-v-ant.html
monitor_graf - copia.html
list_servidores2.html
list_servidores_optimized.html
crear_actividades_sd.html
list_bd_online_grafica - copia.html
lista_bd_servidores - copia.html
exportar_inv_excel2.html
list_actividades_solutor2.html
list_detalle_act2.html
list_detalle_act3.html
list_detalle_act4.html
reporte_novedadesx.html
tabla2.html
```

### **Lote 2 - Funcionalidades no implementadas (ELIMINAR)**
```
asignacion.html

calendar.html
ckeditor.html
conectar.html
createReport.html
editable_grid.html
ejecuta_comando_sql.html
chart_pygal.html
plot_pygal.html
rutinas.html

edit_rutina_status.html

list_rutina_status.html

view_rutina_status.html

```

### **Lote 3 - Archivos de prueba/desarrollo (ELIMINAR)**
```
prueba_9i.html
tabla.html
content.html
edita.html
editItem.html
herpos.html
persona.html
form_crecimiento_bd.html
form_crecimiento_tbs.html
form_dashboard.html
g_crecimiento_diario.html
```

## RESUMEN DESPUÉS DE LIMPIEZA PROPUESTA
- **Archivos actuales**: 197
- **Archivos a eliminar**: ~60-80
- **Archivos restantes**: ~120-140
- **Reducción estimada**: 30-40% del código

¿Quieres que proceda con alguno de estos lotes de eliminación?
