# -*- coding: utf-8 -*-
# __author__ = 'alfonsodg'

from isoweek import Week
import calendar
from gluon.contrib.pyfpdf import FPDF, HTMLMixin


def data_voip(customer_service):
    login = db.customers_services(db.customers_services.id == customer_service).account
    try:
        server = db.services_configurations(
            db.services_configurations.customer_service == customer_service).service_server
    except:
        return [None] * 8
    # server_id = db.services_servers(db.services_servers.id==server).alternate_name
    # sip_proxy = db.services_servers(db.services_servers.id==server).host_ip
    query = """select * from accounts where login='%s' and server_id='%s'""" % (
        login, server)
    data = db2.executesql(query)
    account_definition = []
    for row in data:
        account_definition = []
        for col in row:
            account_definition.append(col)
            #    account_definition[customer_service] = tmp
            # +-----------+-----------------+-----------+-------------+-----------+---------------+-------+------+-------------+
            # | server_id | login           | id_client | id_currency | id_tariff | account_state | TaxId | Type | InvoiceType |
            # +-----------+-----------------+-----------+-------------+-----------+---------------+-------+------+-------------+
            # |         1 | bayental_ripley |         6 |           2 |        96 |     7019.7884 | 18    |    0 |           0 |
            # |         2 | bayental_ripley |        38 |           2 |       140 |        0.0000 | 18    |    0 |           0 |
            # +-----------+-----------------+-----------+-------------+-----------+---------------+-------+------+-------------+
    return account_definition


def get_dates(mode=0):
    base = datetime.datetime.today()
    date_year = base.date().year
    date_month = base.date().month
    date_day = base.date().day
    numdays = 7
    date_list = []
    if mode == 0:
        date_list = [((base - datetime.timedelta(days=x)).date(),
                      (base - datetime.timedelta(days=x)).date()
                      ) for x in range(0, numdays)]
    elif mode == 1:
        for iter in range(1, 5):
            week_number = (base.isocalendar()[1] - iter)
            week = Week(date_year, week_number)
            date_list.append((week.monday(), week.sunday()))
    elif mode == 2:
        prev_year = False
        if date_day > 15:
            date_list.append((datetime.date(date_year, date_month, 1), datetime.date(date_year, date_month, 15)))
        prev_month = date_month - 1
        if prev_month <= 0:
            prev_month = 12
            date_year = date_year - 1
            prev_year = True
        last_day = calendar.monthrange(date_year, prev_month)[1]
        date_list.append((datetime.date(date_year, prev_month, 16), datetime.date(date_year, prev_month, last_day)))
        date_list.append((datetime.date(date_year, prev_month, 1), datetime.date(date_year, prev_month, 15)))
        prev_month = date_month - 2
        if prev_year:
            prev_month = 11
            # date_year = date_year - 1
        last_day = calendar.monthrange(date_year, prev_month)[1]
        date_list.append((datetime.date(date_year, prev_month, 16), datetime.date(date_year, prev_month, last_day)))
        date_list.append((datetime.date(date_year, prev_month, 1), datetime.date(date_year, prev_month, 15)))
    elif mode == 3:
        prev_year = False
        neo_month = date_month
        last_day = calendar.monthrange(date_year, neo_month)[1]
        mes_1 = (datetime.date(date_year, neo_month, 1), datetime.date(date_year, neo_month, last_day))
        date_list.append(mes_1)
        neo_month = date_month - 1
        if neo_month == 0:
            neo_month = 12
            date_year = date_year - 1
            prev_year = True
        last_day = calendar.monthrange(date_year, neo_month)[1]
        mes_2 = (datetime.date(date_year, neo_month, 1), datetime.date(date_year, neo_month, last_day))
        date_list.append(mes_2)
        neo_month = date_month - 2
        if prev_year:
            neo_month = 11
        last_day = calendar.monthrange(date_year, neo_month)[1]
        mes_3 = (datetime.date(date_year, neo_month, 1), datetime.date(date_year, neo_month, last_day))
        date_list.append(mes_3)
    return date_list


def csv_export(records, column_names, fields, mode='dal'):
    """Export DAL result set, list of dicts or list of lists to CSV stream for returning to user
    Arguments:
    records = the data to be returned
    column_names (list)= the column names/headings for the first row in the CSV file
                    Example ['First Name', 'Last Name', 'Email']
    fields (list) = the names of the fields (as they appear in records) in the order they
                    should be in the CSV. Example ['f_name', 'l_name', 'email']
                    or ['table_a.f_name', 'table_a.l_name', 'table_b.email']
                    If mode = 'list' and your records are in the correct order then fields may be None
                    otherwise use [1,3,0] if you list is in a different order
    mode (string) = what type of data is in records? 'dal' (Default), 'dict' or 'list'
                    'dal' if records came from a regular dal query (Default)
                    'dict' if records are a list of dicts (for example using db.executesql() with as_dict = True)
                    'list' if records are a list of lists/tuples (for example using db.executesql() with as_dict = False)

    """

    # create fake file object
    import cStringIO
    file = cStringIO.StringIO()
    # setup csv writer
    import csv
    csv_file = csv.writer(file)
    # write first row withspecified column headings/names
    csv_file.writerow(column_names)
    # which mode - dal or dict?
    if mode.lower() == 'dal' or mode.lower() == 'dict':
        for record in records:
            csv_file.writerow([record[field] for field in fields])
    elif mode.lower() == 'list':
        if fields == None:
            csv_file.writerows(records)
        else:
            for record in records:
                csv_file.writerow([record[field] for field in fields])
    return file


def pdf_invoice(rows, head, foot, document_number, current_date,
                legal_name, tax_id, name_currency, address_description=None, phone_description=None):
    # data = request.vars
    body = TBODY(*rows)
    table = TABLE(*[head, foot, body],
                  _border="0", _align="center", _width="100%")

    #                  _border="1", _align="center", _width="100%")

    # from gluon.contrib.pyfpdf import FPDF, HTMLMixin


    class MyFPDF(FPDF, HTMLMixin):
        def header(self):
            self.set_font('Arial', 'B', 10)
            self.cell(0, 10, u"FACTURA ELECTRONICA - %s" % document_number, 0, 1, 'R')
            self.cell(0, 10, u"RUC 20545529719", 0, 1, 'R')
            self.ln(2)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 6)
            txt = u'Página %s of %s' % (self.page_no(), self.alias_nb_pages())
            self.cell(0, 10, txt, 0, 0, 'C')

    pdf = MyFPDF()
    # first page:
    pdf.add_page()
    pdf.set_font('Arial', 'B', 8)
    pdf.cell(0, 7, u"NET VOISS S.A.C.", 0, 1)
    pdf.cell(0, 7, u"Av. Surco Nro 638 Dpto. 302", 0, 1)
    pdf.cell(0, 7, u"Santiago de Surco - LIMA - LIMA", 0, 1)
    pdf.ln(1)
    pdf.line(40, 53, 180, 53)
    pdf.ln(1)
    # pdf.set_font('Arial','B',8)
    # pdf.set_line_width(0.1)
    # pdf.ln(0.4)
    # rows = [
    #         THEAD(TR(
    #             TH("",_width="70%"),
    #             TH("",_width="30%"))),
    #         TBODY(TR(
    #                 TD(u"Señores: %s" % legal_name),TD(u"Fecha de Emisión: %s" % current_date)
    #                 ),
    #               TR(
    #                 TD(u"Dirección: %s" % address_description),TD(u"Código de Cliente:")
    #                 ),
    #               TR(
    #                 TD(u"Teléfono: %s" % phone_description),TD(u"Vendedor: José Torres")
    #                 ),
    #               TR(
    #                 TD(u"RUC: %s" % tax_id),TD(u"Moneda: %s" % name_currency)
    #                 )
    #             )
    #         ]
    # table_aux = TABLE(*rows, _border="0", _align="center", _width="100%")
    pdf.cell(0, 6, u"Señores: %s" % legal_name, 0, 0, 'L')
    pdf.cell(0, 6, u"Fecha Emisión: %s" % current_date, 0, 1, 'R')
    pdf.cell(0, 6, u"Dirección: %s" % address_description, 0, 1, 'L')
    # pdf.cell(0, 6, u"Código de Cliente:", 0, 1,'R')
    pdf.cell(0, 6, u"Teléfono: %s" % phone_description, 0, 0, 'L')
    pdf.cell(0, 6, u"Vendedor: %s" % u"José Torres", 0, 1, 'R')
    pdf.cell(0, 6, u"RUC: %s" % tax_id, 0, 0, 'L')
    pdf.cell(0, 6, u"Moneda: %s" % name_currency, 0, 1, 'R')
    # table_aux = str(XML(table_aux, sanitize=False))
    # table_aux = u'<font size="8">%s</font>' % table_aux.decode('utf8')
    # pdf.write_html(table_aux)
    table = str(XML(table, sanitize=False))
    table = u'<font size="8">%s</font>' % table.decode('utf8')
    pdf.write_html(table)
    return pdf


def data_graphics(val_start, val_end, cliente_condition='TODOS',
                  vendedor_condition='TODOS', cuenta_condition=''):
    query = """select fecha,sum(intentos),sum(completados),sum(fallados),
    sum(minutos),sum(costoclientedolsinigv),sum(costoproveedor),
    sum(ganancia),ifnull(sum(costoclientedolsinigv-costoproveedor)/sum(costoproveedor)*100,0),
    cliente,cuenta,vendedor
    from resumen_cuenta where fecha between '%s' and '%s' """ % (val_start, val_end)
    if cliente_condition != 'TODOS':
        query += "and cliente='%s' " % cliente_condition
    if vendedor_condition != 'TODOS':
        query += "and vendedor='%s' " % vendedor_condition
    if len(cuenta_condition) > 1:
        query += "and cuenta='%s'" % cuenta_condition
    query += "group by fecha;"
    # print query
    data = db2.executesql(query)
    consumo = []
    costos = []
    minutos = []
    llamadas = []
    ganancia = []
    rentabilidad = []
    costos.append(['Fecha', 'Costo'])
    consumo.append(['Fecha', 'Consumo'])
    minutos.append(['Fecha', 'Minutos'])
    llamadas.append(['Fecha', 'Llamadas', 'Completadas', 'Falladas'])
    ganancia.append(['Fecha', 'Ganancia'])
    rentabilidad.append(['Fecha', 'Rentabilidad'])
    for line in data:
        costos.append(['%s' % line[0], round(float(line[6]), 2)])
        consumo.append(['%s' % line[0], round(float(line[5]), 2)])
        minutos.append(['%s' % line[0], round(float(line[4]), 2)])
        llamadas.append(['%s' % line[0], int(line[1]), int(line[2]), int(line[3])])
        ganancia.append(['%s' % line[0], round(float(line[7]), 2)])
        rentabilidad.append(['%s' % line[0], round(float(line[8]), 2)])
    return costos, consumo, minutos, llamadas, ganancia, rentabilidad, data


def generate_graphics(val_start=None, val_end=None, num_days=30, cliente_condition='TODOS',
                      vendedor_condition='TODOS', cuenta_condition=''):
    # year = now.year
    # month = now.month - 1 or 12
    # if month == 12:
    #     year = now.year -1
    # day = now.day
    # try:
    #     last = datetime.datetime(year, month, day)
    # except:
    #     last = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    today = datetime.datetime.now()
    last = today - datetime.timedelta(days=num_days)
    if val_start is None:
        val_start = last.date()
        val_end = today.date()
    if val_end is None:
        val_end = today.date()
    query = """select fecha,sum(intentos),sum(completados),sum(fallados),
    sum(minutos),sum(costoclientedolsinigv),sum(costoproveedor),
    sum(ganancia),ifnull(sum(costoclientedolsinigv-costoproveedor)/sum(costoproveedor)*100,0),
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
    day_header = []
    costos_data = []
    consumos_data = []
    minutos_data = []
    llamadas_intentos_data = []
    llamadas_completados_data = []
    llamadas_fallados_data = []
    for line in data:
        day_header.append('%s' % line[0])
        costos_data.append(round(float(line[6]), 2))
        consumos_data.append(round(float(line[5]), 2))
        minutos_data.append(round(float(line[4]), 2))
        llamadas_intentos_data.append(int(line[1]))
        llamadas_completados_data.append(int(line[2]))
        llamadas_fallados_data.append(int(line[3]))
    costos = [day_header, costos_data]
    consumos = [day_header, consumos_data]
    minutos = [day_header, minutos_data]
    llamadas = [day_header, llamadas_intentos_data, llamadas_completados_data, llamadas_fallados_data]
    return costos, consumos, minutos, llamadas


def graphics_channels(val_start=None, val_end=None, num_days=1, cliente_condition='TODOS',
                      vendedor_condition='TODOS', cuenta_condition='', state_condition='TODOS'):
    today = datetime.datetime.now()
    last = today - datetime.timedelta(days=num_days)
    if val_start is None:
        val_start = last
        val_end = today
    if val_end is None:
        val_end = today
    #query = (db.channels_customers.id > 0)
    #rows = db(query).select(orderby=db.channels_customers.id)
    #last_row = rows.last()
    #last_time = last_row['data_time']
    #query_aux = (db.channels_customers.data_time == last_time)
    query_aux = ((db.channels_customers.data_time >= val_start) & (db.channels_customers.data_time <= val_end))
    if cliente_condition != 'TODOS':
        query_aux &= (db.channels_customers.customer==cliente_condition)
    if vendedor_condition != 'TODOS':
        query_aux &= (db.channels_customers.seller==vendedor_condition)
    if state_condition != 'TODOS':
        query_aux &= (db.channels_customers.call_state==state_condition)
    if len(cuenta_condition) > 1:
        query_aux &= (db.channels_customers.account == cuenta_condition)
        #query += "and cuenta='%s'" % cuenta_condition
    total_channels = db.channels_customers.channels.sum()
    rows = db(query_aux).select(db.channels_customers.data_time, total_channels,
                                groupby=db.channels_customers.data_time,
                                orderby=db.channels_customers.data_time)
    current_channels = []
    for row in rows:
        data_time = '{}'.format(row['channels_customers.data_time']).split(' ')
        count_channels = row['SUM(channels_customers.channels)']
        if count_channels is None or count_channels <= 0:
            continue
        current_channels.append((data_time[1], count_channels))
    return current_channels

def graphics_provider_channels(val_start=None, val_end=None, num_days=1,
                          vendedor_condition='TODOS', cuenta_condition='', state_condition='TODOS'):
        today = datetime.datetime.now()
        last = today - datetime.timedelta(days=num_days)
        if val_start is None:
            val_start = last
            val_end = today
        if val_end is None:
            val_end = today
        # query = (db.channels_customers.id > 0)
        # rows = db(query).select(orderby=db.channels_customers.id)
        # last_row = rows.last()
        # last_time = last_row['data_time']
        # query_aux = (db.channels_customers.data_time == last_time)
        query_aux = ((db.channels_providers.data_time >= val_start) & (db.channels_providers.data_time <= val_end))
        if vendedor_condition != 'TODOS':
            query_aux &= (db.channels_providers.seller == vendedor_condition)
        if state_condition != 'TODOS':
            query_aux &= (db.channels_providers.call_state == state_condition)
        if len(cuenta_condition) > 1:
            query_aux &= (db.channels_providers.provider.contains(cuenta_condition))
            # query += "and cuenta='%s'" % cuenta_condition
        total_channels = db.channels_providers.channels.sum()
        rows = db(query_aux).select(db.channels_providers.data_time, total_channels,
                                    groupby=db.channels_providers.data_time,
                                    orderby=db.channels_providers.data_time)
        current_channels = []
        for row in rows:
            data_time = '{}'.format(row['channels_providers.data_time']).split(' ')
            count_channels = row['SUM(channels_providers.channels)']
            if count_channels is None or count_channels <= 0:
                continue
            current_channels.append((data_time[1], count_channels))
        return current_channels