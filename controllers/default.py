# -*- coding: utf-8 -*-
### required - do no delete
def user():
    #auth.login(next=URL('services', 'index'))
    #auth.settings.login_next = URL('services','index')
    db.auth_user.customer.writable = False
    return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
def index():
    if auth.user:
        if auth.has_membership(user_id=auth.user.id, role='root'):
            redirect(URL('administrative','index'))
        elif auth.has_membership(user_id=auth.user.id, role='customer'):
            redirect(URL('services','index'))
    return dict()

def error():
    return dict()

