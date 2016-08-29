# -*- coding: utf-8 -*-
import collections
import csv
import decimal
import requests


### required - do no delete
def user(): return dict(form=auth())


def download(): return response.download(request, db)


def call(): return service()


### end requires
def index():
    return dict()


def error():
    return dict()


def get_csv():
    file_name = request.vars.file_name
    return dict(file_name=file_name)


# @auth.requires_membership('root')
# @auth.requires_membership('sales')
@auth.requires_login()
def customers_channels():
    user_id = auth.user.id
    # print auth.user_group(user_id)
    sales_user = auth.has_membership(role='sales')
    root_user = auth.has_membership(role='root')
    if root_user is False and sales_user is False:
        return
    # response.view = 'default.html'
    title = T('Graphics')
    year = now.year
    month = now.month - 1 or 12
    if month == 12:
        year = now.year - 1
    day = now.day
    try:
        last = datetime.datetime(year, month, day)
    except:
        last = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    customers = collections.OrderedDict()
    sellers = collections.OrderedDict()
    sales_code = False
    if sales_user:
        rows = db(db.sellers.related_user == user_id).select(db.customers.id,
                                                             db.customers.name, left=(
                db.customers.on(db.customers.id == db.customers_sellers.customer),
                db.sellers.on(db.sellers.id == db.customers_sellers.seller)
            ),
                                                             orderby=db.customers.name)
        for row in rows:
            customers[row.id] = "%s" % (row.name)
        customers['TODOS'] = 'TODOS'
        rows = db(db.sellers.related_user == user_id).select(db.sellers.id,
                                                             db.sellers.name, orderby=db.sellers.name)
        for row in rows:
            sellers[row.id] = "%s" % (row.name)
            sales_code = row.id
    else:
        rows = db(db.customers.id > 0).select(db.customers.id,
                                              db.customers.name, orderby=db.customers.name)
        for row in rows:
            customers[row.id] = "%s" % (row.name)
        # customers = sorted(customers.items(), key=lambda x: customers[x])
        customers['TODOS'] = 'TODOS'
        rows = db(db.sellers.id > 0).select(db.sellers.id,
                                            db.sellers.name, orderby=db.sellers.name)
        for row in rows:
            sellers[row.id] = "%s" % (row.name)
        sellers['TODOS'] = 'TODOS'
    if len(request.vars) > 0:
        try:
            val_start = datetime.datetime.strptime(request.vars.start_time, '%d/%m/%Y')
            val_end = datetime.datetime.strptime(request.vars.end_time, '%d/%m/%Y')
        except:
            val_start = datetime.datetime.strptime(request.vars.start_time, '%Y-%m-%d')
            val_end = datetime.datetime.strptime(request.vars.end_time, '%Y-%m-%d')
        cliente_condition = request.vars.cliente
        if len(cliente_condition) < 1:
            cliente_condition = 'TODOS'
        vendedor_condition = request.vars.vendedor
        if len(vendedor_condition) < 1:
            vendedor_condition = 'TODOS'
        cuenta_condition = request.vars.cuenta
    else:
        val_start = last
        val_end = datetime.datetime.now()
        cliente_condition = 'TODOS'
        cuenta_condition = ''
    if sales_user:
        vendedor_condition = sales_code
    else:
        vendedor_condition = 'TODOS'
    val_start = val_start.date()
    val_end = val_end.date()
    form = SQLFORM.grid(db.channels_customers)
    form_aux = SQLFORM.factory(
        Field('start_time', 'date', label=T('Start Date'), default=val_start),
        Field('end_time', 'date', label=T('End Date'), default=val_end),
        Field('cliente', label=T('Customer'), default=cliente_condition, requires=IS_IN_SET(customers)),
        Field('cuenta', 'string', default=cuenta_condition, label=T('Account')),
        Field('vendedor', label=T('Seller'), default=vendedor_condition, requires=IS_IN_SET(sellers)),
    )
    if form_aux.process(formname='factory').accepted:
        val_start = form_aux.vars.start_time
        val_end = form_aux.vars.end_time
        #cliente_condition = form.vars.cliente
        #vendedor_condition = form.vars.vendedor
        #cuenta_condition = form.vars.cuenta
        print val_start, val_end
    return dict(form=form, form_aux=form_aux)


@auth.requires_login()
def customers_channels_test():
    user_id = auth.user.id
    # print auth.user_group(user_id)
    sales_user = auth.has_membership(role='sales')
    root_user = auth.has_membership(role='root')
    if root_user is False and sales_user is False:
        return
    # response.view = 'default.html'
    title = T('Graphics')
    year = now.year
    month = now.month - 1 or 12
    if month == 12:
        year = now.year - 1
    day = now.day
    try:
        last = datetime.datetime(year, month, day)
    except:
        last = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    customers = collections.OrderedDict()
    sellers = collections.OrderedDict()
    sales_code = False
    if sales_user:
        rows = db(db.sellers.related_user == user_id).select(db.customers.id,
                                                             db.customers.name, left=(
                db.customers.on(db.customers.id == db.customers_sellers.customer),
                db.sellers.on(db.sellers.id == db.customers_sellers.seller)
            ),
                                                             orderby=db.customers.name)
        for row in rows:
            customers[row.id] = "%s" % (row.name)
        customers['TODOS'] = 'TODOS'
        rows = db(db.sellers.related_user == user_id).select(db.sellers.id,
                                                             db.sellers.name, orderby=db.sellers.name)
        for row in rows:
            sellers[row.id] = "%s" % (row.name)
            sales_code = row.id
    else:
        rows = db(db.customers.id > 0).select(db.customers.id,
                                              db.customers.name, orderby=db.customers.name)
        for row in rows:
            customers[row.id] = "%s" % (row.name)
        # customers = sorted(customers.items(), key=lambda x: customers[x])
        customers['TODOS'] = 'TODOS'
        rows = db(db.sellers.id > 0).select(db.sellers.id,
                                            db.sellers.name, orderby=db.sellers.name)
        for row in rows:
            sellers[row.id] = "%s" % (row.name)
        sellers['TODOS'] = 'TODOS'
    if len(request.vars) > 0:
        try:
            val_start = datetime.datetime.strptime(request.vars.start_time, '%d/%m/%Y')
            val_end = datetime.datetime.strptime(request.vars.end_time, '%d/%m/%Y')
        except:
            val_start = datetime.datetime.strptime(request.vars.start_time, '%Y-%m-%d')
            val_end = datetime.datetime.strptime(request.vars.end_time, '%Y-%m-%d')
        cliente_condition = request.vars.cliente
        if len(cliente_condition) < 1:
            cliente_condition = 'TODOS'
        vendedor_condition = request.vars.vendedor
        if len(vendedor_condition) < 1:
            vendedor_condition = 'TODOS'
        cuenta_condition = request.vars.cuenta
    else:
        val_start = last
        val_end = datetime.datetime.now()
        cliente_condition = 'TODOS'
        cuenta_condition = ''
    if sales_user:
        vendedor_condition = sales_code
    else:
        vendedor_condition = 'TODOS'
    val_start = val_start.date()
    val_end = val_end.date()
    form = SQLFORM.factory(
        Field('start_time', 'date', label=T('Start Date'), default=val_start),
        Field('end_time', 'date', label=T('End Date'), default=val_end),
        Field('cliente', label=T('Customer'), default=cliente_condition, requires=IS_IN_SET(customers)),
        Field('cuenta', 'string', default=cuenta_condition, label=T('Account')),
        Field('vendedor', label=T('Seller'), default=vendedor_condition, requires=IS_IN_SET(sellers)),
    )
    if form.process().accepted:
        val_start = form.vars.start_time
        val_end = form.vars.end_time
        cliente_condition = form.vars.cliente
        vendedor_condition = form.vars.vendedor
        cuenta_condition = form.vars.cuenta
    costos, consumo, minutos, llamadas, ganancia, rentabilidad, data = data_graphics(
        val_start, val_end, cliente_condition,
        vendedor_condition, cuenta_condition)
    return dict(form=form, data=data, costos=costos,
                consumo=consumo, minutos=minutos,
                llamadas=llamadas, ganancia=ganancia, rentabilidad=rentabilidad, title=title)



@auth.requires_login()
def graphics():
    user_id = auth.user.id
    # print auth.user_group(user_id)
    sales_user = auth.has_membership(role='sales')
    root_user = auth.has_membership(role='root')
    if root_user is False and sales_user is False:
        return
    # response.view = 'default.html'
    title = T('Graphics')
    year = now.year
    month = now.month - 1 or 12
    if month == 12:
        year = now.year - 1
    day = now.day
    try:
        last = datetime.datetime(year, month, day)
    except:
        last = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    customers = collections.OrderedDict()
    sellers = collections.OrderedDict()
    sales_code = False
    if sales_user:
        rows = db(db.sellers.related_user == user_id).select(db.customers.id,
                                                             db.customers.name, left=(
                db.customers.on(db.customers.id == db.customers_sellers.customer),
                db.sellers.on(db.sellers.id == db.customers_sellers.seller)
            ),
                                                             orderby=db.customers.name)
        for row in rows:
            customers[row.id] = "%s" % (row.name)
        customers['TODOS'] = 'TODOS'
        rows = db(db.sellers.related_user == user_id).select(db.sellers.id,
                                                             db.sellers.name, orderby=db.sellers.name)
        for row in rows:
            sellers[row.id] = "%s" % (row.name)
            sales_code = row.id
    else:
        rows = db(db.customers.id > 0).select(db.customers.id,
                                              db.customers.name, orderby=db.customers.name)
        for row in rows:
            customers[row.id] = "%s" % (row.name)
        # customers = sorted(customers.items(), key=lambda x: customers[x])
        customers['TODOS'] = 'TODOS'
        rows = db(db.sellers.id > 0).select(db.sellers.id,
                                            db.sellers.name, orderby=db.sellers.name)
        for row in rows:
            sellers[row.id] = "%s" % (row.name)
        sellers['TODOS'] = 'TODOS'
    if len(request.vars) > 0:
        try:
            val_start = datetime.datetime.strptime(request.vars.start_time, '%d/%m/%Y')
            val_end = datetime.datetime.strptime(request.vars.end_time, '%d/%m/%Y')
        except:
            val_start = datetime.datetime.strptime(request.vars.start_time, '%Y-%m-%d')
            val_end = datetime.datetime.strptime(request.vars.end_time, '%Y-%m-%d')
        cliente_condition = request.vars.cliente
        if len(cliente_condition) < 1:
            cliente_condition = 'TODOS'
        vendedor_condition = request.vars.vendedor
        if len(vendedor_condition) < 1:
            vendedor_condition = 'TODOS'
        cuenta_condition = request.vars.cuenta
    else:
        val_start = last
        val_end = datetime.datetime.now()
        cliente_condition = 'TODOS'
        cuenta_condition = ''
    if sales_user:
        vendedor_condition = sales_code
    else:
        vendedor_condition = 'TODOS'
    val_start = val_start.date()
    val_end = val_end.date()
    form = SQLFORM.factory(
        Field('start_time', 'date', label=T('Start Date'), default=val_start),
        Field('end_time', 'date', label=T('End Date'), default=val_end),
        Field('cliente', label=T('Customer'), default=cliente_condition, requires=IS_IN_SET(customers)),
        Field('cuenta', 'string', default=cuenta_condition, label=T('Account')),
        Field('vendedor', label=T('Seller'), default=vendedor_condition, requires=IS_IN_SET(sellers)),
    )
    if form.process().accepted:
        val_start = form.vars.start_time
        val_end = form.vars.end_time
        cliente_condition = form.vars.cliente
        vendedor_condition = form.vars.vendedor
        cuenta_condition = form.vars.cuenta
    costos, consumo, minutos, llamadas, ganancia, rentabilidad, data = data_graphics(
        val_start, val_end, cliente_condition,
        vendedor_condition, cuenta_condition)
    return dict(form=form, data=data, costos=costos,
                consumo=consumo, minutos=minutos,
                llamadas=llamadas, ganancia=ganancia, rentabilidad=rentabilidad, title=title)


# @auth.requires_membership('root')
@auth.requires_login()
def cdr_reports():
    user_id = auth.user.id
    sales_user_id = 1
    sales_user = auth.has_membership(role='sales')
    root_user = auth.has_membership(role='root')
    if root_user is False and sales_user is False:
        return
    title = T('CDR Reports')
    servers = {}
    data = []
    customers = {}
    options = {
        0: T('Completed'),
        1: T('Failed'),
    }
    rows = db(db.services_servers.id > 0).select(db.services_servers.id,
                                                 db.services_servers.name,
                                                 db.services_servers.host_ip)
    for row in rows:
        servers[row.id] = "%s-%s" % (row.name, row.host_ip)
    servers['todos'] = 'todos'
    year = now.year
    month = now.month - 1 or 12
    if month == 12:
        year = now.year - 1
    day = now.day
    try:
        last = datetime.datetime(year, month, day)
    except:
        last = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    if len(request.vars) > 0:
        if type(request.vars.start_time) is types.ListType:
            try:
                val_start = datetime.datetime.strptime(request.vars.from_date[0], '%d/%m/%Y')
                val_end = datetime.datetime.strptime(request.vars.to_date[0], '%d/%m/%Y')
            except:
                val_start = datetime.datetime.strptime(request.vars.from_date[0], '%Y-%m-%d')
                val_end = datetime.datetime.strptime(request.vars.to_date[0], '%Y-%m-%d')
        else:
            try:
                val_start = datetime.datetime.strptime(request.vars.from_date, '%d/%m/%Y')
                val_end = datetime.datetime.strptime(request.vars.to_date, '%d/%m/%Y')
            except:
                val_start = datetime.datetime.strptime(request.vars.from_date, '%Y-%m-%d')
                val_end = datetime.datetime.strptime(request.vars.to_date, '%Y-%m-%d')
    else:
        val_start = datetime.datetime.now()
        val_end = datetime.datetime.now()
    val_start = val_start.date()
    val_end = val_end.date()
    req_customer = request.vars.customer
    req_customer_name = request.vars.customer_name
    if req_customer_name is None:
        req_customer_name = '%'
    req_provider = request.vars.provider
    req_provider_name = request.vars.provider_name
    if req_provider_name is None:
        req_provider_name = '%'
    req_called_number = request.vars.called_number
    if req_called_number is None:
        req_called_number = '%'
    req_release_reason = request.vars.release_reason
    if req_release_reason is None:
        req_release_reason = '%'
    req_from_hour = request.vars.from_hour
    if req_from_hour is None:
        req_from_hour = '00:00:00'
    req_to_hour = request.vars.to_hour
    if req_to_hour is None:
        req_to_hour = '23:59:59'
    if sales_user:
        sales_user_id = db.sellers(db.sellers.related_user == user_id).id
        rows = db(db.accounts.seller == sales_user_id).select(db.accounts.id,
                                                              db.accounts.account,
                                                              orderby=db.accounts.account)
        for row in rows:
            customers[row.account] = "%s" % (row.account)
            customers['%'] = '%'
        form = SQLFORM.factory(
            Field('customer', 'boolean', default=req_customer, label=T('Customer')),
            Field('customer_name', requires=IS_IN_SET(customers), default='%', label=T('Customer')),
            Field('provider', 'boolean', default=req_provider, label=T('Provider')),
            Field('provider_name', 'string', default=req_provider_name, label=T('Provider')),
            Field('called_number', 'string', default=req_called_number, label=T('Called Number')),
            Field('release_reason', 'string', default=req_release_reason, label=T('Release Reason')),
            Field('from_date', 'date', label=T('From'), default=val_start),
            Field('from_hour', 'string', label=T('From'), default=req_from_hour),
            Field('to_date', 'date', label=T('To'), default=val_end),
            Field('to_hour', 'string', label=T('To'), default=req_to_hour),
            Field('group', label=T('Group'), default=0, requires=IS_IN_SET(options),
                  widget=SQLFORM.widgets.radio.widget),
            Field('server', label=T('Server'), default='todos', requires=IS_IN_SET(servers)),
        )
    else:
        form = SQLFORM.factory(
            Field('customer', 'boolean', default=req_customer, label=T('Customer')),
            Field('customer_name', 'string', default=req_customer_name, label=T('Customer')),
            Field('provider', 'boolean', default=req_provider, label=T('Provider')),
            Field('provider_name', 'string', default=req_provider_name, label=T('Provider')),
            Field('called_number', 'string', default=req_called_number, label=T('Called Number')),
            Field('release_reason', 'string', default=req_release_reason, label=T('Release Reason')),
            Field('from_date', 'date', label=T('From'), default=val_start),
            Field('from_hour', 'string', label=T('From'), default=req_from_hour),
            Field('to_date', 'date', label=T('To'), default=val_end),
            Field('to_hour', 'string', label=T('To'), default=req_to_hour),
            Field('group', label=T('Group'), default=0, requires=IS_IN_SET(options),
                  widget=SQLFORM.widgets.radio.widget),
            Field('server', label=T('Server'), default='todos', requires=IS_IN_SET(servers)),
        )
    group = False
    csv_path = False
    release_reason = False
    customer = False
    provider = False
    if form.process().accepted:
        customer = form.vars.customer
        customer_name = form.vars.customer_name
        provider = form.vars.provider
        provider_name = form.vars.provider_name
        called_number = form.vars.called_number
        release_reason = form.vars.release_reason
        from_date = form.vars.from_date
        to_date = form.vars.to_date
        from_time = "%s %s" % (from_date, form.vars.from_hour)
        to_time = "%s %s" % (to_date, form.vars.to_hour)
        group = form.vars.group
        server = form.vars.server
        # if customer_name not in customers:
        #     return dict(form=form, data=data, group=group, csv_path=csv_path,
        #          release_reason=release_reason, customer=customer,
        #          provider=provider, title=title)
        headers = []
        query_str = 'select '
        # if group == '0':
        #     query_str += 't.id_call id, '
        # else:
        #     query_str += 't.id_failed_call id, '
        if customer:
            query_str += 'acc.login, '
            headers.append('Login')
        if provider:
            query_str += 'case t.route_type when 0 then gateways.description when 2 then gatekeepers.description when 5 then acc2.login end proveedor, '
            headers.append('Provider')
        # query_str += 't.id_client id_client, '
        query_str += 't.caller_id caller_id, '
        headers.append('Caller ID')
        query_str += 't.called_number called_number, '
        headers.append('Called Number')
        query_str += 't.call_start call_start, '
        headers.append('Call Start')
        if group == '0':
            query_str += 't.call_end call_end, '
            query_str += 't.duration duration, '
            query_str += 'round(t.call_rate,4) call_rate, '
            query_str += 'round(t.cost * t.ratio,4) cost, '
            headers.append('Call End')
            headers.append('Duration')
            headers.append('Rate')
            headers.append('Cost')
        # else:
        #     query_str += 'now() call_end, '
        #     query_str += '0 duration, '
        #     query_str += '0 call_rate, '
        #     query_str += '0 cost, '

        if group == '1':
            query_str += 't.release_reason release_reason, '
            headers.append('Release Reason')
        query_str += 't.tariffdesc tariffdesc, '
        headers.append('Destination')
        query_str += 't.ip_number ip_number, '
        headers.append('IP Number')
        query_str += 'servers.host_ip ip_proxy '
        headers.append('Proxy')
        if group == '0':
            query_str += 'from calls t '
        else:
            query_str += 'from callsfailed t '
        query_str += """left join accounts acc on acc.id_client=t.id_client and acc.client_type=t.client_type and acc.server_id=t.server_id """
        #        query_str += 'clientsip on t.id_client = clientsip.id_client left outer join '
        #        query_str += 'left outer join currency_names as currencysip on clientsip.id_currency = currencysip.id '
        #        query_str += 'clientsshared on t.id_client = clientsshared.id_client left outer join '
        #        query_str += 'currency_names as currencyshared on clientsshared.id_currency = currencyshared.id left outer join '
        query_str += 'left outer join gatekeepers on t.id_route = gatekeepers.id_route and t.server_id=gatekeepers.server_id '
        query_str += 'left outer join gateways on t.id_route = gateways.id_route and t.server_id=gateways.server_id '
        query_str += 'left outer join accounts acc2 on t.id_route = acc2.id_client and acc2.server_id=t.server_id and acc2.client_type=32 and t.route_type = 5 '
        query_str += 'left join sige.services_servers servers on t.server_id = servers.id '
        #        query_str += 'clientsshared as routeshared on t.id_route = routeshared.id_client left outer join '
        #        query_str += 'invoiceclients on t.id_client = invoiceclients.idclient and t.client_type = invoiceclients.type '
        query_str += 'where '
        query_str += 't.call_start between "%s" and "%s" ' % (from_time, to_time)
        if customer == True:
            query_str += 'and acc.login like "%s" ' % customer_name
        if provider == True:
            query_str += 'and (gatekeepers.description like "%s" or ' % (provider_name)
            query_str += 'gateways.description like "%s" or ' % (provider_name)
            query_str += 'acc2.login like "%s") ' % (provider_name)
        if len(called_number) > 1:
            query_str += 'and t.called_number like "%s" ' % (called_number)
        if group == '1':
            query_str += 'and t.release_reason like "%s" ' % (release_reason)
        if server != 'todos':
            query_str += 'and t.server_id = "%s" ' % (server)
        if sales_user:
            query_str += 'and acc.seller = "%s " ' % (sales_user_id)
        query_str += "order by "
        if customer:
            query_str += 'acc.login, '
        if provider:
            query_str += 'proveedor, '
        query_str += "call_start"
        data = db2.executesql(query_str)
        if group == '0':
            file_name = "cdr_admin_completados-%s-%s.csv" % (from_date, to_date)
        else:
            file_name = "cdr_admin_fallados-%s-%s.csv" % (from_date, to_date)
        file_url = "%s/%s" % (UPLOAD_PATH, file_name)
        csv_path = file_name
        out = csv.writer(open(file_url, "w"), delimiter=',', quoting=csv.QUOTE_ALL)
        out.writerow(headers)
        out.writerows(data)
    return dict(form=form, data=data, group=group, csv_path=csv_path,
                release_reason=release_reason, customer=customer,
                provider=provider, title=title)


#@auth.requires_membership('root')
@auth.requires_login()
def admin_reports():
    user_id = auth.user.id
    sales_user_id = 1
    sales_user = auth.has_membership(role='sales')
    root_user = auth.has_membership(role='root')
    if root_user is False and sales_user is False:
        return
    title = T('Administrative Reports')
    options = {
        0: T('Hourly'),
        1: T('Daily'),
        2: T('Monthly')
    }
    servers = {}
    customers = {}
    rows = db(db.services_servers.id > 0).select(db.services_servers.id,
                                                 db.services_servers.name,
                                                 db.services_servers.host_ip)
    for row in rows:
        servers[row.id] = "%s-%s" % (row.name, row.host_ip)
    servers['todos'] = 'todos'
    year = now.year
    month = now.month - 1 or 12
    if month == 12:
        year = now.year - 1
    day = now.day
    try:
        last = datetime.datetime(year, month, day)
    except:
        last = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    if len(request.vars) > 0:
        if type(request.vars.start_time) is types.ListType:
            try:
                val_start = datetime.datetime.strptime(request.vars.from_date[0], '%d/%m/%Y')
                val_end = datetime.datetime.strptime(request.vars.to_date[0], '%d/%m/%Y')
            except:
                val_start = datetime.datetime.strptime(request.vars.from_date[0], '%Y-%m-%d')
                val_end = datetime.datetime.strptime(request.vars.to_date[0], '%Y-%m-%d')
        else:
            try:
                val_start = datetime.datetime.strptime(request.vars.from_date, '%d/%m/%Y')
                val_end = datetime.datetime.strptime(request.vars.to_date, '%d/%m/%Y')
            except:
                val_start = datetime.datetime.strptime(request.vars.from_date, '%Y-%m-%d')
                val_end = datetime.datetime.strptime(request.vars.to_date, '%Y-%m-%d')
        # if type(request.vars.start_time) is types.ListType:
        #     val_start = datetime.datetime.strptime(request.vars.from_date[0], '%d/%m/%Y')
        #     val_end = datetime.datetime.strptime(request.vars.to_date[0], '%d/%m/%Y')
        # else:
        #     val_start = datetime.datetime.strptime(request.vars.from_date, '%d/%m/%Y')
        #     val_end = datetime.datetime.strptime(request.vars.to_date, '%d/%m/%Y')
    else:
        val_start = datetime.datetime.now()
        val_end = datetime.datetime.now()
    val_start = val_start.date()
    val_end = val_end.date()
    req_customer = request.vars.customer
    req_customer_name = request.vars.customer_name
    if req_customer_name is None:
        req_customer_name = '%'
    req_provider = request.vars.provider
    req_provider_name = request.vars.provider_name
    if req_provider_name is None:
        req_provider_name = '%'
    req_destination = request.vars.destination
    if req_destination is None:
        req_destination = '%'
    req_destination_name = request.vars.destination_name
    if req_destination_name is None:
        req_destination_name = '%'
    req_from_hour = request.vars.from_hour
    if req_from_hour is None:
        req_from_hour = '00:00:00'
    req_to_hour = request.vars.to_hour
    if req_to_hour is None:
        req_to_hour = '23:59:59'
    if sales_user:
        sales_user_id = db.sellers(db.sellers.related_user == user_id).id
        rows = db(db.accounts.seller == sales_user_id).select(db.accounts.id,
                                                              db.accounts.account,
                                                              orderby=db.accounts.account)
        for row in rows:
            customers[row.account] = "%s" % (row.account)
        customers['%'] = '%'
        form = SQLFORM.factory(
            Field('customer', 'boolean', default=req_customer, label=T('Customer')),
            Field('customer_name', requires=IS_IN_SET(customers), default='%', label=T('Customer')),
            Field('provider', 'boolean', default=req_provider, label=T('Provider')),
            Field('provider_name', 'string', default=req_provider_name, label=T('Provider')),
            Field('destination', 'boolean', default=req_destination, label=T('Destination')),
            Field('destination_name', 'string', default=req_destination_name, label=T('Destination')),
            Field('from_date', 'date', label=T('From'), default=val_start),
            Field('from_hour', 'string', label=T('From'), default=req_from_hour),
            Field('to_date', 'date', label=T('To'), default=val_end),
            Field('to_hour', 'string', label=T('To'), default=req_to_hour),
            Field('group', label=T('Group'), requires=IS_IN_SET(options), widget=SQLFORM.widgets.radio.widget),
            Field('server', label=T('Server'), default='todos', requires=IS_IN_SET(servers)),
            Field('ip_number', 'boolean', label=T('IP')),
            Field('origin', 'boolean', label=T('Origin')),
            Field('prefix', 'boolean', label=T('Prefix')),
        )
    else:
        form = SQLFORM.factory(
            Field('customer', 'boolean', default=req_customer, label=T('Customer')),
            Field('customer_name', 'string', default=req_customer_name, label=T('Customer')),
            Field('provider', 'boolean', default=req_provider, label=T('Provider')),
            Field('provider_name', 'string', default=req_provider_name, label=T('Provider')),
            Field('destination', 'boolean', default=req_destination, label=T('Destination')),
            Field('destination_name', 'string', default=req_destination_name, label=T('Destination')),
            Field('from_date', 'date', label=T('From'), default=val_start),
            Field('from_hour', 'string', label=T('From'), default=req_from_hour),
            Field('to_date', 'date', label=T('To'), default=val_end),
            Field('to_hour', 'string', label=T('To'), default=req_to_hour),
            Field('group', label=T('Group'), requires=IS_IN_SET(options), widget=SQLFORM.widgets.radio.widget),
            Field('server', label=T('Server'), default='todos', requires=IS_IN_SET(servers)),
            Field('ip_number', 'boolean', label=T('IP')),
            Field('origin', 'boolean', label=T('Origin')),
            Field('prefix', 'boolean', label=T('Prefix')),
        )
    data = []
    ip_number = False
    customer = False
    provider = False
    destination = False
    origin = False
    prefix = False
    group = False
    csv_path = False
    if form.process().accepted:
        headers = []
        customer = form.vars.customer
        customer_name = form.vars.customer_name
        provider = form.vars.provider
        provider_name = form.vars.provider_name
        destination = form.vars.destination
        destination_name = form.vars.destination_name
        from_date = form.vars.from_date
        to_date = form.vars.to_date
        start_time = "%s %s" % (from_date, form.vars.from_hour)
        end_time = "%s %s" % (to_date, form.vars.to_hour)
        group = form.vars.group
        ip_number = form.vars.ip_number
        origin = form.vars.origin
        prefix = form.vars.prefix
        server = form.vars.server
        query_str = 'select '
        query_str += """t.fecha fecha, """
        headers.append('Fecha')
        if customer:
            query_str += """t.cliente cliente, t.invoicetype invoicetype,
            t.moneda moneda, t.igv igv, """
            headers.append('Cliente')
            headers.append('Tipo')
            headers.append('Moneda')
            headers.append('Impuesto')
        if provider:
            query_str += """t.proveedor proveedor, """
            headers.append('Proveedor')
        query_str += """sum(t.completados + t.fallados) intentos, sum(t.completados) completados,
            sum(t.fallados) fallados, round(sum(t.minutos),2) minutos, """
        headers.append('Intentos')
        headers.append('Completados')
        headers.append('Fallados')
        headers.append('Minutos')
        if ip_number:
            query_str += """t.ip_number ip_number, """
            headers.append('IP_NUMBER')
        if origin:
            query_str += """t.origen origen, """
            headers.append('Origen')
        if prefix:
            query_str += """t.prefijo prefijo, """
            headers.append('Prefijo')
        if destination:
            query_str += """t.destino destino, """
            headers.append('Destino')
        query_str += """
            round(100 * sum(completados)/sum(t.completados + t.fallados),2) asr,
            if(completados>0,round(sum(t.minutos)/sum(t.completados),2),0.0000) acd,
            round(sum(t.pdd)/sum(t.completados + t.fallados),2) pdd,
            round(sum(t.costoclientesoligv),2) costoclientesoligv,
            round(sum(t.costoclientesolsinigv),2) costoclientesolsinigv,
            round(sum(t.costoclientedoligv),2) costoclientedoligv,
            round(sum(t.costoclientedolsinigv),2) costoclientedolsinigv,
            round(sum(t.costoproveedor),2) costoproveedor,
            round(sum(t.costoclientedolsinigv - t.costoproveedor),2) ganancia,
            if(t.costoproveedor>0,round(sum(t.costoclientedolsinigv - t.costoproveedor)/sum(t.costoproveedor)*100,2),0.00) rentabilidad """
        headers.append('ASR')
        headers.append('ACD')
        headers.append('PDD')
        headers.append('CS_IGV')
        headers.append('CS_SIGV')
        headers.append('CD_IGV')
        headers.append('CD_SIGV')
        headers.append('Costo')
        headers.append('Ganancia')
        headers.append('Rentabilidad')
        query_str += 'from '
        query_str += '(select '
        if group == '0':
            query_str += 'date_format(callsok.call_start, "%Y-%m-%d %H") fecha, '
        elif group == '1':
            query_str += 'date(callsok.call_start) fecha, '
        else:
            query_str += 'date_format(callsok.call_start, "%Y-%m") fecha, '
        if ip_number:
            query_str += 'callsok.ip_number ip_number, '
        else:
            query_str += '"*" ip_number, '
        if customer:
            query_str += 'acc.login cliente, '
            query_str += 'case acc.invoice_type when 0 then "Postpago" when 1 then "Prepago" end invoicetype, '
            query_str += 'case acc.id_currency when 1 then "$" else "S/." end moneda, '
            query_str += 'ifnull(acc.tax_id,0) igv, '
        else:
            query_str += '"*" cliente, '
            query_str += '"*" invoicetype, '
            query_str += '"*" moneda, '
            query_str += '"*" igv, '
        if provider:
            query_str += 'case callsok.route_type when 0 then gateways.description when 2 then gatekeepers.description when 5 then acc2.login end proveedor, '
        else:
            query_str += '"*" proveedor, '
        if destination:
            query_str += 'callsok.tariffdesc destino, '
        else:
            query_str += '"*" destino, '
        query_str += 'count(*) completados, '
        query_str += '0 fallados, '
        query_str += 'sum(duration/60) minutos, '
        if origin:
            query_str += 'callsok.caller_id origen, '
        else:
            query_str += '"*" origen, '
        if prefix:
            query_str += 'callsok.tariff_prefix prefijo, '
        else:
            query_str += '"*" prefijo, '
        query_str += 'sum(if(ratio=1, 0, callsok.cost * callsok.ratio)) costoclientesoligv, '
        query_str += 'sum(if(ratio=1, 0, callsok.cost * callsok.ratio/(1+(ifnull(acc.tax_id,0))/100))) costoclientesolsinigv, '
        query_str += 'sum(callsok.cost) costoclientedoligv, '
        query_str += 'sum(callsok.cost/(1+(ifnull(acc.tax_id,0))/100)) costoclientedolsinigv, '
        query_str += 'sum(callsok.costD) costoproveedor, '
        query_str += 'sum(callsok.pdd) pdd '
        query_str += 'from calls callsok '
        query_str += """left join accounts acc on
                acc.id_client=callsok.id_client and acc.client_type=callsok.client_type
                and acc.server_id=callsok.server_id """
        query_str += 'left outer join gatekeepers on callsok.id_route = gatekeepers.id_route and callsok.server_id=gatekeepers.server_id '
        query_str += 'left outer join gateways on callsok.id_route = gateways.id_route and callsok.server_id=gateways.server_id '
        query_str += 'left outer join accounts acc2 on callsok.id_route = acc2.id_client and acc2.server_id=callsok.server_id and acc2.client_type=32 and callsok.route_type = 5 '
        query_str += 'where '
        query_str += 'callsok.call_start between "%s" and "%s"  and ' % (start_time, end_time)
        query_str += 'callsok.tariffdesc like "%s" and ' % (destination_name)
        if sales_user:
            query_str += 'acc.login like "%s" and acc.seller = "%s" and ' % (customer_name, sales_user_id)
        else:
            query_str += 'acc.login like "%s" and ' % (customer_name)
            #query_str += 'and acc.seller = "%s " ' % (sales_user_id)
        query_str += '(gatekeepers.description like "%s" or gateways.description like "%s" or acc2.login like "%s") ' % (
            provider_name, provider_name, provider_name)
        if server != 'todos':
            query_str += 'and callsok.server_id = "%s" ' % server
        query_str += 'group by '
        query_str += 'fecha, cliente, invoicetype, moneda, igv, proveedor, destino, ip_number, origen, prefijo '
        query_str += 'union '
        query_str += 'select '
        if group == '0':
            query_str += 'date_format(callsfailed.call_start, "%Y-%m-%d %H") fecha, '
        elif group == '1':
            query_str += 'date(callsfailed.call_start) fecha, '
        else:
            query_str += 'date_format(callsfailed.call_start, "%Y-%m") fecha, '
        if ip_number:
            query_str += 'callsfailed.ip_number ip_number, '
        else:
            query_str += '"*" ip_number, '
        if customer:
            query_str += 'acc.login cliente, '
            query_str += 'case acc.invoice_type when 0 then "Postpago" when 1 then "Prepago" end invoicetype, '
            query_str += 'case acc.id_currency when 1 then "$" else "S/." end moneda, '
            query_str += 'ifnull(acc.tax_id,0) igv, '
        else:
            query_str += '"*" cliente, '
            query_str += '"*" invoicetype, '
            query_str += '"*" moneda, '
            query_str += '"*" igv, '
        if provider:
            query_str += 'case callsfailed.route_type when 0 then ifnull(gateways.description,"NO ROUTE") when 2 then ifnull(gatekeepers.description, "NO ROUTE") when 5 then ifnull(acc2.login, "NO ROUTE") else  "NO ROUTE" end proveedor, '
        else:
            query_str += '"*" proveedor, '
        if destination:
            query_str += 'if(callsfailed.tariffdesc is not NULL, callsfailed.tariffdesc, "NO DESTINATION") destino, '
        else:
            query_str += '"*" destino, '
        query_str += '0 completados, '
        query_str += 'count(*) fallados, '
        query_str += '0 minutos, '
        if origin:
            query_str += 'callsfailed.caller_id origen, '
        else:
            query_str += '"*" origen, '
        if prefix:
            query_str += 'ifnull(callsfailed.tariff_prefix, "NO PREFIX") prefijo, '
        else:
            query_str += '"*" prefijo, '
        query_str += '0 costoclientesoligv, '
        query_str += '0 costoclientesolsinigv, '
        query_str += '0 costoclientedoligv, '
        query_str += '0 costoclientedolsinigv, '
        query_str += '0 costoproveedor, '
        query_str += '0 pdd '
        query_str += 'from callsfailed '
        query_str += """left join accounts acc on
                acc.id_client=callsfailed.id_client and acc.client_type=callsfailed.client_type
                and acc.server_id=callsfailed.server_id """
        query_str += 'left outer join gatekeepers on callsfailed.id_route = gatekeepers.id_route and callsfailed.server_id=gatekeepers.server_id '
        query_str += 'left outer join gateways on callsfailed.id_route = gateways.id_route and callsfailed.server_id=gateways.server_id '
        query_str += 'left outer join accounts acc2 on callsfailed.id_route = acc2.id_client and acc2.server_id=callsfailed.server_id and acc2.client_type=32 and callsfailed.route_type = 5 '
        query_str += 'where '
        query_str += 'callsfailed.call_start between "%s" and "%s"  and ' % (start_time, end_time)
        if sales_user:
            query_str += 'acc.login like "%s" and acc.seller = "%s" and ' % (customer_name, sales_user_id)
        else:
            query_str += 'acc.login like "%s" and ' % (customer_name)
        query_str += '(gatekeepers.description like "%s" or gateways.description like "%s" or acc2.login like "%s" or callsfailed.tariffdesc like "%s") ' % (
            provider_name, provider_name, provider_name, destination_name)
        if server != 'todos':
            query_str += 'and callsfailed.server_id = "%s" ' % server
        query_str += 'group by '
        query_str += 'fecha, cliente, invoicetype, moneda, igv, proveedor, destino, ip_number, origen, prefijo '
        query_str += ') as t '
        if provider or destination:
            query_str += 'where '
        if provider:
            query_str += 'proveedor like "%s" ' % provider_name
        if destination:
            if provider:
                query_str += 'and '
            query_str += 'destino like "%s" ' % destination_name
        query_str += 'group by '
        query_str += 'fecha, cliente, t.invoicetype, moneda, igv, proveedor, destino, ip_number, origen, prefijo '
        query_str += 'order by fecha, cliente, invoicetype, moneda, igv, proveedor, destino, ip_number, origen, prefijo '
        data = db2.executesql(query_str)
        total_calls = decimal.Decimal(0)
        total_completed = decimal.Decimal(0)
        total_failed = decimal.Decimal(0)
        total_minutes = decimal.Decimal(0)
        total_cs_igv = decimal.Decimal(0)
        total_css_igv = decimal.Decimal(0)
        total_cd_igv = decimal.Decimal(0)
        total_cds_igv = decimal.Decimal(0)
        total_costo = decimal.Decimal(0)
        total_asr = decimal.Decimal(0)
        total_acd = decimal.Decimal(0)
        total_pdd = decimal.Decimal(0)
        total_ganancia = decimal.Decimal(0)
        total_rentabilidad = decimal.Decimal(0)
        last_row = []
        for line in data:
            if customer:
                if provider:
                    total_calls += decimal.Decimal(line[6])
                    total_completed += decimal.Decimal(line[7])
                    total_failed += decimal.Decimal(line[8])
                    total_minutes += decimal.Decimal(line[9])
                else:
                    total_calls += decimal.Decimal(line[5])
                    total_completed += decimal.Decimal(line[6])
                    total_failed += decimal.Decimal(line[7])
                    total_minutes += decimal.Decimal(line[8])
            else:
                if provider:
                    total_calls += decimal.Decimal(line[2])
                    total_completed += decimal.Decimal(line[3])
                    total_failed += decimal.Decimal(line[4])
                    total_minutes += decimal.Decimal(line[5])
                else:
                    total_calls += decimal.Decimal(line[1])
                    total_completed += decimal.Decimal(line[2])
                    total_failed += decimal.Decimal(line[3])
                    total_minutes += decimal.Decimal(line[4])
            total_cs_igv += decimal.Decimal(line[-7])
            total_css_igv += decimal.Decimal(line[-6])
            total_cd_igv += decimal.Decimal(line[-5])
            total_cds_igv += decimal.Decimal(line[-4])
            total_costo += decimal.Decimal(line[-3])
        try:
            total_asr = round(decimal.Decimal(100) * total_completed / (total_completed + total_failed), 2)
        except:
            total_asr = 0
        try:
            total_acd = round(total_minutes / total_completed, 2)
        except:
            total_acd = 0
        total_pdd = 0
        total_ganancia = round(total_cds_igv - total_costo, 2)
        try:
            total_rentabilidad = round((total_cds_igv - total_costo) / total_costo * decimal.Decimal(100), 2)
        except:
            total_rentabilidad = 0
        last_row.append('')
        if customer:
            last_row.append('')
            last_row.append('')
            last_row.append('')
            last_row.append('')
        if provider:
            last_row.append('')
        last_row.append(total_calls)
        last_row.append(total_completed)
        last_row.append(total_failed)
        last_row.append(total_minutes)
        if ip_number:
            last_row.append('')
        if origin:
            last_row.append('')
        if prefix:
            last_row.append('')
        if destination:
            last_row.append('')
        last_row.append(total_asr)
        last_row.append(total_acd)
        last_row.append(total_pdd)
        last_row.append(total_cs_igv)
        last_row.append(total_css_igv)
        last_row.append(total_cd_igv)
        last_row.append(total_cds_igv)
        last_row.append(total_costo)
        last_row.append(total_ganancia)
        last_row.append(total_rentabilidad)
        new_data = list(data)
        new_data.append(last_row)
        file_name = "cdr_report_admin-%s-%s.csv" % (from_date, to_date)
        file_url = "%s/%s" % (UPLOAD_PATH, file_name)
        csv_path = "%s" % file_name
        out = csv.writer(open(file_url, "w"), delimiter=',', quoting=csv.QUOTE_ALL)
        out.writerow(headers)
        out.writerows(new_data)
    return dict(form=form, data=data, ip_number=ip_number,
                customer=customer, provider=provider,
                destination=destination, origin=origin,
                prefix=prefix, group=group, csv_path=csv_path, title=title)


@auth.requires_membership('root')
def cdr_aux_reports():
    title = T('CDR Reports')
    servers = {}
    data = []
    options = {
        0: T('Completed'),
        1: T('Failed'),
    }
    rows = db(db.services_servers.id > 0).select(db.services_servers.id,
                                                 db.services_servers.name,
                                                 db.services_servers.host_ip)
    for row in rows:
        servers[row.id] = "%s-%s" % (row.name, row.host_ip)
    servers['todos'] = 'todos'
    year = now.year
    month = now.month - 1 or 12
    if month == 12:
        year = now.year - 1
    day = now.day
    try:
        last = datetime.datetime(year, month, day)
    except:
        last = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    if len(request.vars) > 0:
        if type(request.vars.start_time) is types.ListType:
            val_start = datetime.datetime.strptime(request.vars.from_date[0], '%d/%m/%Y')
            val_end = datetime.datetime.strptime(request.vars.to_date[0], '%d/%m/%Y')
        else:
            val_start = datetime.datetime.strptime(request.vars.from_date, '%d/%m/%Y')
            val_end = datetime.datetime.strptime(request.vars.to_date, '%d/%m/%Y')
    else:
        val_start = datetime.datetime.now()
        val_end = datetime.datetime.now()
    val_start = val_start.date()
    val_end = val_end.date()
    req_customer = request.vars.customer
    req_customer_name = request.vars.customer_name
    if req_customer_name is None:
        req_customer_name = '%'
    req_provider = request.vars.provider
    req_provider_name = request.vars.provider_name
    if req_provider_name is None:
        req_provider_name = '%'
    req_called_number = request.vars.called_number
    if req_called_number is None:
        req_called_number = '%'
    req_release_reason = request.vars.release_reason
    if req_release_reason is None:
        req_release_reason = '%'
    req_from_hour = request.vars.from_hour
    if req_from_hour is None:
        req_from_hour = '00:00:00'
    req_to_hour = request.vars.to_hour
    if req_to_hour is None:
        req_to_hour = '23:59:59'
    form = SQLFORM.factory(
        Field('customer', 'boolean', default=req_customer, label=T('Customer')),
        Field('customer_name', 'string', default=req_customer_name, label=T('Customer')),
        Field('provider', 'boolean', default=req_provider, label=T('Provider')),
        Field('provider_name', 'string', default=req_provider_name, label=T('Provider')),
        Field('called_number', 'string', default=req_called_number, label=T('Called Number')),
        Field('release_reason', 'string', default=req_release_reason, label=T('Release Reason')),
        Field('from_date', 'date', label=T('From'), default=val_start),
        Field('from_hour', 'string', label=T('From'), default=req_from_hour),
        Field('to_date', 'date', label=T('To'), default=val_end),
        Field('to_hour', 'string', label=T('To'), default=req_to_hour),
        Field('group', label=T('Group'), default=0, requires=IS_IN_SET(options), widget=SQLFORM.widgets.radio.widget),
        Field('server', label=T('Server'), default='todos', requires=IS_IN_SET(servers)),
    )
    group = False
    csv_path = False
    release_reason = False
    customer = False
    provider = False
    if form.process().accepted:
        customer = form.vars.customer
        customer_name = form.vars.customer_name
        provider = form.vars.provider
        provider_name = form.vars.provider_name
        called_number = form.vars.called_number
        release_reason = form.vars.release_reason
        from_date = form.vars.from_date
        to_date = form.vars.to_date
        from_time = datetime.datetime.strptime("%s %s" % (from_date, form.vars.from_hour),
                                               '%Y-%m-%d %H:%M:%S').isoformat()
        to_time = datetime.datetime.strptime("%s %s" % (to_date, form.vars.to_hour), '%Y-%m-%d %H:%M:%S').isoformat()
        group = form.vars.group
        server = form.vars.server
        print 'aaa', from_time
        print 'bbbb', to_time
        URL = 'http://209.126.121.94:8983/solr/calls/select?q=*&fq=call_start:[{}Z+TO+{}Z]&sort=call_start%20asc&wt=json&rows=1000000'.format(
            from_time, to_time)
        print URL
        data = requests.get(URL)
        elem = data.json()
        print elem['response']
    return dict(form=form)
