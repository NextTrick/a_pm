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
def manage():
    response.view = 'default.html'
    title = T('Customer Management')
    db.services_configurations.customer_service.writable = False
    form = SQLFORM.smartgrid(db.customers,
                             linked_tables=['customers_addresses', 'customers_contacts',
                                            'customers_contacts_phones', 'customers_services',
                                            'customers_rates', 'customers_contracts',
                                            'customers_contracts_documents',
                                            'services_configurations'],
                             fields=[db.customers.name,
                                     db.customers.legal_name,db.customers.tax_id,
                                     db.customers.activity_start,db.customers.account_type,
                                     db.customers.currency,db.customers.commercial_document,
                                     db.customers.tax, db.customers.status,
                                     db.customers_addresses.name, db.customers_addresses.address,
                                     db.customers_addresses.reference, db.customers_addresses.country,
                                     db.customers_addresses.tax_address,
                                     db.customers_contacts.area, db.customers_contacts.role,
                                     db.customers_contacts.document_id, db.customers_contacts.name,
                                     db.customers_contacts.email,
                                     db.customers_contacts_phones.name, db.customers_contacts_phones.phone,
                                     db.customers_contacts_phones.extension, db.customers_contacts_phones.main,
                                     db.customers_contracts.name, db.customers_contracts.start_date,
                                     db.customers_contracts.end_date, db.customers_contracts.archive,
                                     db.customers_contracts_documents.name, db.customers_contracts_documents.archive,
                                     db.customers_rates.package, db.customers_rates.name,
                                     db.customers_rates.rate,
                                     db.customers_services.service, db.customers_services.seller,
                                     db.customers_services.billing_period,
                                     db.customers_services.currency, db.customers_services.did,
                                     db.customers_services.account, db.customers_services.password,
                                     db.services_configurations.provider, db.services_configurations.billing_period,
                                     db.services_configurations.currency, db.services_configurations.rate_cost
                                     ],
                             #buttons_placement='left',
                             #links_placement='left',
                             csv=False)
    return dict(form=form, title=title)


@auth.requires_membership('root')
def contract():
    response.view = 'default.html'
    title = T('Customer Contracts')
    form = SQLFORM.smartgrid(db.customers_contracts,
                             linked_tables=['customers_contracts_documents'],
                             csv=False)
    return dict(form=form, title=title)