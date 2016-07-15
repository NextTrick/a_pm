# -*- coding: utf-8 -*-
### required - do no delete
def user(): return dict(form=auth())
def download():
    import os
    filename = request.args(0)
    filename = os.path.join(UPLOAD_PATH, filename)
    ret = open(filename, 'rb')
    response.headers['Content-Disposition'] = 'attachment;filename=%s' % (filename)
    return ret.read()
    #return response.download(request,db)

def call(): return service()
### end requires
def index():
    return dict()

def error():
    return dict()

@auth.requires_login()
def tickets():
    try:
        user = auth.user.id
    except:
        redirect(URL('default','index'))
    customer = auth.user.customer
    role = 'user'
    if auth.has_membership(user_id=auth.user.id, role='root'):
        data = db(((db.tickets.status>=0))).select()
        role = 'root'
    else:
        data = db(((db.tickets.status>=0) & (db.tickets.customer==customer))).select()
    return dict(data=data, role=role)

@auth.requires_login()
def ticket_new():
    try:
        user = auth.user.id
    except:
        redirect(URL('default','index'))
    customer = auth.user.customer
    service = request.vars.service
    area = request.vars.area
    db.tickets.user_req.default = user
    db.tickets.customer.default = customer
    db.tickets_workflow.user_req.default = user
    db.tickets.status.default = 0
    if service is not None:
        db.tickets.service.default = service
        db.tickets.service.writable = False
        db.tickets.area.default = area
        db.tickets.area.writable = False
        service = int(service)
    db.tickets.customer.writable = False
    db.tickets.register_time.writable = False
    db.tickets.user_req.writable = False
    db.tickets.status.writable = False
#    db.tickets_workflow.auxiliar_data.uploadfolder = UPLOAD_PATH
    form = SQLFORM.factory(db.tickets,db.tickets_workflow)
    if form.process().accepted:
        id = db.tickets.insert(**db.tickets._filter_fields(form.vars))
        form.vars.ticket=id
        id = db.tickets_workflow.insert(**db.tickets_workflow._filter_fields(form.vars))
        response.flash=T('Ticket Processed')
        redirect(URL('tickets'))
#    form = SQLFORM(db.tickets)
    return dict(form=form, service=service)


@auth.requires_login()
def charge_new():
    try:
        user = auth.user.id
    except:
        redirect(URL('default','index'))
    customer = auth.user.customer
#    service = request.vars.service
    form = SQLFORM.factory(
        Field('content_data', 'text', label=T('Message')),
        Field('auxiliar_data', 'upload', label=T('Attachment'), uploadfolder=UPLOAD_PATH),
    )
    if form.process().accepted:
        content_data = form.vars.content_data
        auxiliar_data = form.vars.auxiliar_data
        data_tickets = {
            'customer':customer,
            'area':2,
            'user_req':user,
            'brief':'Recarga',
            'status':0
        }
        id = db.tickets.insert(**data_tickets)
        db.commit()
        extra_data = {
            'ticket':id,
            'user_req':user,
            'content_data':content_data,
            'auxiliar_data':auxiliar_data
        }
        extra_id = db.tickets_workflow.insert(**extra_data)
        db.commit()
        response.flash=T('Ticket Processed')
        redirect(URL('tickets'))
#    form = SQLFORM(db.tickets)
    return dict(form=form)


@auth.requires_login()
def ticket_thread():
    try:
        user = auth.user.id
    except:
        redirect(URL('default','index'))
    ticket = request.vars.ticket
    service = request.vars.service
    if service is not None:
        service = int(service)
    area = request.vars.area
    db.tickets_workflow.register_time.writable = False
    db.tickets_workflow.user_req.default = user
    db.tickets_workflow.user_req.writable = False
    db.tickets_workflow.ticket.default = ticket
    db.tickets_workflow.ticket.writable = False
    ticket_grid = []
    if auth.has_membership(user_id=auth.user.id, role='root'):
        query = (db.tickets.id==ticket)
        ticket_grid = SQLFORM.grid(query, csv=False)
    form = SQLFORM.factory(db.tickets_workflow)
    query_workflow = (db.tickets_workflow.ticket==ticket)
    grid = SQLFORM.grid(query_workflow, create=False, deletable=False, editable=False, csv=True)
    if form.process().accepted:
        id = db.tickets_workflow.insert(**db.tickets_workflow._filter_fields(form.vars))
        response.flash=T('Thread Added')
        redirect(URL('tickets'))
    return dict(form=form, grid=grid, ticket_grid=ticket_grid, service=service)