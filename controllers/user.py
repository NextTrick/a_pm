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

#@auth.requires(restrictions)
@auth.requires_membership('root')
def manage():
    response.view = 'default.html'
    title = T('Manage')
    form = SQLFORM.grid(db.auth_user,
        csv=False, deletable=False)
    return dict(form=form, title=title)

#@auth.requires(restrictions)
@auth.requires_membership('root')
def groups():
    response.view = 'default.html'
    title = T('Groups')
    form = SQLFORM.grid(db.auth_group,
        csv=False, deletable=False)
    return dict(form=form, title=title)


#@auth.requires(restrictions)
@auth.requires_membership('root')
def membership():
    response.view = 'default.html'
    title = T('Membership')
    form = SQLFORM.grid(db.auth_membership,
        csv=False, deletable=False)
    return dict(form=form, title=title)

@auth.requires_membership('root')
def sellers():
    response.view = 'default.html'
    title = T('Sellers')
    form = SQLFORM.grid(db.sellers, deletable=False)
    return dict(form=form, title=title)