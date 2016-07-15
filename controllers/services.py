# -*- coding: utf-8 -*-
import time
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires


@auth.requires_login()
def index():
    customer = auth.user.customer
    try:
        customer_type = db.customers(db.customers.id==customer).account_type
    except:
        customer_type = None
    user = auth.user.id
    customer = auth.user.customer
    data = db.customers(db.customers.id==customer)
    year = now.year
    month = now.month - 1 or 12
    if month == 12:
        year = now.year -1
    day = now.day
    try:
        last = datetime.datetime(year, month, day)
    except:
        last = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    val_start = last
    val_end = datetime.datetime.now()
    cliente_condition = customer
    vendedor_condition = 'TODOS'
    cuenta_condition = ''
    currency = data.currency
    # credits = db(db.customers_credits.customer==customer).select(
    #     db.customers_credits.register_time,
    #     db.customers_credits.currency, db.customers_credits.amount,
    #     db.customers_credits.customer_amount,
    #     db.customers_credits.notes, limitby=(0,10))
    # query="""select pay.data,pay.money,typ.name,pay.description,pay.actual_value,
    #     if(pay.type>2,pay.actual_value-pay.money,pay.actual_value+pay.money) as final
    #     from payments pay left join paymenttypes typ on typ.id=pay.type
    #     where pay.id_client=13 and pay.client_type=32;"""

    # services = db((db.customers_services.customer==customer)).select(
    #     db.customers_services.service, db.customers_services.package,
    #     db.customers_services.start_date,db.customers_services.billing_period,
    #     db.customers_services.status, db.customers_services.account
    # )
    costos, consumo, minutos, llamadas, ganancia, rentabilidad, content = data_graphics(
        val_start, val_end, cliente_condition,
        vendedor_condition, cuenta_condition, currency)
    elem = [val_start,val_end,cliente_condition,vendedor_condition,cuenta_condition,currency]
    elem_aux = [costos, consumo, minutos, llamadas, ganancia, rentabilidad, content]
    form = SQLFORM.factory(
        Field('alerta', 'boolean', label=T('Alerta')),
        Field('monto', 'float', label=T('Monto'), default=100),
    )
    if data is None:
        redirect(URL('default', 'index'))
    return dict(form=form, data=data, consumo=consumo, minutos=minutos, llamadas=llamadas, customer_type=customer_type)
    #return dict(data=data, services=services, credits=credits)


def error():
    return dict()

@auth.requires_login()
def service_list():
    user = auth.user.id
    customer = auth.user.customer
    role = 'user'
    try:
        customer_type = db.customers(db.customers.id==customer).account_type
    except:
        customer_type = None
    area = db.areas(db.areas.name=='Ventas')
    if auth.has_membership(user_id=user, role='root'):
        query = (db.customers_services.customer>0)
    else:
        query = (db.customers_services.customer==customer)
    service_rows = db(query).select(
        db.customers_services.id,
        db.customers_services.service,
        db.customers_services.customer_contract, db.customers_services.package,
        db.customers_services.start_date, db.customers_services.billing_period,
        db.customers_services.account, db.customers_services.password,
        db.customers_services.did,db.customers_services.monthly,
        db.customers_services.currency,db.customers_services.status,
        db.customers_services.server_host,db.customers_services.server_port,
        orderby=db.customers_services.service
    )
    return dict(role=role, area=area.id, service_rows=service_rows, customer_type=customer_type)

@auth.requires_login()
def graphical_reports():
    user = auth.user.id
    customer = auth.user.customer
    data = db.customers(db.customers.id==customer)
    year = now.year
    month = now.month - 1 or 12
    if month == 12:
        year = now.year -1
    day = now.day
    try:
        last = datetime.datetime(year, month, day)
    except:
        last = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    val_start = last
    val_end = datetime.datetime.now()
    cliente_condition = 'TODOS'
    vendedor_condition = 'TODOS'
    cuenta_condition = request.vars.customer_service
    currency = data.currency
    costos, consumo, minutos, llamadas, ganancia, rentabilidad, content = data_graphics(
        val_start, val_end, cliente_condition,
        vendedor_condition, cuenta_condition, currency)
    if data is None:
        redirect(URL('default', 'index'))
    return dict(data=data, consumo=consumo, minutos=minutos, llamadas=llamadas)


@auth.requires_login()
def did_list():
    user = auth.user.id
    customer = auth.user.customer
    role = 'user'
    area = db.areas(db.areas.name=='Ventas')
    if auth.has_membership(user_id=user, role='root'):
        query = (db.customers_services.customer>0)
    else:
        query = (db.customers_services.customer==customer)
    did_rows = db((db.customers_services.service==0) &
                  query).select(
        db.customers_services.customer_contract, db.customers_services.package,
        db.customers_services.start_date, db.customers_services.billing_period,
        db.customers_services.account, db.customers_services.password,
        db.customers_services.did,db.customers_services.monthly,
        db.customers_services.currency,db.customers_services.status,
        db.customers_services.server_host,db.customers_services.server_port
    )
    return dict(role=role, area=area.id, did_rows=did_rows)


@auth.requires_login()
def did_rates():
    user = auth.user.id
    customer = auth.user.customer
    role = 'user'
    area = db.areas(db.areas.name=='Ventas')
    did_rows = db((db.packages.service==0) & (db.packages.status==0)).select(
        db.packages.name, db.packages.currency, db.packages.setup_fee,
        db.packages.monthly_fee, orderby=db.packages.name
    )
    return dict(role=role, area=area.id, did_rows=did_rows)


@auth.requires_login()
def did_requests():
    user = auth.user.id
    customer = auth.user.customer
    role = 'user'
    area = db.areas(db.areas.name=='Ventas')
    if auth.has_membership(user_id=user, role='root'):
        data = db((db.tickets.service==0) &
                  (db.tickets.area==area.id)).select()
        role = 'admin'
    else:
        data = db((db.tickets.service==0) &
                  (db.tickets.customer==customer) &
                  (db.tickets.area==area.id)).select()
    #print did_rows
    return dict(data=data, role=role, area=area.id)


@auth.requires_login()
def add_funds():
    user = auth.user.id
    customer = auth.user.customer
    if auth.has_membership(user_id=user, role='root'):
        editable = True
    else:
        editable = False
    db.customers_credits.customer.default = customer
    db.customers_credits.customer.writable = False
    db.customers_credits.customer_amount.writable = False
    db.customers_credits.status.default = 0
    db.customers_credits.status.writable = editable
    query = (db.customers_credits.customer==customer)
    form = SQLFORM.grid(query, fields=[db.customers_credits.customer,
                                       db.customers_credits.register_time,
                                       db.customers_credits.currency,
                                       db.customers_credits.amount,
                                       db.customers_credits.customer_amount,
                                       db.customers_credits.login_reference,
                                       db.customers_credits.notes,
                                       db.customers_credits.status,
                                       ],
                        deletable=False, editable=editable)
    return dict(form=form)


@auth.requires_login()
def credits():
    customer = auth.user.customer
    query = (db.customers_credits.customer==customer)
    form = SQLFORM.grid(query,
            fields=[
                db.customers_credits.register_time,
                db.customers_credits.credit_type,
                db.customers_credits.customer,
                db.customers_credits.login_reference,
                db.customers_credits.currency,
                db.customers_credits.amount,
                db.customers_credits.customer_amount,
                db.customers_credits.notes,
                db.customers_credits.status,
                   ],
            editable=False, deletable=False, create=False, paginate=50,
            exportclasses=dict(xml=False, html=False, json=False, tsv=False,
                     tsv_with_hidden_cols=False)
            )
    return dict(form=form)


@auth.requires_login()
def whitelist():
    user = auth.user.id
    customer = auth.user.customer
    data = db((db.customers_services.customer==customer) &
                  (db.customers_services.service==1)).select(
        db.customers_services.id, db.customers_services.account)
    customer_services = {}
    for row in data:
        customer_services[row.id] = row.account
    query = db.whitelist_destinations.customer_service.requires = IS_IN_SET(
        customer_services)
    form = SQLFORM.smartgrid(db.whitelist_destinations,
        #linked_tables=['customers_contracts_documents'],
        constraints=dict(customers_services=query),
        deletable=False
        )
    return dict(form=form)


@auth.requires_login()
def blacklist():
    user = auth.user.id
    customer = auth.user.customer
    data = db((db.customers_services.customer==customer) &
                  (db.customers_services.service==1)).select(
        db.customers_services.id, db.customers_services.account)
    customer_services = {}
    for row in data:
        customer_services[row.id] = row.account
    query = db.blacklist_destinations.customer_service.requires = IS_IN_SET(customer_services)
    form = SQLFORM.smartgrid(db.blacklist_destinations,
        #linked_tables=['customers_contracts_documents'],
        constraints=dict(customers_services=query),
        deletable=False
        )
    data_voip(1)
    return dict(form=form)


@auth.requires_login()
def voip_accounts():
    user = auth.user.id
    customer = auth.user.customer
    service = request.vars.service
    role = 'user'
    area = db.areas(db.areas.name=='Ventas')
    if auth.has_membership(user_id=user, role='root'):
        query = (db.customers_services.customer>0)
    else:
        query = (db.customers_services.customer==customer)
    voip_rows = db((db.customers_services.service==service) &
                  query).select(
        db.customers_services.id,
        db.customers_services.customer_contract, db.customers_services.package,
        db.customers_services.start_date, db.customers_services.billing_period,
        db.customers_services.account, db.customers_services.password,
        db.customers_services.did,db.customers_services.monthly,
        db.customers_services.currency,db.customers_services.status
    )
    return dict(voip_rows=voip_rows)

@auth.requires_login()
def retail_rates():
    user = auth.user.id
    customer = auth.user.customer
#    user = auth.user.id
#     data = dict(request.vars)
#     data_aux = request.args
#     if 'devengado' in data:
#         customer_service = data['customer_service']
#         currency = data['currency']
#     else:
#         try:
#             customer_service = data_aux[0]
#         except:
#             customer_service = None
#         try:
#             currency = data_aux[1]
#         except:
#             currency = None
    customer_service = request.vars.customer_service
    currency = request.vars.currency
    try:
        information = data_voip(customer_service)
    except:
        redirect('voip_accounts')
    if len(information) == 0:
        redirect('voip_accounts')
    code_tariff = "%s%s" % (information[0], information[4])
    query = (db.tariffs_integrated.id==code_tariff)
    form = SQLFORM.grid(query, fields=[db.tariffs_integrated.code_prefix,
                                       db.tariffs_integrated.description,
                                       db.tariffs_integrated.voice_rate],
                        editable=False, deletable=False, create=False, details=False,
#                        args=[customer_service, currency]
                        )
    # extra_element = INPUT(_type='hidden', _name='customer_service', _value=customer_service)
    # form[0].insert(-1,extra_element)
    # extra_element = INPUT(_type='hidden', _name='currency', _value=currency)
    # form[0].insert(-1,extra_element)
    return dict(form=form, currency=currency, customer_service=customer_service)


@auth.requires_login()
def retail_cdr():
    user = auth.user.id
    customer = auth.user.customer
    customer_service = request.vars.customer_service
    #information = data_voip(customer_service)
    #if len(information) == 0:
    #    redirect('voip_accounts')
    #query = """select prefix, description, voice_rate from tariffs where id_tariff=%s;""" % (information[4])
    #data = db2.executesql(query)
    daily = get_dates(0)
    weekly = get_dates(1)
    half_monthly = get_dates(2)
    monthly = get_dates(3)
    return dict(customer_service=customer_service, daily=daily, weekly=weekly,
                half_monthly=half_monthly, monthly=monthly)



# @auth.requires_login()
# def export_data():
#     start_date = request.vars.start_date
#     end_date = request.vars.end_date
#     customer_service = request.vars.customer_service
#     kind = str(request.vars.kind)
#     information = data_voip(customer_service)
#     if len(information) == 0:
#         redirect('retail_cdr')
#     name_client = information[1]
#     id_client = information[2]
#     type_client = information[7]
#     sip_proxy = information[9]
#     if start_date == end_date:
#         condition = "call_start='%s'" % (start_date)
#     else:
#         condition = "call_start between date('%s') and date('%s')" % (start_date, end_date)
#     if kind == '1':
#         query = """select '%s' as id_client, caller_id, called_number,
#             call_start, call_end, (call_end - call_start) as duration,
#             costD as rate, cost, tariffdesc as destination,
#             ip_number, '%s' as sip_proxy from calls where id_client='%s' and client_type='%s'
#             and %s""" % (name_client, sip_proxy, id_client, type_client, condition)
#     else:
#         query = """select '%s' as id_client, caller_id, called_number,
#             call_start, release_reason, tariffdesc as destination,
#             ip_number, '%s' as sip_proxy from calls where id_client='%s' and client_type='%s'
#             and %s""" % (name_client, sip_proxy, id_client, type_client, condition)
#     data = db2.executesql(query)
#     return dict(data=data, basename='sucess-calls')

@auth.requires_login()
def export_data():
    start_date = request.vars.start_date
    end_date = request.vars.end_date
    customer_service = request.vars.customer_service
    kind = str(request.vars.kind)
    information = data_voip(customer_service)
    if len(information) == 0:
        redirect('retail_cdr')
    name_client = information[1]
    # id_client = information[2]
    # type_client = information[7]
    # sip_proxy = information[9]
    if start_date == end_date:
        condition = "date(call_start)='%s'" % (start_date)
    else:
        start_date = "%s 00:00:00" % start_date
        end_date = "%s 23:59:59" % end_date
        condition = "(call_start between '%s' and '%s')" % (start_date, end_date)
    if kind == '1':
        query = """select acc.login as id_client, caller_id, called_number,
            date_format(call_start, '%%d/%%m/%%Y %%H:%%i:%%S') as call_start,
            date_format(call_end, '%%d/%%m/%%Y %%H:%%i:%%S') as call_end, duration,
            call_rate as rate, round(cost*ratio,4), tariffdesc as destination,
            ip_number, acc.sip_proxy as sip_proxy from calls left join accounts acc on
            acc.id_client=calls.id_client and acc.client_type=calls.client_type
            and acc.server_id=calls.server_id
            where acc.login='%s' and %s order by call_start,
            call_end""" % (name_client, condition)
        basename = "cdr_%s_%s-%s" % (name_client, start_date, end_date)
        column_names = ['id_client', 'caller_id', 'called_number', 'call_start',
                    'call_end', 'duration', 'rate', 'cost', 'destination', 'ip_number', 'sip_proxy']
    else:
        query = """select acc.login as id_client, caller_id, called_number,
            date_format(call_start, '%%d/%%m/%%Y %%H:%%i:%%S') as call_start, release_reason, tariffdesc as destination,
            ip_number, acc.sip_proxy as sip_proxy from callsfailed calls    left join accounts acc on
            acc.id_client=calls.id_client and acc.client_type=calls.client_type
            and acc.server_id=calls.server_id
            where acc.login='%s'
            and %s order by call_start,called_number""" % (name_client,condition)
        basename = "cdr_failed_%s_%s-%s" % (name_client, start_date, end_date)
        column_names = ['id_client', 'caller_id', 'called_number', 'call_start',
                    'release_reason', 'destination', 'ip_number', 'sip_proxy']
    data = db2.executesql(query)
    csv_stream = csv_export(data, column_names, None, mode = 'list')
    dateval = time.strftime('%Y-%m-%d')
    filename = "%s--%s.csv" % (basename, dateval)
    disposition = 'attachment; filename=%s' % filename
    response.headers['Content-Type']='application/vnd.ms-excel'
    response.headers['Content-Disposition']=disposition
    return csv_stream.getvalue()


def add_charges():
    customer = auth.user.customer
    db.customers_charges.customer.default = customer
    db.customers_charges.customer.writable = False
    form = SQLFORM.grid(db.customers_charges, fields=[
                db.customers_credits.customer,
                db.customers_credits.register_time,
                db.customers_credits.currency,
                db.customers_credits.amount,
                db.customers_credits.customer_amount,
                db.customers_credits.login_reference,
                db.customers_credits.notes,
                db.customers_credits.status,
                ],
            editable=False, deletable=False, create=False)
    return dict(form=form)


def data_graphics(val_start, val_end, cliente_condition,
        vendedor_condition, cuenta_condition, currency):
    if currency == 1:
        query = """select fecha,sum(intentos),sum(completados),sum(fallados),
            sum(minutos),sum(costoclientedoligv),sum(costoproveedor),
            sum(ganancia),ifnull(sum(costoclientedoligv-costoproveedor)/sum(costoproveedor)*100,0),
            cliente,cuenta,vendedor
            from resumen_cuenta where fecha between '%s' and '%s' """ % (val_start, val_end)
    else:
        query = """select fecha,sum(intentos),sum(completados),sum(fallados),
            sum(minutos),sum(costoclientesoligv),sum(costoproveedor),
            sum(ganancia),ifnull(sum(costoclientesoligv-costoproveedor)/sum(costoproveedor)*100,0),
            cliente,cuenta,vendedor
            from resumen_cuenta where fecha between '%s' and '%s' """ % (val_start, val_end)
    if cliente_condition != 'TODOS':
        query += "and cliente='%s' " % cliente_condition
    if vendedor_condition != 'TODOS':
        query += "and vendedor='%s' " % vendedor_condition
    if len(cuenta_condition) > 1:
        query += "and cuenta='%s'" % cuenta_condition
    query += "group by fecha;"
    data = db2.executesql(query)
    consumo = []
    costos = []
    minutos = []
    llamadas = []
    ganancia = []
    rentabilidad = []
    costos.append(['Fecha','Costo'])
    consumo.append(['Fecha', 'Consumo'])
    minutos.append(['Fecha', 'Minutos'])
    llamadas.append(['Fecha','Llamadas', 'Completadas', 'Falladas'])
    ganancia.append(['Fecha', 'Ganancia'])
    rentabilidad.append(['Fecha', 'Rentabilidad'])
    for line in data:
        costos.append(['%s' % line[0], round(float(line[6]),2)])
        consumo.append(['%s' % line[0], round(float(line[5]),2)])
        minutos.append(['%s' % line[0], round(float(line[4]),2)])
        llamadas.append(['%s' % line[0], int(line[1]), int(line[2]), int(line[3])])
        ganancia.append(['%s' % line[0], round(float(line[7]),2)])
        rentabilidad.append(['%s' % line[0], round(float(line[8]),2)])
    return costos, consumo, minutos, llamadas, ganancia, rentabilidad, data