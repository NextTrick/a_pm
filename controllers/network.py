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
def database():
    service = db.services_classes(db.services_classes.name=='DB')
    db.services_servers.service_class.default = service.id
    db.services_servers.service_class.writable = False
    query = (db.services_servers.service_class==service.id)
    form = SQLFORM.grid(query)
    return dict(form=form)

@auth.requires_membership('root')
def ftp():
    service = db.services_classes(db.services_classes.name=='FTP')
    db.services_servers.service_class.default = service.id
    db.services_servers.service_class.writable = False
    query = (db.services_servers.service_class==service.id)
    form = SQLFORM.grid(query)
    return dict(form=form)

@auth.requires_membership('root')
def cacti():
    service = db.services_classes(db.services_classes.name=='CACTI')
    db.services_servers.service_class.default = service.id
    db.services_servers.service_class.writable = False
    query = (db.services_servers.service_class==service.id)
    form = SQLFORM.grid(query)
    return dict(form=form)

def sms():
    return dict()

def smtp():
    return dict()