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

#@auth.requires_membership('root')
@auth.requires_login()
def registered_users():
    response.view = 'default.html'
    title = T('Registered Users')
    user_id = auth.user.id
    sales_user_id = 1
    sales_user = auth.has_membership(role='sales')
    root_user = auth.has_membership(role='root')
    customers = []
    if sales_user:
        sales_user_id = db.sellers(db.sellers.related_user == user_id).id
        rows = db(db.accounts.seller == sales_user_id).select(db.accounts.id,
                                                              db.accounts.account,
                                                              orderby=db.accounts.account)
        if len(rows) < 1:
            return dict(form='', title=title)
        for row in rows:
            customers.append(row.account)
        query = ((db.registered_users.login_account.contains(customers)))
    else:
        query = ((db.registered_users.id > 0))
    db.registered_users.server_id.represent = lambda  value, row: None if value is None else name_data(db.services_servers, value, "host_ip")
#    db.current_calls.call_state.represent = lambda  value, row: None if value is None else calling_status[value]
    form_grid = SQLFORM.grid(query,
                        editable=False, deletable=False,
                        create=False, details=False,
                        paginate=50,
                        fields=[db.registered_users.login_account,
                                db.registered_users.registration_time,db.registered_users.location_server_ip_address,
                                db.registered_users.server_id
                                ])
    return dict(form=form_grid, title=title)

@auth.requires_membership('root')
#@auth.requires_login()
def current_calls():
    user_id = auth.user.id
    sales_user_id = 1
    sales_user = auth.has_membership(role='sales')
    root_user = auth.has_membership(role='root')
    customers = []
    if sales_user:
        sales_user_id = db.sellers(db.sellers.related_user == user_id).id
        rows = db(db.accounts.seller == sales_user_id).select(db.accounts.id,
                                                              db.accounts.account,
                                                              orderby=db.accounts.account)
        for row in rows:
            customers.append(row.account)
        #query = ((db.accounts.seller == sales_user_id) & (db.current_calls.account.contains(customers)))
        query = (db.current_calls.account.contains(customers))
    else:
        query = ((db.current_calls.id > 0))
    response.view = 'default.html'
    title = T('Current Calls')
    db.current_calls.server_id.represent = lambda  value, row: None if value is None else name_data(db.services_servers, value, "host_ip")
    db.current_calls.call_state.represent = lambda  value, row: None if value is None else calling_status[value]
    form_grid = SQLFORM.grid(query,
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


#@auth.requires_membership('root')
@auth.requires_login()
def customer_current_calls():
    user_id = auth.user.id
    sales_user_id = 1
    sales_user = auth.has_membership(role='sales')
    root_user = auth.has_membership(role='root')
    customers = []
    if sales_user:
        sales_user_id = db.sellers(db.sellers.related_user == user_id).id
        rows = db(db.accounts.seller == sales_user_id).select(db.accounts.id,
                                                              db.accounts.account,
                                                              orderby=db.accounts.account)
        for row in rows:
            customers.append(row.account)
        #query = ((db.accounts.seller == sales_user_id) & (db.current_calls.account.contains(customers)))
        query = (db.current_calls.account.contains(customers))
    else:
        query = ((db.current_calls.id > 0))
    response.view = 'default.html'
    title = T('Customer Current Calls')
    db.current_calls.server_id.represent = lambda  value, row: None if value is None else name_data(db.services_servers, value, "host_ip")
    db.current_calls.call_state.represent = lambda  value, row: None if value is None else calling_status[value]
    form_grid = SQLFORM.grid(query,
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
#@auth.requires_membership('sales')
@auth.requires_login()
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

@auth.requires_login()
def credits():
    user_id = auth.user.id
    sales_user = auth.has_membership(role='sales')
    if sales_user:
        sales_user_id = db.sellers(db.sellers.related_user == user_id).id
        query = ((db.customers_credits.seller == sales_user_id))
    else:
        query = ((db.customers_credits.id > 0))
    response.view = 'default.html'
    title = T('Credits')
    #query = (db.customers_credits.customer == customer)
    db.customers_credits.register_time.writable = False
    db.customers_credits.credit_type.writable = False
    db.customers_credits.customer.writable = False
    db.customers_credits.seller.writable = False
    db.customers_credits.login_reference.writable = False
    db.customers_credits.currency.writable = False
    db.customers_credits.amount.writable = False
    db.customers_credits.customer_amount.writable = False
    db.customers_credits.notes.writable = False
    db.customers_credits.service.writable = False
    db.customers_credits.condition_status.writable = False
    form = SQLFORM.grid(query,
                        editable=True, deletable=False,
                        create=False, paginate=50,
                        fields=[
                            db.customers_credits.register_time,
                            db.customers_credits.credit_type,
                            db.customers_credits.customer,
                            db.customers_credits.seller,
                            db.customers_credits.login_reference,
                            db.customers_credits.currency,
                            db.customers_credits.amount,
                            db.customers_credits.customer_amount,
                            db.customers_credits.notes,
                            db.customers_credits.status,
                        ]
                        # exportclasses=dict(xml=False, html=False, json=False, tsv=False,
                        #          tsv_with_hidden_cols=False),
                        )
    # db.current_calls.server_id.represent = lambda  value, row: None if value is None else name_data(db.services_servers, value, "host_ip")
    # db.current_calls.call_state.represent = lambda  value, row: None if value is None else calling_status[value]
    # form_grid = SQLFORM.grid(db.current_calls,
    #                     editable=False, deletable=False,
    #                     create=False, details=False,
    #                     paginate=50,
    #                     fields=[db.current_calls.account, db.current_calls.account_state,
    #                             db.current_calls.ani,
    #                             db.current_calls.dialed_number, db.current_calls.call_start,
    #                             db.current_calls.duration, db.current_calls.tariffdesc,
    #                             db.current_calls.route,
    #                             db.current_calls.call_state, db.current_calls.server_id
    #                             ])
    # return dict(form_grid=form_grid)
    return dict(form=form, title=title)