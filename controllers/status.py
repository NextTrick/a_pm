# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

@auth.requires_membership('root')
def registered_users():
    response.view = 'default.html'
    title = T('Registered Users')
    db.registered_users.server_id.represent = lambda  value, row: None if value is None else name_data(db.services_servers, value, "host_ip")
#    db.current_calls.call_state.represent = lambda  value, row: None if value is None else calling_status[value]
    form_grid = SQLFORM.grid(db.registered_users,
                        editable=False, deletable=False,
                        create=False, details=False,
                        paginate=50,
                        fields=[db.registered_users.login_account,
                                db.registered_users.registration_time,db.registered_users.location_server_ip_address,
                                db.registered_users.server_id
                                ])
    return dict(form=form_grid, title=title)

@auth.requires_membership('root')
def current_calls():
    response.view = 'default.html'
    title = T('Current Calls')
    db.current_calls.server_id.represent = lambda  value, row: None if value is None else name_data(db.services_servers, value, "host_ip")
    db.current_calls.call_state.represent = lambda  value, row: None if value is None else calling_status[value]
    form_grid = SQLFORM.grid(db.current_calls,
                        editable=False, deletable=False,
                        create=False, details=False,
                        paginate=50,
                        fields=[db.current_calls.account, db.current_calls.account_state,
                                db.current_calls.ani,
                                db.current_calls.dialed_number, db.current_calls.call_start,
                                db.current_calls.duration, db.current_calls.tariffdesc,
                                db.current_calls.route,
                                db.current_calls.call_state, db.current_calls.server_id
                                ])
    return dict(form=form_grid, title=title)


@auth.requires_membership('root')
def customer_current_calls():
    response.view = 'default.html'
    title = T('Current Calls')
    db.current_calls.server_id.represent = lambda  value, row: None if value is None else name_data(db.services_servers, value, "host_ip")
    db.current_calls.call_state.represent = lambda  value, row: None if value is None else calling_status[value]
    form_grid = SQLFORM.grid(db.current_calls,
                        editable=False, deletable=False,
                        create=False, details=False,
                        paginate=50,
                        fields=[db.current_calls.account, db.current_calls.account_state,
                                db.current_calls.ani,
                                db.current_calls.dialed_number, db.current_calls.call_start,
                                db.current_calls.duration, db.current_calls.tariffdesc,
                                db.current_calls.call_state, db.current_calls.server_id
                                ])
    return dict(form=form_grid, title=title)

#@auth.requires_membership('root')
@auth.requires_membership('sales')
def accounts():
    user_id = auth.user.id
    sales_user_id = 1
    sales_user = auth.has_membership(role='sales')
    root_user = auth.has_membership(role='root')
    if sales_user:
        sales_user_id = db.sellers(db.sellers.related_user == user_id).id
        query = ((db.accounts.seller == sales_user_id))
    else:
        query = ((db.accounts.id > 0))

    response.view = 'default.html'
    title = T('Accounts')
    db.accounts.server_id.represent = lambda  value, row: None if value is None else name_data(db.services_servers, value, "host_ip")
#    db.current_calls.call_state.represent = lambda  value, row: None if value is None else calling_status[value]

    form_grid = SQLFORM.grid(query,
                        editable=False, deletable=False,
                        create=False, details=False)
    return dict(form=form_grid, title=title)