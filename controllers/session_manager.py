# -*- coding: utf-8 -*-

def index():
    # Importar dentro de la función para garantizar el contexto correcto
    from gluon import current
    db = current.db
    request = current.request
    response = current.response
    session = current.session
    T = current.T
    auth = current.auth
    
    # Verificar permisos
    if not auth.has_membership('admin'):
        redirect(URL('default', 'user', args='not_authorized'))
    
    import os
    import datetime
    from gluon.storage import Storage
    
    # Configuración de ruta de sesiones
    session_folder = os.path.join(request.folder, 'sessions')
    
    # Verificar si existe el directorio de sesiones
    if not os.path.exists(session_folder):
        return dict(
            sessions=[],
            total_sessions=0,
            error="Directorio de sesiones no encontrado"
        )
    
    # Obtener archivos de sesión
    try:
        session_files = [f for f in os.listdir(session_folder) if f.startswith('session_')]
    except OSError:
        return dict(
            sessions=[],
            total_sessions=0,
            error="No se puede leer el directorio de sesiones"
        )
    
    sessions = []
    now = datetime.datetime.now()
    
    for session_file in session_files:
        try:
            session_path = os.path.join(session_folder, session_file)
            
            # Extraer ID de sesión de forma más segura
            if session_file.startswith('session_') and session_file.endswith('.pickle'):
                session_id = session_file[8:-7]  # 'session_' y '.pickle' tienen 8 y 7 caracteres
            else:
                continue  # Saltar archivos que no coincidan con el patrón
            
            last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(session_path))
            
            # Calcular duración
            duration = now - last_modified
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            duration_str = "%02d:%02d:%02d" % (hours, minutes, seconds)
            
            # Cargar datos de sesión
            session_data = Storage()
            session_data.load(session_path)
            
            # Obtener información relevante
            session_info = {
                'session_id': session_id,
                'client_ip': session_data.get('client_ip', 'Desconocido'),
                'last_activity': last_modified,
                'duration': duration_str,
                'auth_user': None
            }
            
            # Obtener información de usuario si está autenticado
            if 'auth' in session_data and session_data.auth.user:
                session_info['auth_user'] = db.auth_user(session_data.auth.user)
            
            sessions.append(session_info)
        except Exception as e:
            # Registrar error pero continuar
            import sys
            sys.stderr.write(f"Error procesando sesión {session_file}: {str(e)}\n")
            continue
    
    # Filtrar por búsqueda si existe
    search = request.vars.search
    if search:
        filtered_sessions = []
        for s in sessions:
            if s['auth_user']:
                if (search.lower() in s['auth_user'].email.lower() or 
                    search.lower() in s['auth_user'].first_name.lower() or
                    search.lower() in s['auth_user'].last_name.lower()):
                    filtered_sessions.append(s)
            elif search in s['client_ip'] or search in s['session_id']:
                filtered_sessions.append(s)
        sessions = filtered_sessions
    
    # Paginación simple (sin Crud para evitar dependencias)
    page = int(request.vars.page or 0)
    items_per_page = 20
    total_pages = (len(sessions) + items_per_page - 1) // items_per_page
    start = page * items_per_page
    end = min((page + 1) * items_per_page, len(sessions))
    paginated_sessions = sessions[start:end] if sessions else []
    
    return dict(
        sessions=paginated_sessions,
        total_sessions=len(sessions),
        current_page=page,
        total_pages=total_pages,
        prettydate=lambda dt: prettydate(dt, T)
    )

def kill_session():
    # Importar dentro de la función
    from gluon import current
    request = current.request
    session = current.session
    T = current.T
    auth = current.auth
    
    # Verificar permisos
    if not auth.has_membership('admin'):
        redirect(URL('default', 'user', args='not_authorized'))
    
    session_id = request.args(0)
    if not session_id:
        redirect(URL('index'))
    
    import os
    session_folder = os.path.join(request.folder, 'sessions')
    session_file = 'session_' + session_id + '.pickle'
    session_path = os.path.join(session_folder, session_file)
    
    try:
        os.remove(session_path)
        session.flash = T('Sesión terminada exitosamente')
    except Exception as e:
        session.flash = T('Error al terminar la sesión: %s') % str(e)
    
    redirect(URL('index'))