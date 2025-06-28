# Gestión de Sesiones Activas

## Descripción

Esta funcionalidad permite a los administradores del sistema gestionar las sesiones activas de los usuarios conectados a la aplicación web2py. Proporciona una interfaz web para:

- Ver todas las sesiones activas
- Identificar usuarios conectados
- Ver tiempo de inactividad de cada sesión
- Terminar sesiones individuales
- Terminar todas las sesiones (excepto la del administrador)

## Características

### Vista Principal (`manage_sessions`)
- **Tabla de sesiones activas** con información detallada:
  - ID de sesión (truncado para seguridad)
  - Nombre del usuario
  - Email del usuario
  - Última actividad
  - Tiempo de inactividad (en segundos, minutos u horas)
  - Estado de la sesión (Activa, Incompleta, Corrupta)

### Funcionalidades de Control
- **Terminar sesión individual**: Botón para desconectar un usuario específico
- **Terminar todas las sesiones**: Opción para desconectar a todos los usuarios excepto el administrador actual
- **Auto-refresh**: La página se actualiza automáticamente cada 30 segundos
- **Confirmaciones**: Modales de confirmación antes de realizar acciones destructivas

### Seguridad
- Solo usuarios con membresía 'ADMIN' pueden acceder
- Protección contra terminación de la sesión del administrador actual
- Manejo de sesiones corruptas o vacías
- Validación de parámetros de entrada

## Archivos Creados/Modificados

### Controlador (`controllers/default.py`)
- `manage_sessions()`: Función principal que muestra la vista
- `terminate_session()`: Termina una sesión específica
- `terminate_all_sessions()`: Termina todas las sesiones excepto la del administrador

### Vista (`views/default/manage_sessions.html`)
- Interfaz web completa con Bootstrap
- Tabla responsiva con información de sesiones
- Modales de confirmación
- JavaScript para interacciones

### Menú (`models/menu.py`)
- Enlace agregado en el menú de Administración

## Uso

### Acceso
1. Iniciar sesión como administrador
2. Ir al menú "Administración" → "Control de Sesiones"

### Operaciones Disponibles

#### Ver Sesiones Activas
- La página muestra automáticamente todas las sesiones activas
- Se actualiza cada 30 segundos automáticamente
- Las sesiones se ordenan por tiempo de inactividad (más inactivas primero)

#### Terminar Sesión Individual
1. Hacer clic en el botón "Terminar" en la fila de la sesión deseada
2. Confirmar la acción en el modal que aparece
3. La sesión será terminada inmediatamente

#### Terminar Todas las Sesiones
1. Hacer clic en el botón "Terminar Todas las Sesiones"
2. Confirmar la acción en el modal de advertencia
3. Todas las sesiones serán terminadas excepto la del administrador actual

## Información Técnica

### Estructura de Datos de Sesión
```python
{
    'session_id': 'ID único de la sesión',
    'user_id': 'ID del usuario en auth_user',
    'user_email': 'Email del usuario',
    'user_name': 'Nombre completo del usuario',
    'last_activity': 'Fecha/hora de última actividad',
    'idle_time': 'Tiempo transcurrido desde última actividad',
    'file_path': 'Ruta del archivo de sesión'
}
```

### Estados de Sesión
- **Activa**: Sesión válida con usuario autenticado
- **Incompleta**: Sesión sin información de usuario completa
- **Corrupta**: Archivo de sesión dañado o no legible

### Permisos Requeridos
- `@auth.requires_membership('ADMIN')`: Solo administradores pueden acceder

## Consideraciones de Seguridad

1. **Protección de Sesión del Administrador**: La función `terminate_all_sessions()` excluye automáticamente la sesión del administrador que ejecuta la acción.

2. **Validación de Entrada**: Todas las funciones validan los parámetros de entrada antes de procesarlos.

3. **Manejo de Errores**: Las funciones incluyen manejo de excepciones para evitar errores del sistema.

4. **Logging**: Las acciones de terminación de sesiones generan mensajes flash para auditoría.

## Mantenimiento

### Limpieza Automática
- Las sesiones corruptas se muestran pero no se pueden terminar individualmente
- Se recomienda revisar periódicamente las sesiones inactivas por largos períodos

### Monitoreo
- La página se actualiza automáticamente cada 30 segundos
- Los administradores pueden monitorear la actividad en tiempo real

## Troubleshooting

### Problemas Comunes

1. **No se muestran sesiones**: Verificar que el directorio `sessions/` existe y tiene permisos de lectura.

2. **Error al terminar sesión**: Verificar permisos de escritura en el directorio `sessions/`.

3. **Sesiones corruptas**: Estas se muestran como "Corrupta" y no afectan el funcionamiento del sistema.

### Logs
- Los errores se muestran como mensajes flash en la interfaz
- Revisar los logs del servidor web2py para errores adicionales 