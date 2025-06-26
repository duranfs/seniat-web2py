# 📊 ANÁLISIS DE VISTAS UTILIZADAS - APLICACIÓN SENIAT

## 🔍 **METODOLOGÍA DE ANÁLISIS**

Se analizaron:
1. **Archivo de menús** (`models/menu.py`)
2. **Controladores** (default.py, oracle.py, bitacora.py, etc.)
3. **Funciones activas** en los controladores

---

## 🎯 **VISTAS PRIORITARIAS POR USO**

### **🔥 NIVEL 1: CRÍTICAS (Menú Principal)**

#### **📱 Dashboard y Monitoreo**
- ✅ `dashboard.html` - **YA OPTIMIZADO**
- ⭐ `monitor_graf.html` - **ALTA PRIORIDAD**
- `form_dashboard.html`
- `monitor.html`

#### **💾 Inventario Base**
- ✅ `list_basedatos.html` - **YA OPTIMIZADO** 
- ⭐ `list_servidores.html` - **ALTA PRIORIDAD**
- `list_estadisticas.html`
- `list_cuentas_so.html`

#### **👥 Gestión Operativa**
- ⭐ `crear_actividades_sd.html` - **ALTA PRIORIDAD**
- ⭐ `list_actividades_sd.html` - **ALTA PRIORIDAD**
- `bitacora/bitacora_actividades_sd.html`
- `reportes/reporte_sd.html`

---

### **🔥 NIVEL 2: IMPORTANTES (Acceso Frecuente)**

#### **🏗 Administración DBA**
- `list_dba.html`
- `oracle/ejecutar_sql.html`
- `list_rutinas.html`
- `asignar_rutinas.html`
- `rutinas_asignadas.html`

#### **📋 Tablas Básicas**
- `list_tipoequipo.html`
- `list_tipobd.html`
- `list_ubicacion.html`
- `list_ambiente.html`
- `list_version.html`
- `list_so.html`
- `list_estados.html`
- `list_custodios.html`

#### **📊 Reportes**
- `exportar_inv_excel.html`
- `reporte_servidores.html`
- `reporte_guardias.html`

---

### **🔥 NIVEL 3: MODERADO (Funcionalidades Específicas)**

#### **📈 Gráficas y Análisis**
- `horas_por_bd.html`
- `horas_por_ambiente.html`
- `horas_por_analista.html`
- `horas_por_actividades.html`

#### **🔐 Administración**
- `plugin_useradmin/index.html`
- `plugin_manage_groups/group.html`

#### **📚 Wiki y Documentación**
- `list_program.html`

---

### **🔥 NIVEL 4: BAJO USO (Mantenimiento/Admin)**

#### **🛠 Formularios de Edición**
- `edit_basedatos.html`
- `edit_servidor.html`
- `edit_actividad.html`
- `edit_rutinas.html`
- `edit_claves.html`

#### **👁 Vistas de Detalle**
- `view_basedatos.html`
- `view_servidor.html`
- `view_rutinas.html`

---

## 📊 **ESTADÍSTICAS DE USO ESTIMADAS**

### **Por Rol de Usuario:**

#### **DBA + ADMIN (Acceso Completo)**
- Dashboard: **diario** 🔥
- Inventario: **diario** 🔥  
- Monitor: **diario** 🔥
- Gestión Operativa: **semanal** 
- Administración: **mensual**

#### **DBA (Operaciones)**
- Monitor: **diario** 🔥
- Inventario: **diario** 🔥
- Gestión Operativa: **diario** 🔥
- Reportes: **semanal**

#### **OPERADOR (Solo Monitoreo)**
- Monitor: **diario** 🔥
- Dashboard: **diario** 🔥
- Estadísticas: **semanal**

---

## 🎯 **PLAN DE OPTIMIZACIÓN PROPUESTO**

### **FASE 1: CRÍTICAS (1-2 semanas)**
```
✅ dashboard.html (completado)
✅ list_basedatos.html (completado)
✅ monitor_graf.html (completado)
✅ list_servidores.html (completado)
⏳ crear_actividades_sd.html
⏳ list_actividades_sd.html
```

### **FASE 2: IMPORTANTES (2-3 semanas)**
```
⏳ list_dba.html
⏳ oracle/ejecutar_sql.html
⏳ rutinas_asignadas.html
⏳ asignar_rutinas.html
⏳ exportar_inv_excel.html
⏳ reporte_servidores.html
```

### **FASE 3: MODERADO (1-2 semanas)**
```
⏳ horas_por_*.html (4 archivos)
⏳ plugin_useradmin/index.html
⏳ list_program.html
```

### **FASE 4: BAJO USO (según necesidad)**
```
⏳ edit_*.html (múltiples archivos)
⏳ view_*.html (múltiples archivos)
⏳ Formularios auxiliares
```

---

## 🚫 **VISTAS PROBABLEMENTE NO UTILIZADAS**

### **Candidatos para Revisión/Eliminación:**
```
- crear_actividades.html (versión antigua)
- list_actividades.html (versión antigua)
- monitor.html (versión antigua)
- *.html con sufijo (copia), _old, _ant
- Archivos de prueba: prueba_*.html
- Versiones duplicadas: *2.html, *x.html
```

### **Archivos Identificados como Obsoletos:**
```
- bitacora_actividades_sd (copia).html
- monitor_graf-v-ant.html
- monitor_graf - copia.html
- list_bd_online_grafica - copia.html
- lista_bd_servidores - copia.html
- list_tipobdxxx.html
- reporte_novedadesx.html
```

---

## 📋 **CHECKLIST DE VERIFICACIÓN**

### **Para confirmar uso real:**
- [ ] Analizar logs de acceso del servidor web
- [ ] Revisar enlaces en las vistas principales
- [ ] Verificar JavaScript que hace llamadas AJAX
- [ ] Consultar con usuarios finales sobre funcionalidades

### **Para cada vista a optimizar:**
- [ ] Identificar CSS duplicado
- [ ] Verificar funcionalidad actual
- [ ] Aplicar CSS común
- [ ] Probar responsive design
- [ ] Validar con usuarios

---

## 🏆 **PRIORIZACIÓN FINAL**

### **Optimizar INMEDIATAMENTE:**
1. `monitor_graf.html` (usado diariamente)
2. `list_servidores.html` (inventario crítico)
3. `crear_actividades_sd.html` (gestión operativa)

### **Optimizar SIGUIENTE:**
4. `list_actividades_sd.html`
5. `rutinas_asignadas.html`
6. `asignar_rutinas.html`

### **Revisar y posiblemente ELIMINAR:**
- Todos los archivos con "(copia)"
- Archivos con sufijos _old, _ant, xxx
- Vistas no referenciadas en menús ni controladores

---

**Fecha**: 26 de Junio, 2025  
**Estado**: Análisis Completado  
**Siguiente**: Optimizar vistas prioritarias
