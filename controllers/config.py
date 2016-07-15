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

#Basics
@auth.requires_membership('root')
def customers():
    response.view = 'default.html'
    title = T('Customers')
    form = SQLFORM.grid(db.customers, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def packages():
    response.view = 'default.html'
    title = T('Packages')
    form = SQLFORM.grid(db.packages, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def areas():
    response.view = 'default.html'
    title = T('Areas')
    form = SQLFORM.grid(db.areas, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def roles():
    response.view = 'default.html'
    title = T('Roles')
    form = SQLFORM.grid(db.roles, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def business_areas():
    response.view = 'default.html'
    title = T('Business Areas')
    form = SQLFORM.grid(db.business_areas, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def services_classes():
    response.view = 'default.html'
    title = T('Services Classes')
    form = SQLFORM.grid(db.services_classes, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def countries():
    response.view = 'default.html'
    title = T('Countries')
    form = SQLFORM.grid(db.countries, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def cities():
    response.view = 'default.html'
    title = T('Cities')
    form = SQLFORM.grid(db.cities, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def currencies():
    response.view = 'default.html'
    title = T('Currencies')
    form = SQLFORM.smartgrid(db.currencies,
                             linked_tables=['currencies_exchange_rates'],
                             csv=False, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def payment_means():
    response.view = 'default.html'
    title = T('Payment Means')
    form = SQLFORM.grid(db.payment_means, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def payment_kinds():
    response.view = 'default.html'
    title = T('Payment Kinds')
    form = SQLFORM.grid(db.payment_kinds, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def billing_periods():
    response.view = 'default.html'
    title = T('Billing Periods')
    form = SQLFORM.grid(db.billing_periods, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def payment_methods():
    response.view = 'default.html'
    title = T('Payment Methods')
    form = SQLFORM.grid(db.payment_methods, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def commercial_documents():
    response.view = 'default.html'
    title = T('Commercial Documents')
    form = SQLFORM.grid(db.commercial_documents, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def banks():
    response.view = 'default.html'
    title = T('Banks')
    form = SQLFORM.grid(db.banks, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def banks_account_types():
    response.view = 'default.html'
    title = T('Banks Account Types')
    form = SQLFORM.grid(db.bank_account_types, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def services_descriptions():
    response.view = 'default.html'
    title = T('Services Descriptions')
    form = SQLFORM.grid(db.services_invoices_descriptions, deletable=False)
    return dict(form=form, title=title)


@auth.requires_membership('root')
def mail_notifications():
    response.view = 'default.html'
    title = T('Mail Notifications')
    form = SQLFORM.grid(db.mail_notifications, deletable=False)
    return dict(form=form, title=title)