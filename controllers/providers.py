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
    title = T('Provider Manage')
    form = SQLFORM.smartgrid(db.providers,
                             linked_tables=['providers_addresses', 'providers_contacts',
                                            'providers_contacts_phones', 'providers_banks'],
                             csv=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def contract():
    response.view = 'default.html'
    title = T('Provider Contracts')
    form = SQLFORM.smartgrid(db.providers_contracts,
                             linked_tables=['providers_contracts_documents'],
                             csv=False)
    return dict(form=form, title=title)