# -*- coding: utf-8 -*-
import number_to_letter
import collections
import types
import calendar
import csv

# from gluon.contrib.pyfpdf import FPDF, HTMLMixin
### required - do no delete
def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    query = """
    select acc.server_id,acc.login from accounts acc
    left join sige.customers_services serv
    on serv.account=acc.login
    where serv.customer is NULL order by acc.login,acc.server_id;
    """
    data = db2.executesql(query)
    costos, consumos, minutos, llamadas = generate_graphics(num_days=7)
    return dict(data=data, costos=costos, consumos=consumos, minutos=minutos, llamadas=llamadas)

def error():
    vals = request.vars
    error = vals.content
    return dict(error=error)


@auth.requires_membership('root')
def post_paid_automatic_billing():
    query = """
    select cust.id customer,serv.service,cust.name customer_name, cust.legal_name,
    cust.tax_id,serv.currency,serv.id service_code,sum(serv.setup),sum(serv.monthly),
    sum(res.minutos) minutos,if(serv.currency=1,sum(res.costoclientedoligv),
    sum(res.costoclientesoligv)) amount,date_add(cusdate.end_time, interval 1 day) start_date,
    if(per.days>0,date_add(cusdate.end_time, interval per.days day),
    date_add(cusdate.end_time, interval per.months month)) end_date
    from sige.customers cust
    left join sige.customers_services serv on serv.customer=cust.id
    left join resumen_cuenta res on res.cuenta=serv.account
    left join sige.billing_periods per on per.id=serv.billing_period
    inner join (select det.customer_service,det.end_time from sige.invoices_details det
        left join sige.invoices inv on inv.id=det.invoice
        where date_add(det.end_time, interval 1 month)<=NOW() and
        (det.customer_service,det.end_time) in
        (select inv.customer_service service,max(inv.end_time) last_time
        from sige.invoices_details inv group by customer_service) and det.status!=2)
    cusdate on cusdate.customer_service=serv.id and
    res.fecha>cusdate.end_time
    where cust.account_type=1 and
    res.fecha between date_add(cusdate.end_time, interval 1 day) and
    if(per.days>0,date_add(cusdate.end_time, interval per.days-1 day),
        date_sub(date_add(cusdate.end_time, interval per.months month), interval 1 day))
    group by cust.id,serv.service order by customer_name;
    """
    data = db2.executesql(query)
    return dict(data=data)


@auth.requires_membership('root')
def post_paid_billing():
    year = now.year
    month = now.month - 1 or 12
    if month == 12:
        year = now.year -1
    day = now.day
    try:
        last = datetime.datetime(year, month, day)
    except:
        last = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    if len(request.vars) > 0:
        if type(request.vars.start_time) is types.ListType:
            val_start = datetime.datetime.strptime(request.vars.start_time[0], '%d/%m/%Y')
            val_end = datetime.datetime.strptime(request.vars.end_time[0], '%d/%m/%Y')
        else:
            val_start = datetime.datetime.strptime(request.vars.start_time, '%d/%m/%Y')
            val_end = datetime.datetime.strptime(request.vars.end_time, '%d/%m/%Y')
    else:
        val_start = last
        val_end = datetime.datetime.now()
    val_start = val_start.date()
    val_end = val_end.date()
    form = SQLFORM.factory(
        Field('start_time', 'date', label=T('Start Date'), default=val_start),
        Field('end_time', 'date', label=T('End Date'), default=val_end),
    )
    data = []
    start_time = False
    end_time = False
    if form.process().accepted:
        start_time = form.vars.start_time
        end_time = form.vars.end_time
        query = """
            select cust.id customer,serv.service,cust.name customer_name, cust.legal_name, cust.tax_id,serv.currency,
                serv.id service_code,sum(serv.setup),sum(serv.monthly),if(sum(res.minutos) is NULL,0.0,sum(res.minutos)) minutos,
                if(serv.currency=1,if(sum(res.costoclientedoligv) is NULL, 0.0, sum(res.costoclientedoligv)),
                if(sum(res.costoclientesoligv) is NULL, 0.0, sum(res.costoclientesoligv))) amount from sige.customers cust
                left join sige.customers_services serv on serv.customer=cust.id
                left join resumen_cuenta res on res.cuenta=serv.account
        """
        query += "and res.fecha between '%s' and '%s' " % (start_time, end_time)
        query += """where cust.account_type=1 and cust.test!='T' and serv.id not in (
                select customer_service from sige.invoices_details where
                (start_time between '%s' and '%s' or end_time between '%s' and '%s') and status!=2)
        """ % (start_time, end_time, start_time, end_time)
        #
        # query += """where cust.account_type=1 and cust.tax='T' and serv.id not in (
        #         select customer_service from sige.invoices_details where
        #         (start_time between '%s' and '%s' or end_time between '%s' and '%s') and status!=2)
        # """ % (start_time, end_time, start_time, end_time)
        query += "group by cust.id,serv.service order by customer_name;"
        # query="""
        # select cust.id,serv.id,cust.name, cust.legal_name, cust.tax_id,serv.service,serv.currency,
        #     serv.setup,serv.monthly,sum(calls.duration)/60 minutes,if(serv.currency=1,sum(calls.cost*calls.ratio),
        #     sum(calls.cost)) amount from sige.customers cust
        #     left join sige.customers_services serv on serv.customer=cust.id
        #     left join accounts acc on acc.login=serv.account
        #     left join calls on acc.id_client=calls.id_client and acc.client_type=calls.client_type and
        #     acc.server_id=calls.server_id
        #     where cust.account_type=1 and
        #     serv.id not in (
        #         select customer_service from sige.invoices_details where
        #         (start_time between '%s' and '%s' or end_time between '%s' and '%s') and status!=2) and
        #     call_start between '%s' and '%s' group by cust.name,serv.service
        # """ % (start_time, end_time, start_time, end_time, start_time, end_time)
        data = db2.executesql(query)
    return dict(form = form, data=data, start_time=start_time, end_time=end_time)


@auth.requires_membership('root')
def pre_paid_billing():
    # customers = collections.OrderedDict()
    # rows = db(db.customers.id>0).select(db.customers.id,
    #     db.customers.name, orderby=db.customers.name)
    # for row in rows:
    #     customers[row.id] = "%s" % (row.name)
    # customers['TODOS'] = 'TODOS'
    # if len(request.vars) > 0:
    #     cliente_condition = request.vars.customer
    #     if cliente_condition is not None:
    #         cliente_condition = 'TODOS'
    # else:
    #     cliente_condition = 'TODOS'
    # form = SQLFORM.factory(
    #     Field('customer', label=T('Customer'), default=cliente_condition,
    #           requires=IS_IN_SET(customers)),
    # )
    # data = []
    year = now.year
    month = now.month - 1 or 12
    if month == 12:
        year = now.year -1
    day = now.day
    try:
        last = datetime.datetime(year, month, day)
    except:
        last = datetime.datetime(year, month, calendar.monthrange(year, month)[1])
    customers = collections.OrderedDict()
    sellers = collections.OrderedDict()
    rows = db(db.customers.account_type==0).select(db.customers.id,
        db.customers.name, orderby=db.customers.name)
    for row in rows:
        customers[row.id] = "%s" % (row.name)
    #customers = sorted(customers.items(), key=lambda x: customers[x])
    customers['TODOS'] = 'TODOS'
    rows = db(db.sellers.id>0).select(db.sellers.id,
        db.sellers.name, orderby=db.sellers.name)
    for row in rows:
        sellers[row.id] = "%s" % (row.name)
    sellers['TODOS'] = 'TODOS'
    if len(request.vars) > 0:
        val_start = datetime.datetime.strptime(request.vars.start_time, '%d/%m/%Y')
        val_end = datetime.datetime.strptime(request.vars.end_time, '%d/%m/%Y')
        cliente_condition = request.vars.customer
        if cliente_condition is None:
            cliente_condition = 'TODOS'
        vendedor_condition = request.vars.vendedor
        if vendedor_condition is None:
            vendedor_condition = 'TODOS'
        cuenta_condition = request.vars.cuenta
    else:
        val_start = last
        val_end = datetime.datetime.now()
        cliente_condition = 'TODOS'
        vendedor_condition = 'TODOS'
        cuenta_condition = ''
    val_start = val_start.date()
    val_end = val_end.date()
    form = SQLFORM.factory(
        Field('start_time', 'date', label=T('Start Date'), default=val_start),
        Field('end_time', 'date', label=T('End Date'), default=val_end),
        Field('customer', label=T('Customer'), default=cliente_condition,
              requires=IS_IN_SET(customers)),
        Field('cuenta', 'string', default=cuenta_condition,label=T('Account')),
    )
    data = []
    if form.process().accepted:
        customer = form.vars.customer
        start_time = "%s 00:00:00" % form.vars.start_time
        end_time = "%s 23:59:59" % form.vars.end_time
        cuenta = form.vars.cuenta
        if customer=='TODOS':
            customer_condition = (db.customers.account_type==0)
        else:
            customer_condition = (db.customers.id==customer)
        if cuenta=='TODOS':
            account_condition = (db.customers_credits.customer>0)
        else:
            account_condition = (
                db.customers_credits.login_reference.contains(cuenta))
        data=db(((db.customers_credits.condition_status==None) |
                 (db.customers_credits.condition_status==2)) &
                 (customer_condition) &
                 (account_condition) &
                 ((db.customers_credits.status_time>start_time) &
                  (db.customers_credits.status_time<end_time)) &
                  ((db.customers.test==None) | (db.customers.test=='F')) &
                  (db.customers.account_type==0)).select(
                        db.customers_credits.id,
                        db.customers_credits.customer,
                        db.customers_credits.login_reference,
                        db.customers_credits.currency,
                        db.customers_credits.amount,
                        db.customers_credits.customer_amount,
                        db.customers_credits.notes,
                        db.customers_credits.status_time,
                        left=db.customers.on(
                            db.customers.id==db.customers_credits.customer),
                        orderby=db.customers_credits.customer)
    return dict(data=data, form=form)


@auth.requires_membership('root')
def invoice():
    customer = request.vars.customer
    service = request.vars.service
    start_time = request.vars.start_time
    end_time = request.vars.end_time
    origin = request.vars.origin
    customers_addresses = collections.OrderedDict()
    rows = db(db.customers_addresses.customer==customer).select(db.customers_addresses.id,
        db.customers_addresses.name, orderby=db.customers_addresses.priority)
    for row in rows:
        customers_addresses[row.id] = "%s" % (row.name)
    query = """
        select cust.id customer,cust.name customer_name, cust.legal_name, cust.tax_id,cust.payment_mean,
            cust.tax,serv.service,serv.billing_period,cust.currency,cust.commercial_document,
            if(length(serv.account)>0, serv.account,serv.did) account,serv.currency,
            serv.setup,serv.monthly,
            if(sum(res.minutos) is NULL,0.0,sum(res.minutos)) minutos,
            if(serv.currency=1,if(sum(res.costoclientedoligv) is NULL, 0.0, sum(res.costoclientedoligv)),if(sum(res.costoclientesoligv) is NULL, 0.0, sum(res.costoclientesoligv))) amount,
            serv.id from sige.customers cust
            left join sige.customers_services serv on serv.customer=cust.id
            left join resumen_cuenta res on res.cuenta=serv.account
    """
    query += "and res.fecha between '%s' and '%s' " % (start_time, end_time)
    query += """where cust.account_type=1 and serv.id not in (
            select customer_service from sige.invoices_details where
            (start_time between '%s' and '%s' or end_time between '%s' and '%s') and status!=2) and
    """ % (start_time, end_time, start_time, end_time)
    query += "cust.id = '%s' and serv.service='%s' " % (customer, service)
    query += "group by cust.id,serv.service,serv.account,serv.did order by serv.service,serv.account,serv.did;"

    # query = """select cust.id,cust.name, cust.legal_name, cust.tax_id,cust.payment_mean,
    #     cust.tax,serv.service,serv.billing_period,cust.currency,cust.commercial_document,serv.account,serv.currency,
    #     serv.setup,serv.monthly,sum(calls.duration)/60 minutes,if(serv.currency=1,sum(calls.cost*calls.ratio),
    #     sum(calls.cost)) amount,serv.id
    #     from sige.customers cust
    #     left join sige.customers_services serv on serv.customer=cust.id
    #     left join accounts acc on acc.login=serv.account
    #     left join calls on acc.id_client=calls.id_client and acc.client_type=calls.client_type and acc.server_id=calls.server_id
    #     where cust.account_type=1 and
    #     serv.id not in (
    #         select customer_service from sige.invoices_details where
    #         (start_time between '%s' and '%s' or end_time between '%s' and '%s') and status!=2) and
    #     call_start between '%s' and '%s' and
    #     cust.id = '%s' and serv.service='%s' group by cust.name,serv.service,serv.account;""" % (
    #         start_time, end_time,start_time, end_time,start_time, end_time, customer, service)
    data = db2.executesql(query)
    tree = {}
    tmp = []
    for line in data:
        tree['id'] = line[0]
        tree['name'] = line[1]
        tree['legal_name'] = line[2]
        tree['tax_id'] = line[3]
        tree['payment_mean'] = line[4]
        if line[5] == 'True' or line[5] == 'T':
            tree['tax'] = GLOBAL_TAX
        else:
            tree['tax'] = 0
        tree['service'] = line[6]
        tree['billing_period'] = line[7]
        tree['currency'] = line[8]
        tree['document_type'] = line[9]
        tmp.append(line[10:])
    tree['data'] = tmp
    return dict(data=tree, start_time=start_time, end_time=end_time, customers_addresses=customers_addresses, origin=origin)


def regenerate():
    # invoice = request.vars.invoice
    # data_invoice = db(db.invoices.id==invoice).select(db.invoices.ALL,
    #     db.invoices_details.ALL, left=db.invoices_details.on(
    #         db.invoices.id==db.invoices_details.invoice))
    invoice = request.vars.invoice
    #data_invoice = db(db.invoices.id==invoice).select(db.invoices.ALL)
    data_invoice = db.invoices(db.invoices.id==invoice)
    address = data_invoice.customer_address
    currency = data_invoice.currency
    document_type = data_invoice.commercial_document
    document_serial = data_invoice.serial
    document_correlative = data_invoice.correlative
    total = data_invoice.gran_total
    kind = data_invoice.commercial_document
    description = db.services_invoices_descriptions(
        db.services_invoices_descriptions.service==kind).name
    total_amount = total
    notes = data_invoice.notes
    total_discount = data_invoice.discount
    gran_sub_total = data_invoice.sub_total
    tax_amount = data_invoice.tax
    current_date = data_invoice.invoice_date
    customer = data_invoice.customer
    document_number = u"%s - %s" % (document_serial, document_correlative)
    data_customer = db.customers(db.customers.id==customer)
    legal_name = data_customer.legal_name
    tax_id = data_customer.tax_id
    rows, head, foot, name_currency = layout_invoice(currency,
        total, description, total_amount, notes, total_discount,
        gran_sub_total, tax_amount)
    address_description = name_data(db.customers_addresses,address,"address")
    phone_description = name_data(db.customers_addresses,address,"main_phone")
    pdf = pdf_invoice(rows, head, foot, document_number, current_date,
                legal_name, tax_id, name_currency, address_description, phone_description)
    # pdf = pdf_invoice(rows, head, foot, document_number, current_date,
    #             legal_name, tax_id, name_currency)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=invoice-%s_%s.pdf' % (document_type, document_number)
    return pdf.output(dest='S')


def prepaid_generate():
    facturas = request.vars.factura
    boletas = request.vars.boleta
    current_date = request.vars.current_date
    if current_date is None:
        current_date = now.date()
    description = u"Por servicio de tráfico de llamadas"
    if facturas is not None:
        credits = facturas
        document_type = 1
    else:
        credits = boletas
        document_type = 2
    if type(credits) is not types.ListType:
        credits = [credits]
    total = 0
    for credit in credits:
        data_credit = db.customers_credits(db.customers_credits.id==credit)
        total += data_credit.amount
        total_amount = total
        notes = ''
        total_discount = 0
#        db(db.customers_credits.id==credit).update(condition_status=1)
    customer = data_credit.customer
    currency = data_credit.currency
    data_customer = db.customers(db.customers.id==customer)
    tax = data_customer.tax
    if tax:
        gran_sub_total = round((total*100)/(100.0+GLOBAL_TAX),2)
        tax_amount = round(total-gran_sub_total,2)
    else:
        tax_amount = 0
        gran_sub_total = 0
    legal_name = data_customer.legal_name
    tax_id = data_customer.tax_id
    data_document = db.commercial_documents(db.commercial_documents.id==document_type)
    document_serial = data_document.serial
    document_correlative = int(data_document.correlative)
    next_correlative = document_correlative + 1
    db.commercial_documents[document_type] = dict(correlative=next_correlative)
    document_number = u"%s - %s" % (document_serial, document_correlative)
    for credit in credits:
        data_credit = db.customers_credits(db.customers_credits.id==credit)
        credit_tmp = {'condition_status':1,
               'serial':document_serial,
               'correlative':document_correlative}
        db(db.customers_credits.id==credit).update(**credit_tmp)
    invoice_data = {}
    invoice_data['invoice_date'] = current_date
    invoice_data['commercial_document'] = document_type
    invoice_data['serial'] = document_serial
    invoice_data['correlative'] = document_correlative
    invoice_data['customer'] = customer
    invoice_data['currency'] = currency
    invoice_data['sub_total'] = gran_sub_total
    invoice_data['gran_total'] = total
    invoice_data['tax'] = tax_amount
    invoice_data['notes'] = notes
    invoice_data['start_time'] = now
    invoice_data['end_time'] = now
    invoice_id = db.invoices.insert(**invoice_data)
    #data_credit['condition_status'] = 1
    db.commit()
    rows, head, foot, name_currency = layout_invoice(currency,
        total, description, total_amount, notes, total_discount,
        gran_sub_total, tax_amount)
    try:
        address = db.customers_addresses((db.customers_addresses.customer==customer) & (db.customers_addresses.priority==1)).id
    except:
        address = None
    address_description = name_data(db.customers_addresses,address,"address")
    phone_description = name_data(db.customers_addresses,address,"main_phone")
    pdf = pdf_invoice(rows, head, foot, document_number, current_date,
                legal_name, tax_id, name_currency)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=invoice-%s_%s.pdf' % (document_type, document_number)
    return pdf.output(dest='S')


def generate():
    data = request.vars
    if 'current_date' in data:
        current_date = data['current_date']
    else:
        current_date = now.date()
    address = data['address']
    customer = data['customer']
    legal_name = data['legal_name']
    tax_id = data['tax_id']
#    name_currency = data['name_currency']
    tax = float(data['tax'])
    currency = data['currency']
    document_type = data['document_type']
    start_time = data['start_time']
    end_time = data['end_time']
    kind = int(data['kind'])
    total_minutes = float(data['total_minutes'])
    #total_amount = float(data['total_amount'])
    total_amount = float(data['gran_total'])
    total_discount = float(data['total_discount'])
    total = float(data['gran_total'])
    notes = data['notes']
    try:
        data_document = db.commercial_documents(db.commercial_documents.id==document_type)
    except:
        error_data = T('No Commercial Document Assigned')
        redirect(URL('administrative','error', vars=dict(content=error_data)))
    document_name = data_document.name
    if 'document_serial' in data:
        document_serial = data['document_serial']
        document_correlative = int(data['document_correlative'])
    else:
        document_serial = data_document.serial
        document_correlative = int(data_document.correlative)
        next_correlative = document_correlative + 1
        db.commercial_documents[document_type] = dict(correlative=next_correlative)
    if type(data['service']) is types.ListType:
         services = data['service']
    else:
        services = [data['service']]
    if len(notes) == 0:
        notes = ' '
    # if tax > 0:
    #     gran_sub_total = round((total*100)/(100.0+tax),2)
    #     tax_amount = round(total-gran_sub_total,2)
    # else:
    #     tax_amount = 0
    #     gran_sub_total = 0
    gran_sub_total = round((total*100)/(100.0+tax),2)
    tax_amount = round(total-gran_sub_total,2)
    symbol = name_data(db.currencies,currency,"symbol")
    address_description = name_data(db.customers_addresses,address,"address")
    phone_description = name_data(db.customers_addresses,address,"main_phone")
    try:
        description = db.services_invoices_descriptions(db.services_invoices_descriptions.service==kind).name
    except:
        error_data = T('No Service Description')
        redirect(URL('administrative','error', vars=dict(content=error_data)))
    #total_words = number_to_letter.to_word(int(total))
    #total_decimal = u"%s/100 %s" % (str(total).split('.')[1], name_currency)
    #total_letters = u"SON: %s Y %s" % (total_words, total_decimal)
    document_number = u"%s - %s" % (document_serial, document_correlative)
    details = []
    for service in services:
        account = data['account_%s' % service]
        amount = data['amount_%s' % service]
        discount = data['discount_%s' % service]
        sub_total = data['sub_total_%s' % service]
        minutes = "minutos: %s" % data['minutes_%s' % service]
        details.append([account, minutes, amount, discount, sub_total, service])
    #response.title = "%s - %s-%s - NETVOISS S.A.C." % (document_name, document_serial, document_correlative)
    #Invoice Generation
    invoice_data = {}
    invoice_data['invoice_date'] = current_date
    invoice_data['commercial_document'] = document_type
    invoice_data['serial'] = document_serial
    invoice_data['correlative'] = document_correlative
    invoice_data['customer'] = customer
    invoice_data['customer_address'] = address
    invoice_data['currency'] = currency
    invoice_data['discount'] = total_discount
    invoice_data['sub_total'] = gran_sub_total
    invoice_data['gran_total'] = total
    invoice_data['tax'] = tax_amount
    invoice_data['notes'] = notes
    invoice_data['start_time'] = start_time
    invoice_data['end_time'] = end_time
    invoice_id = db.invoices.insert(**invoice_data)
    invoice_details = []
    for line in details:
        tmp = {}
        tmp['invoice'] = invoice_id
        tmp['customer_service'] = line[5]
        tmp['start_time'] = start_time
        tmp['end_time'] = end_time
        tmp['sub_total'] = line[2]
        tmp['discount'] = line[3]
        invoice_details.append(tmp)
    db.invoices_details.bulk_insert(invoice_details)
    db.commit()
    rows, head, foot, name_currency = layout_invoice(currency,
        total, description, total_amount, notes, total_discount,
        gran_sub_total, tax_amount)
    address_description = name_data(db.customers_addresses,address,"address")
    phone_description = name_data(db.customers_addresses,address,"main_phone")
    pdf = pdf_invoice(rows, head, foot, document_number, current_date,
                legal_name, tax_id, name_currency, address_description, phone_description)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=invoice-%s_%s.pdf' % (document_type, document_number)
    return pdf.output(dest='S')


def layout_invoice(currency,
        total, description, total_amount, notes, total_discount,
        gran_sub_total, tax_amount
        ):
    name_currency = name_data(db.currencies,currency,"name")
    symbol = name_data(db.currencies,currency,"symbol")
    total_words = number_to_letter.to_word(int(total))
    format_total = "%0.2f" % (total,)
    total_decimal = u"%s/100" % str(format_total).split('.')[1]
    total_letters = u"SON: %scon %s %s" % (total_words, total_decimal,
                                          name_currency)
    total_letters = total_letters.upper()
    sales_value = gran_sub_total + total_discount
    i = 0
    col = i % 2 and "#F0F0F0" or "#FFFFFF"
    rows = []
    head = THEAD(TR(
                    TH("Descripcion",_width="50%"),
                    TH("Cantidad",_width="10%"),
                    TH("Unidad",_width="10%"),
                    TH("Valor Unitario",_width="15%"),
                    TH("Importe",_width="15%"),
                    _bgcolor="#A0A0A0"))
    foot = TFOOT(
            TR( TH(total_letters,_width="70%", _align="left"),
                TH('Importe Total',_width="10%", _align="left"),
                TH(symbol,_width="5%", _align="right"),
                TH("%0.2f" % (total),_width="15%", _align="right"),
                _bgcolor="#E0E0E0"))
    rows.append(TR(
                   TD(description, _align="left"),
                   TD(' ', _align="left"),
                   TD(' ', _align="left"),
                   TD(' ', _align="right"),
                   TD("%0.2f" % (sales_value), _align="right"),
                   _bgcolor=col))
    rows.append(TR(
                   TD(notes, _align="left"),
                   TD(' ', _align="right"),
                   TD(' ', _align="right"),
                   TD(' ', _align="right"),
                   TD(' ', _align="right"),
                   _bgcolor=col))
    rows.append(TR(
                   TD(' ', _align="left"),
                   TD(' ', _align="right"),
                   TD(' ', _align="right"),
                   TD('Sub Total', _align="right"),
                   TD("%0.2f" % (sales_value), _align="right"),
                   _bgcolor=col))
    rows.append(TR(
                   TD(' ', _align="left"),
                   TD(' ', _align="right"),
                   TD(' ', _align="right"),
                   TD('Descuento', _align="right"),
                   TD("%0.2f" % (total_discount), _align="right"),
                   _bgcolor=col))
    rows.append(TR(
                   TD(' ', _align="left"),
                   TD(' ', _align="right"),
                   TD(' ', _align="right"),
                   TD('Valor Venta', _align="right"),
                   TD("%0.2f" % (gran_sub_total), _align="right"),
                   _bgcolor=col))
    rows.append(TR(
                   TD(' ', _align="left"),
                   TD(' ', _align="right"),
                   TD(' ', _align="right"),
                   TD('IGV (18%)', _align="right"),
                   TD("%0.2f" % (tax_amount), _align="right"),
                   _bgcolor=col))
    # rows.append(TR(
    #                TD(' ', _align="left"),
    #                TD(' ', _align="right"),
    #                TD(' ', _align="right"),
    #                TD(' ', _align="right"),
    #                TD('Importe Total', _align="right"),
    #                TD(gran_sub_total, _align="right"),
    #                _bgcolor=col))
    return rows, head, foot, name_currency


@auth.requires_membership('root')
def credits():
    db.customers_credits.status_time.writable = False
    db.customers_credits.customer_amount.writable = False
#    db.customers_credits.credit_type = 1
#    query=((db.customers_credits.id>0) & (db.customers.account_type==0))
#    form = SQLFORM.grid(query,
    form = SQLFORM.grid(db.customers_credits,
        fields=[
            db.customers_credits.register_time,
            db.customers_credits.credit_type,
            db.customers_credits.customer,
            db.customers_credits.login_reference,
            db.customers_credits.currency,
            db.customers_credits.amount,
#                            db.customers.currency,
            db.customers_credits.customer_amount,
            db.customers_credits.notes,
            db.customers_credits.serial,
            db.customers_credits.correlative,
#                            db.customers_credits.condition_status,
            db.customers_credits.status,
            db.customers_credits.credit_reference,
                ],
#                        left=db.customers.on(db.customers.id==db.customers_credits.customer),
        paginate=50,
        deletable=False)
    return dict(form=form)


@auth.requires_membership('root')
def charges():
    db.customers_credits.status_time.writable = False
    db.customers_credits.customer_amount.writable = False
    db.customers_credits.credit_type = 2
    form = SQLFORM.grid(db.customers_credits,
                        fields=[
                            db.customers_credits.register_time,
                            db.customers_credits.customer,
                            db.customers_credits.credit_type,
                            db.customers_credits.login_reference,
                            db.customers_credits.currency,
                            db.customers_credits.amount,
                            db.customers_credits.customer_amount,
                            db.customers_credits.notes,
                            db.customers_credits.condition_status,
                            db.customers_credits.serial,
                            db.customers_credits.correlative,
                            db.customers_credits.status,
                            db.customers_credits.credit_reference,
                                ],
                        deletable=False)
    return dict(form=form)

@auth.requires_membership('root')
def invoice_list():
    # default_data = request.vars.mode
    # mode_list = {
    #     1: T('List'),
    #     2: T('Control'),
    # }
    # form_aux = SQLFORM.factory(
    #     Field('mode', label=T('Mode'), default=default_data, requires=IS_IN_SET(mode_list)),
    # )
    query = (db.invoices.id>0)
    edit_condition = True
    # if form_aux.process().accepted:
    #     if form_aux.vars.mode == '2':
    #         db.invoices.commercial_document.writable = False
    #         db.invoices.customer.writable = False
    #         db.invoices.serial.writable = False
    #         db.invoices.correlative.writable = False
    #         db.invoices.invoice_date.writable = False
    #         db.invoices.currency.writable = False
    #         db.invoices.sub_total.writable = False
    #         db.invoices.discount.writable = False
    #         db.invoices.gran_total.writable = False
    #         db.invoices.tax.writable = False
    #         db.invoices.notes.writable = False
    #         query = (db.invoices.status<>2)
    #         edit_condition = True
    conditional = {'invoices':query}
    form = SQLFORM.smartgrid(db.invoices,
         fields=[
             db.invoices.customer,
             db.invoices.start_time,
             db.invoices.end_time,
             db.invoices.currency,
             db.invoices.sub_total,
             db.invoices.discount,
             db.invoices.tax,
             db.invoices.gran_total,
             db.invoices.invoice_date,
             db.invoices.serial,
             db.invoices.correlative,
             db.invoices.commercial_document,
             db.invoices.invoice_due,
             db.invoices.notes,
             db.invoices.status,
             db.invoices.deliver_date,
#                                 db.invoices.void_reason,
             db.invoices_details.customer_service,
             db.invoices_details.start_time,
             db.invoices_details.end_time,
             db.invoices_details.sub_total,
             db.invoices_details.notes
         ],
         linked_tables=['invoices_details'],
         links=[dict(header=T('Regenerate'), body=lambda row: A(T('Regenerate'), _href=URL('administrative','regenerate',vars=dict(invoice=row.id))))],
         csv=False, deletable=False, editable=edit_condition, constraints=conditional)
    return dict(form=form)


@auth.requires_membership('root')
def invoice_control():
    db.invoices.commercial_document.writable = False
    db.invoices.customer.writable = False
    db.invoices.serial.writable = False
    db.invoices.correlative.writable = False
    db.invoices.invoice_date.writable = False
    db.invoices.currency.writable = False
    db.invoices.sub_total.writable = False
    db.invoices.discount.writable = False
    db.invoices.gran_total.writable = False
    db.invoices.tax.writable = False
    db.invoices.notes.writable = False
    query = (db.invoices.status<>2)
    conditional = {'invoices':query}
    form = SQLFORM.smartgrid(db.invoices,
                             fields=[
                                 db.invoices.customer,
                                 db.invoices.start_time,
                                 db.invoices.end_time,
                                 db.invoices.currency,
                                 db.invoices.sub_total,
                                 db.invoices.discount,
                                 db.invoices.tax,
                                 db.invoices.gran_total,
                                 db.invoices.invoice_date,
                                 db.invoices.serial,
                                 db.invoices.correlative,
                                 db.invoices.commercial_document,
                                 db.invoices.invoice_due,
                                 db.invoices.notes,
                                 db.invoices.status,
                                 db.invoices.deliver_date,
#                                 db.invoices.void_reason,
                                 db.invoices_details.customer_service,
                                 db.invoices_details.start_time,
                                 db.invoices_details.end_time,
                                 db.invoices_details.sub_total,
                                 db.invoices_details.notes
                             ],
                             linked_tables=['invoices_details'],
                             csv=False, deletable=False, constraints=conditional)
    return dict(form=form)

@auth.requires_membership('root')
def invoice_manage():
    form = SQLFORM.smartgrid(db.invoices,
                             linked_tables=['invoices_details'],
                             csv=False, deletable=False, editable=False)
    return dict(form=form)

@auth.requires_membership('root')
def regen_button(row):
    return A('administrative', 'regenerate', vars=dict(invoice=row.id))


@auth.requires_membership('root')
def collection():
    customers = collections.OrderedDict()
    rows = db(db.customers.id>0).select(db.customers.id,
        db.customers.name, orderby=db.customers.name)
    for row in rows:
        customers[row.id] = "%s" % (row.name)
    customers['TODOS'] = 'TODOS'
    default_customer = 'TODOS'
    data = db((db.invoices.status==0) & (db.invoices.condition_status<2)).select(
        db.invoices.id, db.invoices.serial, db.invoices.correlative)
    query_invoices = (db.invoices_collection.status == 0)
    if len(request.vars) > 0:
        default_customer = request.vars.customer
        if default_customer != 'TODOS' and default_customer is not None:
            data = db((db.invoices.status==0) & (db.invoices.condition_status<2) &
                      (db.invoices.customer==default_customer)).select(
                db.invoices.id, db.invoices.serial, db.invoices.correlative)
            query_invoices = (db.invoices_collection.status == 0) & (db.customers.id == default_customer)
    form_aux = SQLFORM.factory(
        Field('customer', label=T('Customer'), default=default_customer,requires=IS_IN_SET(customers)),
    )
    invoices = {}
    for row in data:
        invoices[row.id] = "%s-%s" % (row.serial, row.correlative)
    db.invoices_collection.invoice.requires = IS_IN_SET(invoices)
    #query = (db.invoices_collection.status == 0)
    form = SQLFORM.grid(query_invoices, deletable=False,
                left=(
                    db.invoices.on(db.invoices.id==db.invoices_collection.invoice),
                    db.customers.on(db.customers.id==db.invoices.customer)
                ),
                fields=[
                    db.customers.name,
                    db.invoices_collection.invoice,
                    db.invoices_collection.payment_date,
                    #db.invoices_collection.service,
                    #db.invoices_collection.account_type,
                    db.invoices_collection.kind,
                    db.invoices_collection.amount,
                    db.invoices_collection.notes,
                    db.invoices_collection.status,
                ],
            )
    return dict(form=form, form_aux=form_aux, data=data)


@auth.requires_membership('root')
def customer_balance():
    lines = []
    csv_path = False
    customer = False
    content = []
    customers = collections.OrderedDict()
    rows = db(db.customers.id>0).select(db.customers.id,
        db.customers.name, orderby=db.customers.name)
    for row in rows:
        customers[row.id] = "%s" % (row.name)
    customers['TODOS'] = 'TODOS'
    default_customer = 'TODOS'
    if len(request.vars) > 0:
        default_customer = request.vars.customer
    form = SQLFORM.factory(
        Field('customer', label=T('Customer'), default=default_customer,requires=IS_IN_SET(customers)),
    )
    if form.process().accepted:
        customer = form.vars.customer
        if customer == 'TODOS':
            query_customer = (db.invoices.id>0)
        else:
            query_customer = (db.invoices.customer == customer)
        data = db((db.invoices.status==0) & query_customer).select(
            db.invoices.id,
            db.invoices.commercial_document,
            db.invoices.serial,
            db.invoices.correlative,
            db.invoices.invoice_date,
            db.invoices.invoice_due,
            db.invoices.customer,
            db.invoices.start_time,
            db.invoices.end_time,
            db.invoices.currency,
            db.invoices.sub_total,
            db.invoices.tax,
            db.invoices.gran_total,
            db.invoices.condition_status,
            db.invoices.status,db.invoices_collection.payment_date,
            db.invoices_collection.kind, db.invoices_collection.amount,
            db.invoices.deliver_date,
            left=db.invoices_collection.on(db.invoices.id==db.invoices_collection.invoice),
            orderby=db.invoices.customer|db.invoices.invoice_date|db.invoices_collection.payment_date)
        lines = {}
        amount_detraction = 0
        amount_balance = 0
        bota = []
        for line in data:
            invoice_id = line.invoices.id
            customer = line.invoices.customer
            name_customer = name_data(db.customers, customer)
            ruc_customer = name_data(db.customers, customer, 'tax_id')
            client_type = name_data(db.customers, customer, 'account_type')
            name_client_type = account_types[int(client_type)]
            invoice_date = line.invoices.invoice_date
            invoice_due = line.invoices.invoice_due
            commercial_document = line.invoices.commercial_document
            name_commercial_document = name_data(db.commercial_documents, commercial_document)
            serial = line.invoices.serial
            correlative = line.invoices.correlative
            document_number = '%s-%s' % (serial, correlative)
            period = '%s-%s' % (line.invoices.start_time, line.invoices.end_time)
            currency = line.invoices.currency
            symbol_currency = name_data(db.currencies, currency, 'symbol')
            payment_kind = line.invoices_collection.kind
            type_payment_kind = name_data(db.payment_kinds, payment_kind, 'detraction')
            kind_amount_applied = db.payment_kinds(
                db.payment_kinds.detraction=='True').amount_applied
            kind_amount_applied = float(kind_amount_applied)
            gran_total = float(line.invoices.gran_total)
            if currency == 1:
                kind_amount_applied = kind_amount_applied / 2.8
            if gran_total > kind_amount_applied:
                detraction = (gran_total * DETRACTION) / 100.0
            else:
                detraction = 0
            total = gran_total - detraction
            condition = line.invoices.condition_status
            name_condition = invoices_options[condition]
            deliver_date = line.invoices.deliver_date
            status = line.invoices.status
            name_status = invoices_status[status]
            payment_amount = line.invoices_collection.amount
            payment_date = line.invoices_collection.payment_date
            if invoice_id not in lines:
                amount_detraction = 0
                amount_balance = 0
            lines.setdefault(invoice_id, [
                name_commercial_document,
                document_number,
                invoice_date,
                invoice_due,
                name_customer,
                ruc_customer,
                period,
                symbol_currency,
                round(total,2),
                round(total,2),
                round(detraction,2),
                round(detraction,2),
                deliver_date,
                payment_date,
                name_status,
                name_client_type,
            ])
            #print "aaaa--->",payment_amount, detraction, amount_detraction
            if payment_amount is None:
                payment_amount = 0
            if detraction is None:
                detraction = 0
            if amount_detraction is None:
                amount_detraction = 0
            if invoice_id in lines:
                if type_payment_kind=='True':
                    amount_detraction += payment_amount
                    lines[invoice_id][11] = round(detraction - amount_detraction, 2)
                else:
                    amount_balance += payment_amount
                    lines[invoice_id][9] = round(total - amount_balance, 2)
                lines[invoice_id][13] = payment_date
            else:
                amount_detraction = 0
                amount_balance = 0
        for key in lines:
            tmp = []
            for elem in lines[key]:
                tmp.append(elem)
            content.append(tmp)
        headers = ['Documento','Numero','Fecha de Emision', 'Fecha de Vencimiento',
                   'Cliente', 'RUC', 'Periodo', 'Moneda', 'Importe', 'Saldo Importe',
                   'Detraccion', 'Saldo Detraccion', 'Fecha de Entrega', 'Fecha de Estado',
                   'Estado', 'Tipo Cliente'
                   ]
        file_name = "customer_balance-%s.csv" % (now)
        file_url = "%s/%s" % (UPLOAD_PATH, file_name)
        csv_path = "%s" % file_name
        #content = data.as_list()
        out = csv.writer(open(file_url,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
        out.writerow(headers)
        out.writerows(content)
    return dict(form= form, data=lines, csv_path=csv_path, content=content, customer=customer)





def process_payment_list():
    void = request.vars.void
    paid = request.vars.paid
    if void:
        db.invoices[void] = dict(status=2)
    else:
        if paid:
            db.invoices[paid] = dict(status=1)
    redirect('customer_balance')
    return dict()

def prepaid_debit():
    customer = request.vars.customer
    service = request.vars.service
    facturas = request.vars.factura
    boletas = request.vars.boleta
    current_date = request.vars.current_date
    if current_date is None:
        current_date = now.date()
    description = u"Por servicio de tráfico de llamadas"
    if facturas is not None:
        credits = facturas
        document_type = 1
    else:
        credits = boletas
        document_type = 2
    if type(credits) is not types.ListType:
        credits = [credits]
    total = 0
    for credit in credits:
        data_credit = db.customers_credits(db.customers_credits.id==credit)
        total += data_credit.amount
        total_amount = total
        notes = ''
        total_discount = 0
#        db(db.customers_credits.id==credit).update(condition_status=1)
    customer = data_credit.customer
    currency = data_credit.currency
    data_customer = db.customers(db.customers.id==customer)
    tax = data_customer.tax
    if tax:
        gran_sub_total = round((total*100)/(100.0+GLOBAL_TAX),2)
        tax_amount = round(total-gran_sub_total,2)
    else:
        tax_amount = 0
        gran_sub_total = 0
    legal_name = data_customer.legal_name
    tax_id = data_customer.tax_id
    data_document = db.commercial_documents(db.commercial_documents.id==document_type)
    document_serial = data_document.serial
    document_correlative = int(data_document.correlative)
    next_correlative = document_correlative + 1
    db.commercial_documents[document_type] = dict(correlative=next_correlative)
    document_number = u"%s - %s" % (document_serial, document_correlative)
    for credit in credits:
        data_credit = db.customers_credits(db.customers_credits.id==credit)
        credit_tmp = {'condition_status':1,
               'serial':document_serial,
               'correlative':document_correlative}
        db(db.customers_credits.id==credit).update(**credit_tmp)
    invoice_data = {}
    invoice_data['invoice_date'] = current_date
    invoice_data['commercial_document'] = document_type
    invoice_data['serial'] = document_serial
    invoice_data['correlative'] = document_correlative
    invoice_data['customer'] = customer
    invoice_data['currency'] = currency
    invoice_data['sub_total'] = gran_sub_total
    invoice_data['gran_total'] = total
    invoice_data['tax'] = tax_amount
    invoice_data['notes'] = notes
    invoice_data['start_time'] = now
    invoice_data['end_time'] = now
    invoice_id = db.invoices.insert(**invoice_data)
    #data_credit['condition_status'] = 1
    db.commit()
    rows, head, foot, name_currency = layout_invoice(currency,
        total, description, total_amount, notes, total_discount,
        gran_sub_total, tax_amount)
    # address_description = name_data(db.customers_addresses,address,"address")
    # phone_description = name_data(db.customers_addresses,address,"main_phone")
    # pdf = pdf_invoice(rows, head, foot, document_number, current_date,
    #             legal_name, tax_id, name_currency, address_description, phone_description)
    try:
        address = db.customers_addresses((db.customers_addresses.customer==customer) & (db.customers_addresses.priority==1)).id
    except:
        address = None
    address_description = name_data(db.customers_addresses,address,"address")
    phone_description = name_data(db.customers_addresses,address,"main_phone")
    pdf = pdf_invoice(rows, head, foot, document_number, current_date,
                legal_name, tax_id, name_currency)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment;filename=invoice-%s_%s.pdf' % (document_type, document_number)
    return pdf.output(dest='S')

def get_csv():
    file_name = request.vars.file_name
    return dict(file_name=file_name)

def service_control():
    customers = collections.OrderedDict()
    rows = db(db.customers.id>0).select(db.customers.id,
        db.customers.name, orderby=db.customers.name)
    for row in rows:
        customers[row.id] = "%s" % (row.name)
    customers['TODOS'] = 'TODOS'
    order_options = {
        0: T('Customer'),
        1: T('Service'),
        2: T('Due Days'),
    }
    additional_types = account_types
    additional_types['TODOS'] = 'TODOS'
    if len(request.vars) > 0:
        default_type = request.vars.account_type
        default_customer = request.vars.customer
        default_order = request.vars.order_by
    else:
        default_type = 'TODOS'
        default_customer = 'TODOS'
        default_order = 2
    form = SQLFORM.factory(
        Field('customer', label=T('Customer'), default=default_customer,requires=IS_IN_SET(customers)),
#        Field('account_type', label=T('Type'), default=default_type, requires=IS_IN_SET(additional_types)),
        Field('order_by', label=T('Order Type'), default=default_order, requires=IS_IN_SET(order_options)),
        Field('test', 'boolean', label=T('Test')),
    )
    data = []
    if form.process().accepted:
        customer = form.vars.customer
        account_type = 1
#        account_type = form.vars.account_type
        order_by = form.vars.order_by
        test = form.vars.test
        query_str = """
        select serv.id,cust.name customer_name, serv.service,
        if(length(serv.account)>0, serv.account,serv.did) account,inv.end_time last_date_invoice,
        date_add(inv.end_time, interval 1 day) start_date,
        if(per.days>0,date_add(inv.end_time, interval per.days day), last_day(date_add(inv.end_time, interval per.months month))) end_date,
        datediff(if(per.days>0,date_add(inv.end_time, interval per.days day),last_day(date_add(inv.end_time, interval per.months month))),curdate()) difference_days,
        cust.id, cust.account_type
        from sige.customers cust
        left join sige.customers_services serv on serv.customer=cust.id
        left join sige.billing_periods per on per.id=serv.billing_period
        left join sige.invoices_details inv on inv.customer_service=serv.id
        where serv.id > 0
        """
        if customer != 'TODOS':
            query_str += "and cust.id='%s' " % customer
 #       if account_type != 'TODOS':
        query_str += "and cust.account_type='%s' " % account_type
        if test is True:
            query_str += "and cust.test='T' "
        else:
            query_str += "and (cust.test is NULL or cust.test='F')"
        if order_by == '0':
            query_str += "order by cust.name asc"
        elif order_by == '1':
            query_str += "order by serv.service asc, cust.name"
        else:
            query_str += "order by difference_days desc, cust.name"
        query = query_str
        data = db2.executesql(query)
    return dict(form=form, data=data)

@auth.requires_membership('root')
def pre_notify():
    invoice = request.vars.invoice
    customer = request.vars.customer
    if invoice is not None:
        data = db.mail_notifications(db.mail_notifications.kind==1)
        subject = data['subject']
        message = data['content_message']
        mail_notify(invoice, subject, message)
    redirect(URL('administrative','customer_balance', vars=dict(customer=customer)))
    return dict()

@auth.requires_membership('root')
def post_notify():
    invoice = request.vars.invoice
    customer = request.vars.customer
    if invoice is not None:
        data = db.mail_notifications(db.mail_notifications.kind==2)
        subject = data['subject']
        message = data['content_message']
        mail_notify(invoice, subject, message)
    redirect(URL('administrative','customer_balance', vars=dict(customer=customer)))
    return dict()
    # db.mail_queue.insert(status='1',
    #                      email=area_email,
    #                      subject=subject,
    #                      content_message=message)
