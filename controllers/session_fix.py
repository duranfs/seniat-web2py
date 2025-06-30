def force_db_sessions():
    """Fuerza el uso de la base de datos para sesiones"""
    from gluon import current
    
    # 1. Eliminar sesiones en memoria
    current.session._unlock(current.response)
    current.session.clear()
    
    # 2. Reconfigurar conexión
    current.session.connect(
        current.request,
        current.response,
        db=current.db,
        tablename='web2py_session',
        separate_metadata=True
    )
    
    # 3. Iniciar nueva sesión en DB
    current.session._start()
    
    # 4. Verificar
    test_data = {'test': datetime.now()}
    current.session.test_var = test_data
    current.session._store()
    
    return dict(
        status="Sesión forzada a DB",
        session_id=current.session._uniquer,
        db_record=db(db.web2py_session.unique_key==current.session._uniquer).select().first()
    )