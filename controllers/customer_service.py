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
def profile():
    try:
        user = auth.user.id
    except:
        redirect(URL('default','index'))
    customer_id = auth.user.customer
    customer = db.customers(db.customers.id==customer_id)
    customer_addresses = db(db.customers_addresses.customer==customer_id).select()
    customer_contacts = db(db.customers_contacts.customer==customer_id).select(db.customers_contacts.ALL,
        db.customers_contacts_phones.ALL,
        left=db.customers_contacts_phones.on(db.customers_contacts.id==db.customers_contacts_phones.customer_contact))
    #customer_contact_phone = db.customers_contacts_phones(db.customers_contacts_phones.customer_contact==customer_contact.id)
    #form = SQLFORM.factory(db.customers,db.customers_addresses,db.customers_contacts,db.customers_contacts_phones)
    # customer = auth.user.customer
    # query = (db.customers.id ==customer)
    # db.customers.account_type.writable = False
    # db.customers.currency.writable = False
    # db.customers.payment_mean.writable = False
    # db.customers.payment_method.writable = False
    # db.customers.commercial_document.writable = False
    # db.customers.status.writable = False
    # db.customers.tax.writable = False
    # db.customers.activity_start.writable = False
    # db.customers.electronic_file.writable = False
    # db.customers_addresses.customer.writable = False
    # db.customers_addresses.tax_address.writable = False
    # db.customers_contacts.customer.writable = False
    # db.customers_contacts.main.writable = False
    # db.customers_contacts_phones.customer_contact.writable = False
    # form = SQLFORM.smartgrid(db.customers,
    #                          fields=[
    #                                  db.customers.name,
    #                                  db.customers.legal_name,db.customers.tax_id,
    #                                  db.customers.activity_start,db.customers.account_type,
    #                                  db.customers.currency,db.customers.commercial_document,
    #                                  db.customers.tax, db.customers.status,
    #                                  db.customers_addresses.name, db.customers_addresses.address,
    #                                  db.customers_addresses.reference, db.customers_addresses.country,
    #                                  db.customers_addresses.tax_address,
    #                                  db.customers_contacts.area, db.customers_contacts.role,
    #                                  db.customers_contacts.document_id, db.customers_contacts.name,
    #                                  db.customers_contacts.email,
    #                                  db.customers_contacts_phones.name, db.customers_contacts_phones.phone,
    #                                  db.customers_contacts_phones.extension, db.customers_contacts_phones.main,
    #                          ],
    #                          linked_tables=['customers_addresses', 'customers_contacts',
    #                                         'customers_contacts_phones'],
    #                          constraints= dict(customers=query),
    #                          csv=False, deletable=False)
    #return dict(form=form)
    return dict(customer=customer, customer_addresses=customer_addresses, customer_contacts=customer_contacts)


@auth.requires_membership('root')
def price_list():
    form = SQLFORM.grid(db.customers_rates)
    return dict(form=form)




@auth.requires_membership('root')
def duplicate():
    customer_service = request.vars.customer_service
    #data_invoice = db(db.invoices.id==invoice).select(db.invoices.ALL)
    data_service = db.customers_services(db.customers_services.id==customer_service).as_dict()
    aux_service = dict((k,v) for k,v in data_service.iteritems() if v is not None)
    data_service = dict((k,v) for k,v in aux_service.iteritems() if k is not 'id')
    db.customers_services.insert(**data_service)
    redirect(URL('customer_service','service'))

