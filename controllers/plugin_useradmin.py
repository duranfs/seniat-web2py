'''
Basic User Administration
Fixed redirect loop issue
'''

from gluon.sqlhtml import form_factory

@auth.requires(auth.has_membership(auth.id_group('SYSTEM')))
def index():
    # Verificar si ya estamos procesando una redirección
    if request.env.request_method == 'POST' and not request.post_vars:
        redirect(URL(args=request.args, vars=request.get_vars))
    
    # Manejar acciones POST
    if request.post_vars:
        if request.post_vars.get('block_user'):
            db(db.auth_user.id == request.post_vars.get('block_user')).update(registration_key='blocked')
            session.flash = "User Blocked"
            redirect(URL(args=request.args))
            
        elif 'unblock_user' in request.post_vars:
            db(db.auth_user.id == request.post_vars.get('unblock_user')).update(registration_key='')
            session.flash = "User Unblocked"
            redirect(URL(args=request.args))
            
        elif 'del_user' in request.post_vars:
            db(db.auth_user.id == request.post_vars.get('del_user')).delete()
            session.flash = "User Deleted"
            redirect(URL(args=request.args))
            
        elif 'approve' in request.post_vars:
            db(db.auth_user.id == request.post_vars['approve']).update(registration_key='')
            session.flash = 'Approved user %s' % db(db.auth_user.id == request.post_vars['approve']).select()[0].first_name
            redirect(URL(args=request.args))
            
        elif 'del_usergroup' in request.post_vars:
            user_id, group_id = request.post_vars['del_usergroup'].split('_')
            db((db.auth_membership.user_id == user_id) & (db.auth_membership.group_id == group_id)).delete()
            session.flash = "Group Deleted"
            redirect(URL(args=request.args))
            
        elif 'del_group' in request.post_vars:
            db(db.auth_group.id == request.post_vars.get('del_group')).delete()
            session.flash = "Group Deleted"
            redirect(URL(args=request.args))

    # Obtener datos
    users = db(db.auth_user.id > 0).select(orderby=db.auth_user.registration_key)
    groups = db(db.auth_group.id > 0).select()
    
    # Formularios
    forms_users_groups = {}
    for user in users:
        forms_users_groups[user.id] = form_factory(
            Field('group_id', label="Add Group", requires=IS_IN_DB(db, 'auth_group.id', '%(role)s')),
            formname='fug%s' % user.id
        )
        
        if forms_users_groups[user.id].process(formname='fug%s' % user.id).accepted:
            role = db.auth_group[forms_users_groups[user.id].vars.group_id]
            session.flash = T('Added to group [%s] user %s' % (role.role, user.first_name))
            if not db((db.auth_membership.user_id == user.id) & 
                    (db.auth_membership.group_id == forms_users_groups[user.id].vars.group_id)).count():
                db.auth_membership.insert(
                    user_id=user.id,
                    group_id=forms_users_groups[user.id].vars.group_id
                )
            redirect(URL(args=request.args))

    form_group = SQLFORM(db.auth_group, formname='form_group')
    if form_group.process(formname='form_group').accepted:
        session.flash = 'Created New Group'
        redirect(URL(args=request.args))
    
    # Configuración de DataTables
    response.files.append(URL(request.application, 'static', 'data_table.css'))
    response.files.append(URL(request.application, 'static/DataTables/media/js', 'jquery.DataTables.min.js'))
    script = SCRIPT('''$(document).ready(function(){
        oTable = $('#useradmin-table').dataTable({
            "bStateSave": true, 
            "sPaginationType": "full_numbers",
            "aaSorting": [[0, "asc"]]
        });
    });''')
    
    return dict(
        users=users,
        forms_users_groups=forms_users_groups,
        form_group=form_group,
        db_groups=groups,
        script=script
    )


# ... (resto de las funciones se mantienen igual)

@auth.requires(auth.has_membership(auth.id_group('ADMIN')))
def page():
    response.files.append(URL(request.application, 'static/plugin_useradmin', 'base.css'))
    response.files.append(URL(request.application, 'static', 'data_table.css'))
    response.files.append(URL(request.application, 'static/DataTables/media/js', 'jquery.DataTables.min.js'))
    
    script = SCRIPT('''$(document).ready(function(){
        oTable = $('#useradmin-table').dataTable({
            "bStateSave": true, 
            "sPaginationType": "full_numbers"
        });
    });''')
    
    return dict(script=script)

@auth.requires(auth.has_membership(auth.id_group('ADMIN')))
def edit_user():
    record_id = request.args(0)
    if not record_id:
        form = crud.create(db.auth_user)
    else:
        form = crud.update(db.auth_user, record_id, deletable=False)
    return form

@auth.requires(auth.has_membership(auth.id_group('ADMIN')))
def edit_role():
    record_id = request.args(0)
    if not record_id:
        form = crud.create(db.auth_group)
    else:
        form = crud.update(db.auth_group, record_id, deletable=False)
    return form