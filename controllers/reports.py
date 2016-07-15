# -*- coding: utf-8 -*-#
import csv
import uuid
import decimal
import collections

### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

# def service_control():
#     customers = collections.OrderedDict()
#     rows = db(db.customers.id>0).select(db.customers.id,
#         db.customers.name, orderby=db.customers.name)
#     for row in rows:
#         customers[row.id] = "%s" % (row.name)
#     customers['TODOS'] = 'TODOS'
#     order_options = {
#         0: T('Customer'),
#         1: T('Service'),
#         2: T('Due Days'),
#     }
#     additional_types = account_types
#     additional_types['TODOS'] = 'TODOS'
#     if len(request.vars) > 0:
#         default_type = request.vars.account_type
#         default_customer = request.vars.customer
#         default_order = request.vars.order_by
#     else:
#         default_type = 'TODOS'
#         default_customer = 'TODOS'
#         default_order = 2
#     form = SQLFORM.factory(
#         Field('customer', label=T('Customer'), default=default_customer,requires=IS_IN_SET(customers)),
#         Field('account_type', label=T('Type'), default=default_type, requires=IS_IN_SET(additional_types)),
#         Field('order_by', label=T('Order Type'), default=default_order, requires=IS_IN_SET(order_options)),
#         Field('test', 'boolean', label=T('Test')),
#     )
#     data = []
#     if form.process().accepted:
#         customer = form.vars.customer
#         account_type = form.vars.account_type
#         order_by = form.vars.order_by
#         test = form.vars.test
#         query_str = """
#         select serv.id,cust.name customer_name, serv.service,
#         if(length(serv.account)>0, serv.account,serv.did) account,inv.end_time last_date_invoice,
#         date_add(inv.end_time, interval 1 day) start_date,
#         if(per.days>0,date_add(inv.end_time, interval per.days day), last_day(date_add(inv.end_time, interval per.months month))) end_date,
#         datediff(if(per.days>0,date_add(inv.end_time, interval per.days day),last_day(date_add(inv.end_time, interval per.months month))),curdate()) difference_days,
#         cust.id, cust.account_type
#         from sige.customers cust
#         left join sige.customers_services serv on serv.customer=cust.id
#         left join sige.billing_periods per on per.id=serv.billing_period
#         left join sige.invoices_details inv on inv.customer_service=serv.id
#         where serv.id > 0
#         """
#         if customer != 'TODOS':
#             query_str += "and cust.id='%s' " % customer
#         if account_type != 'TODOS':
#             query_str += "and cust.account_type='%s' " % account_type
#         if test is True:
#             query_str += "and cust.test='T' "
#         else:
#             query_str += "and (cust.test is NULL or cust.test='F')"
#         if order_by == '0':
#             query_str += "order by cust.name asc"
#         elif order_by == '1':
#             query_str += "order by serv.service asc, cust.name"
#         else:
#             query_str += "order by difference_days desc, cust.name"
#         query = query_str
#         data = db2.executesql(query)
#     return dict(form=form, data=data)

#@auth.requires_membership('root')
def voip_reports():
    try:
        customer_service = request.vars.customer_service
        information = data_voip(customer_service)
    except:
        redirect(URL('default','index'))
    login = information[1]
    options = {
        0: T('Hourly'),
        1: T('Daily'),
        2: T('Monthly')
    }
    form = SQLFORM.factory(
        Field('from_date', 'date', label=T('From'), default=now.date()),
        Field('from_hour', 'string', label=T('From'), default='00:00:00'),
        Field('to_date', 'date', label=T('To'), default=now.date()),
        Field('to_hour', 'string', label=T('To'), default='23:59:59'),
        Field('group', label=T('Group'), requires=IS_IN_SET(options), widget=SQLFORM.widgets.radio.widget),
        Field('ip_number', 'boolean', label=T('IP')),
        Field('origin', 'boolean', label=T('Origin')),
        Field('destination', 'boolean', label=T('Destination')),
    )
    data = []
    ip_number = False
    origin = False
    destination = False
    csv_path = ''
    if form.process().accepted:
        login = login
        from_date = form.vars.from_date
        to_date = form.vars.to_date
        start_time = "%s %s" % (from_date, form.vars.from_hour)
        end_time = "%s %s" % (to_date, form.vars.to_hour)
        group = form.vars.group
        ip_number = form.vars.ip_number
        origin = form.vars.origin
        destination = form.vars.destination
        query_str = 'select '
        query_str += 't.id_client id_client, '
        query_str += 't.fecha fecha, '
        query_str += 't.ip_number ip_number, '
        query_str += 't.origen origen, '
        query_str += 't.destino destino, '
        query_str += 'sum(t.completados + t.fallados) intentos, '
        query_str += 'sum(t.completados) completados, '
        query_str += 'sum(t.fallados) fallados, '
        query_str += 'sum(t.minutos) minutos, '
        query_str += '100 * sum(t.completados)/sum(t.completados + t.fallados) asr, '
        query_str += 'sum(t.minutos)/sum(t.completados) acd, '
        query_str += 'sum(t.costo) costo '
        #headers = ['id_client, fecha, ip_number, origen, destino, intentos, completados, fallados, minutos, asr, acd, costo']
        headers = []
        headers.append('id_client')
        headers.append('fecha')
        query_str += 'from '
        query_str += '(select acc.login id_client, '
        if group == '0':
            query_str +=  'date_format(callsok.call_start, "%%Y-%%m-%%d %%H") fecha, '
        elif group == '1':
            query_str += 'date(callsok.call_start) fecha, '
        else:
            query_str += 'date_format(callsok.call_start, "%%Y-%%m") fecha, '
        if ip_number is True:
            query_str += 'callsok.ip_number ip_number, '
            headers.append('ip_number')
        else:
            query_str += '"*" ip_number, '
        if origin is True:
            query_str += 'callsok.caller_id origen, '
            headers.append('origen')
        else:
            query_str += '"*" origen, '
        if destination is True:
            query_str += 'callsok.tariffdesc destino, '
            headers.append('destino')
        else:
            query_str += '"*" destino, '
        query_str += """count(callsok.id_call) completados, 0 fallados, sum(callsok.duration)/60 minutos,
                sum(callsok.cost * callsok.ratio) costo  from calls callsok
                left join accounts acc on acc.id_client=callsok.id_client and acc.client_type=callsok.client_type and acc.server_id=callsok.server_id
                where callsok.call_start between '%s' and '%s'  and acc.login='%s' """
        query_str += 'group by id_client, fecha, ip_number, origen, destino '
        query_str += 'union '
        query_str += 'select acc.login id_client, '
        if group == '0':
            query_str +=  'date_format(callsfailed.call_start, "%%Y-%%m-%%d %%H") fecha, '
        elif group == '1':
            query_str += 'date(callsfailed.call_start) fecha, '
        else:
            query_str += 'date_format(callsfailed.call_start, "%%Y-%%m") fecha, '
        if ip_number is True:
            query_str += 'callsfailed.ip_number ip_number, '
        else:
            query_str += '"*" ip_number, '
        if origin is True:
            query_str += 'callsfailed.caller_id origen, '
        else:
            query_str += '"*" origen, '
        if destination is True:
            query_str += 'callsfailed.tariffdesc destino, '
        else:
            query_str += '"*" destino, '
        #headers = ['id_client, fecha, ip_number, origen, destino, intentos, completados, fallados, minutos, asr, acd, costo']
        headers.append('intentos')
        headers.append('completados')
        headers.append('fallados')
        headers.append('minutos')
        headers.append('asr')
        headers.append('acd')
        headers.append('costo')
        query_str += """0 completados, count(callsfailed.id_failed_call) fallados, 0 minutos,
                0 costo  from callsfailed callsfailed left join accounts acc on
                acc.id_client=callsfailed.id_client and acc.client_type=callsfailed.client_type
                and acc.server_id=callsfailed.server_id where callsfailed.call_start between '%s' and '%s'  and acc.login='%s' """
        query_str += 'group by id_client, fecha, ip_number, origen, destino '
        query_str += ') as t '
        query_str += 'group by id_client, fecha, ip_number, origen, destino '
        query_str += 'order by fecha, ip_number, origen, destino'
        query = query_str % (start_time, end_time, login, start_time, end_time, login)
        data = db2.executesql(query)
        new_data = []
        total = 0
        total_completed = 0
        total_failed = 0
        total_minutes = 0
        total_cost = 0
        total_asr = 0
        total_acd = 0
        for line in data:
            tmp = []
            tmp.append(line[0])
            tmp.append(line[1])
            if ip_number is True:
                tmp.append(line[2])
            if origin is True:
                tmp.append(line[3])
            if destination is True:
                tmp.append(line[4])
            tmp.append(line[5])
            try:
                total += int(line[5])
            except:
                total += 0
            tmp.append(line[6])
            try:
                total_completed += int(line[6])
            except:
                total_completed += 0
            tmp.append(line[7])
            try:
                total_failed += int(line[7])
            except:
                total_failed += 0
            tmp.append(line[8])
            try:
                total_minutes += round(line[8],2)
            except:
                total_minutes += 0
            tmp.append(line[9])
            tmp.append(line[10])
            tmp.append(line[11])
            try:
                total_cost += round(line[11],2)
            except:
                total_cost += 0
            new_data.append(tmp)
        try:
            total_asr=round(100*total_completed/(total_completed+total_failed),2)
        except:
            total_asr=0
        pass
        try:
            total_acd=round(total_minutes/total_completed,2)
        except:
            total_acd=0
        pass
        new_data.append(['','',total,total_completed,total_failed,total_minutes,total_asr,total_acd,total_cost])
        file_name = "report-%s-%s.csv" % (from_date, to_date)
        file_url = "%s/%s" % (UPLOAD_PATH, file_name)
        csv_path = "%s" % file_name
        out = csv.writer(open(file_url,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
        out.writerow(headers)
        out.writerows(new_data)
        #redirect(URL('data_reports', vars=data))
        #data_reports(from_date, to_date)
    return dict(form=form, data=data, ip_number=ip_number, origin=origin, destination=destination, csv_path=csv_path)


@auth.requires_membership('root')
def data_reports():
    """
    select t.id_client id_client, t.fecha fecha, t.ip_number ip_number, t.origen origen,
    t.destino destino, sum(t.completados + t.fallados) intentos, sum(t.completados) completados,
    sum(t.fallados) fallados, sum(t.minutos) minutos, 100 * sum(t.completados)/sum(t.completados + t.fallados) asr,
    sum(t.minutos)/sum(t.completados) acd, sum(t.costo) costo from
    (select acc.login id_client, date_format(callsok.call_start, "%Y-%m-%d %H") fecha, callsok.ip_number ip_number,
    "*" origen, "*" destino, count(callsok.id_call) completados, 0 fallados, sum(callsok.duration)/60 minutos,
    sum(callsok.cost * callsok.ratio) costo  from calls callsok left join accounts acc on
    acc.id_client=callsok.id_client and acc.client_type=callsok.client_type
    and acc.server_id=callsok.server_id where callsok.call_start between '2014-05-01 00:00:00' and '2014-06-05 23:59:00'
    and acc.login='jtorres' group by id_client, fecha, callsok.ip_number, origen, destino union
    select acc.login id_client, date_format(callsfailed.call_start, "%Y-%m-%d %H") fecha, callsfailed.ip_number ip_number,
    "*" origen, "*" destino, 0 completados, count(callsfailed.id_failed_call) fallados, 0 minutos,
    0 costo  from callsfailed callsfailed left join accounts acc on
    acc.id_client=callsfailed.id_client and acc.client_type=callsfailed.client_type
    and acc.server_id=callsfailed.server_id where callsfailed.call_start between '2014-05-01 00:00:00' and '2014-06-05 23:59:00'
    and acc.login='jtorres' group by id_client, fecha, callsfailed.ip_number, origen, destino ) as t
    group by id_client, fecha, ip_number, origen, destino order by fecha, ip_number, origen, destino
    """
    start_time = request.vars.from_time
    end_time = request.vars.to_time
    group = request.vars.group
    ip_number = request.vars.ip_number
    origin = request.vars.origin
    destination = request.vars.destination
    login = request.vars.login
    query_str = 'select '
    query_str += 't.id_client id_client, '
    query_str += 't.fecha fecha, '
    query_str += 't.ip_number ip_number, '
    query_str += 't.origen origen, '
    query_str += 't.destino destino, '
    query_str += 'sum(t.completados + t.fallados) intentos, '
    query_str += 'sum(t.completados) completados, '
    query_str += 'sum(t.fallados) fallados, '
    query_str += 'sum(t.minutos) minutos, '
    query_str += '100 * sum(t.completados)/sum(t.completados + t.fallados) asr, '
    query_str += 'sum(t.minutos)/sum(t.completados) acd, '
    query_str += 'sum(t.costo) costo '
    query_str += 'from '
    query_str += '(select acc.login id_client, '
    if group == '0':
        query_str +=  'date_format(callsok.call_start, "%%Y-%%m-%%d %%H") fecha, '
    elif group == '1':
        query_str += 'date(callsok.call_start) fecha, '
    else:
        query_str += 'date_format(callsok.call_start, "%%Y-%%m") fecha, '
    if ip_number == 'True':
        query_str += 'callsok.ip_number ip_number, '
    else:
        query_str += '"*" ip_number, '
    if origin == 'True':
        query_str += 'callsok.caller_id origen, '
    else:
        query_str += '"*" origen, '
    if destination == 'True':
        query_str += 'callsok.tariffdesc destino, '
    else:
        query_str += '"*" destino, '
    query_str += """count(callsok.id_call) completados, 0 fallados, sum(callsok.duration)/60 minutos,
            sum(callsok.cost * callsok.ratio) costo  from calls callsok
            left join accounts acc on acc.id_client=callsok.id_client and acc.client_type=callsok.client_type and acc.server_id=callsok.server_id
            where callsok.call_start between '%s' and '%s'  and acc.login='%s' """
    query_str += 'group by id_client, fecha, ip_number, origen, destino '
    query_str += 'union '
    query_str += 'select acc.login id_client, '
    if group == '0':
        query_str +=  'date_format(callsfailed.call_start, "%%Y-%%m-%%d %%H") fecha, '
    elif group == '1':
        query_str += 'date(callsfailed.call_start) fecha, '
    else:
        query_str += 'date_format(callsfailed.call_start, "%%Y-%%m") fecha, '
    if ip_number == 'True':
        query_str += 'callsfailed.ip_number ip_number, '
    else:
        query_str += '"*" ip_number, '
    if origin == 'True':
        query_str += 'callsfailed.caller_id origen, '
    else:
        query_str += '"*" origen, '
    if destination == 'True':
        query_str += 'callsfailed.tariffdesc destino, '
    else:
        query_str += '"*" destino, '
    query_str += """0 completados, count(callsfailed.id_failed_call) fallados, 0 minutos,
            0 costo  from callsfailed callsfailed left join accounts acc on
            acc.id_client=callsfailed.id_client and acc.client_type=callsfailed.client_type
            and acc.server_id=callsfailed.server_id where callsfailed.call_start between '%s' and '%s'  and acc.login='%s' """
    query_str += 'group by id_client, fecha, ip_number, origen, destino '
    query_str += ') as t '
    query_str += 'group by id_client, fecha, ip_number, origen, destino '
    query_str += 'order by fecha, ip_number, origen, destino'
    query = query_str % (start_time, end_time, login, start_time, end_time, login)
    data = db2.executesql(query)
    return dict(data=data, ip_number=ip_number, origin=origin, destination=destination)

def represent_data(value):
    return calling_status


def get_csv():
    file_name = request.vars.file_name
    return dict(file_name=file_name)