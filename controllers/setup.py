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
def voip():
    response.view = 'default.html'
    title = T('VOIP Servers')
    service = db.services_classes(db.services_classes.name=='IPSWITCH')
    db.services_servers.service_class.default = service.id
    db.services_servers.service_class.writable = False
    query = (db.services_servers.service_class==service.id)
    form = SQLFORM.grid(query)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def service():
    response.view = 'default.html'
    title = T('Services')
    form = SQLFORM.grid(db.customers_services,
                        deletable=False,
                        paginate=100,
                        left=db.customers.on(db.customers.id==db.customers_services.customer),
                        fields=[
                            db.customers_services.customer,
                            db.customers_services.seller,
                            db.customers_services.service,
                            db.customers.account_type,
                            db.customers_services.currency,
                            db.customers_services.billing_period,
                            db.customers_services.package,
                            db.customers_services.account,
                            db.customers_services.did,
                            db.customers_services.status,
                        ],
#                        links=[dict(header=T('Duplicate'), body=lambda row: A(T('Duplicate'), _href=URL('customer_service','duplicate',vars=dict(customer_service=row.customers_services.id))))],
    )
    return dict(form=form, title=title)