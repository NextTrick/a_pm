# -*- coding: utf-8 -*-#

def name_data(table, id_val, field='name'):
    """
    Content Data Representation
    """
    try:
        value_data = table(id_val)[field]
    except:
        value_data = ''
    data = '%s' % value_data
    data = data.decode('utf8')
    return data

def complex_data(id_val):
    """
    Content Data Representation
    """
    try:
        value_data = db.customers_services(id_val)
    except:
        value_data = ''
    service_name = services_options[value_data['service']]
    service_name = service_name.decode('utf8')
    service_id = value_data['id']
    data = u'%s-%s' % (service_name, service_id)
    #data = data.decode('utf8')
    return data


def send_mail(vals, id):
    try:
        register = vals['register_time']
    except:
        ticket_id = vals.select().first().id
        vals = dict(id)
        vals['ticket'] = ticket_id
        vals['content_data'] = T('Status or Area Change')
    user_code = vals['user_req']
    ticket = db.tickets(db.tickets.id==vals['ticket'])
    company = name_data(db.customers, ticket.customer, 'name')
    try:
        service_id = services_options[ticket.service]
        service_id = service_id.decode('utf8')
    except:
        service_id = T('General')
    area_email = db.areas(ticket.area).email
    user_email = db.auth_user(user_code).email
    area_name = name_data(db.areas, ticket.area, 'name')
    subject = u"%s -- Ticket: %s - Empresa: %s Servicio: %s - Comunicación" % (
        area_name, ticket.id, company, service_id)
    message = vals['content_data']
    db.mail_queue.insert(status='1',
                         email=user_email,
                         subject=subject,
                         content_message=message)
    db.mail_queue.insert(status='1',
                         email=area_email,
                         subject=subject,
                         content_message=message)
    return

def insert_rates(vals, id):
    customer = vals['customer']
    origin_currency = vals['currency']
    destination_currency = db.customers(db.customers.id==customer).currency
    rows = db(  ((db.currencies_exchange_rates.currency==origin_currency) |
                (db.currencies_exchange_rates.destination_currency==origin_currency)) &(
                (db.currencies_exchange_rates.currency==destination_currency) |
                (db.currencies_exchange_rates.destination_currency==destination_currency))
        ).select(
        db.currencies_exchange_rates.currency,
        db.currencies_exchange_rates.destination_currency,
        db.currencies_exchange_rates.rate)
    if len(rows) <= 0:
        currency_1 = False
        currency_2 = False
        rate = 1
    else:
        data = rows.last()
        currency_1 = data.currency
        currency_2 = data.destination_currency
        rate = data.rate
    customer_amount = 0
    if origin_currency == destination_currency:
        customer_amount = round(vals['amount'], 2)
    else:
        if origin_currency == currency_1:
            customer_amount = round(vals['amount'] * rate, 2)
        else:
            customer_amount = round(vals['amount'] / rate, 2)
    #customer_amount = vals['amount'] * rate
    status_time = now
    elems = {'customer_amount':customer_amount, 'status_time':status_time}
    status = db(db.customers_credits.id==id).update(**elems)
    db.commit()

def prepaid_invoice(values, set):
    try:
        status = values['status']
        customer = values['customer']
        currency = values['currency']
        total = values['amount']
    except:
        return
    if status != 0:
        return
    data = db.customers(db.customers.id==customer)
    document_type = data['commercial_document']
    data_document = db.commercial_documents(
        db.commercial_documents.id==document_type)
    document_serial = data_document.serial
    document_correlative = int(data_document.correlative)
    next_correlative = document_correlative + 1
    db.commercial_documents[document_type] = dict(correlative=next_correlative)
    tax = data['tax']
    if status == 1:
        if tax:
            tax_amount = round((total*GLOBAL_TAX)/100.0,2)
            sub_total = round(total-tax_amount,2)
        else:
            sub_total = 0
            tax_amount = 0
        invoice_data = {}
        invoice_data['commercial_document'] = document_type
        invoice_data['serial'] = document_serial
        invoice_data['correlative'] = document_correlative
        invoice_data['customer'] = customer
        invoice_data['currency'] = currency
        invoice_data['sub_total'] = sub_total
        invoice_data['gran_total'] = total
        invoice_data['tax'] = tax_amount
        invoice_data['notes'] = T('Prepaid Credit')
        invoice_id = db.invoices.insert(**invoice_data)
    return


def invoice_update(values, set):
    status = values['status']
    if status == 2:
        invoice_id = set.select().first().id
        db(db.invoices_details.invoice==invoice_id).update(status=2)
        data_invoice = db.invoices(db.invoices.id==invoice_id)
        serial = data_invoice.serial
        correlative = data_invoice.correlative
        credit_tmp = {'condition_status':2, 'serial':None, 'correlative':None}
        db((db.customers_credits.serial==serial) &
           (db.customers_credits.correlative==correlative)).update(**credit_tmp)
    return


def mail_notify(invoice, subject, message):
    data = db.invoices(db.invoices.id==invoice)
    customer = data['customer']
    invoice_number = '%s - %s' % (data['serial'], data['correlative'])
    invoice_amount = data['gran_total']
    invoice_due = data['invoice_due']
    invoice_currency = db.currencies(db.currencies.id==data['currency'])['name']
    symbol_currency = db.currencies(db.currencies.id==data['currency'])['symbol']
    customer_name = db.customers(db.customers.id==customer)['name']
    customer_emails = db((db.customers_contacts.customer==customer) &
                         (db.customers_contacts.notification=='True')).select(
        db.customers_contacts.email)
    content = {
        'invoice_number': invoice_number,
        'invoice_amount': invoice_amount,
        'invoice_due' : invoice_due,
        'invoice_currency' : invoice_currency,
        'customer_name' : customer_name,
        'symbol_currency' : symbol_currency
    }
    subject = subject % (content)
    message = message % (content)
    for row in customer_emails:
        db.mail_queue.insert(status='1',
                             email=row.email,
                             subject=subject,
                             content_message=message)
        db.mail_queue.insert(status='1',
                             email=mail.settings.sender,
                             subject=subject,
                             content_message=message)
    return