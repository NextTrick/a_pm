# -*- coding: utf-8 -*-
import socket

hostname = socket.gethostname()
#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    # db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
    db = DAL('mysql://integracion:y2KItelvox14@localhost/sige', pool_size=1, check_reserved=['all'], migrate=False)
    db2 = DAL('mysql://integracion:y2KItelvox14@localhost/integracion', pool_size=1, check_reserved=['all'],
              migrate=False)
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
import datetime
import types

auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()
now = datetime.datetime.now()

## create all tables needed by auth if not custom tables
# auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
# mail.settings.server = 'logging' or 'smtpout.secureserver.net'
# mail.settings.sender = 'soporte@itelvox.com'
# mail.settings.login = 'soporte@itelvox.com:fvp3LJql1'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True
auth.settings.login_next = URL('index')

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain

use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login
mail.settings.tls = False

account_types = {
    0: T('Prepaid'),
    1: T('Postpaid')
}

# payment_kinds = {
#     0: T('Payment'),
#     1: T('Detraction')
# }


status_options = {
    0: T('Active'),
    1: T('Inactive')
}

credits_options = {
    0: T('Pendent'),
    1: T('Active'),
    2: T('Cancel'),
}

credits_types = {
    1: T('Charge'),
    2: T('Debit'),
}

invoices_options = {
    0: T('Created'),
    1: T('Delivery Pendent'),
    2: T('Generation Pendent')
}

invoices_status = {
    0: T('Pendent'),
    1: T('Paid'),
    2: T('Void')
}

status_tickets = {
    0: T('Open'),
    1: T('In Progress'),
    2: T('Closed')
}

notifications_kinds = {
    1: T('Pre'),
    2: T('Post'),
    3: T('Auto'),
    4: T('Balance')
}
# ticket_kinds = {
#     0: T('Sales'),
#     1: T('Billing'),
#     2: T('Support')
# }

# invoice_types = {
#     0: T('Boleta'),
#     1: T('Factura')
# #    2: T('Ticket'),
# }

priority_options = {
    0: T('Normal'),
    1: T('Urgent'),
    2: T('Critical'),
}

calling_status = {
    0: T('NULL'),
    1: T('Dialing'),
    2: T('Ringing'),
    3: T('Answered'),
}

services_options = {
    0: T('DID'),
    1: T('Retail IP Telephony'),
    2: T('Wholesale IP Telephony'),
    3: T('Cloud PBX'),
    4: T('Dedicated Servers'),
    5: T('Massive IVR'),
    6: T('Massive SMS'),
    7: T('E-mail Marketing'),
    8: T('Others'),
}

db.define_table('commercial_documents',
                Field('name', 'string', label=T('Name')),
                Field('serial', 'string', label=T('Serial')),
                Field('correlative', 'integer', label=T('Correlative')),
                Field('electronic', 'boolean', label=T('Electronic')),
                format='%(name)s')

db.define_table('roles',
                Field('name', 'string', label=T('Name')),
                format='%(name)s')

db.define_table('payment_means',
                Field('name', 'string', label=T('Name')),
                format='%(name)s')

db.define_table('payment_methods',
                Field('name', 'string', label=T('Name')),
                format='%(name)s')

db.define_table('banks',
                Field('name', 'string', label=T('ame')),
                format='%(name)s')

db.define_table('bank_account_types',
                Field('name', 'string', label=T('Name')),
                Field('discount', 'boolean', label=T('Discount')),
                format='%(name)s')

db.define_table('payment_kinds',
                Field('name', 'string', label=T('Name')),
                Field('percentage', 'float', label=T('Percentage'),
                      default=0),
                Field('detraction', 'boolean', label=T('Detraction')),
                Field('amount_applied', 'float', label=T('Applied Amount'),
                      default=0),
                format='%(name)s')

db.define_table('billing_periods',
                Field('name', 'string', label=T('Name')),
                Field('days', 'integer', default=0, label=T('Days Cycle'),
                      comment=T('Days')),
                Field('months', 'integer', default=0, label=T('Months Cycle'),
                      comment=T('Months')),
                Field('due_days', 'integer', default=0, label=T('Due Days'),
                      comment=T('Days')),
                format='%(name)s')

db.define_table('areas',
                Field('name', 'string', label=T('Name')),
                Field('email', 'string', label=T('Email')),
                format='%(name)s')

db.define_table('mail_notifications',
                Field('subject', 'string', label=T('Subject')),
                Field('content_message', 'text', label=T('Message')),
                Field('days', 'integer', label=T('Days')),
                Field('kind', 'integer', label=T('Kind'),
                      requires=IS_IN_SET(notifications_kinds)),
                format='%(id)s')

db.define_table('business_areas',
                Field('name', 'string', label=T('Name')),
                format='%(name)s')

db.define_table('services_classes',
                Field('name', 'string', label=T('Name')),
                format='%(name)s')

db.define_table('countries',
                Field('name', 'string', label=T('Name')),
                Field('short_name', 'string', label=T('Short Name')),
                format='%(short_name)s')

db.define_table('cities',
                Field('country', 'reference countries', label=T('Country')),
                Field('name', 'string', label=T('Name')),
                Field('short_name', 'string', label=T('Short Name')),
                format='%(name)s')

db.define_table('services_invoices_descriptions',
                Field('service', 'integer', label=T('Service'),
                      requires=IS_IN_SET(services_options)),
                Field('name', 'string', label=T('Name')),
                format='%(name)s')

db.define_table('services_servers',
                Field('service_class', 'reference services_classes',
                      label=T('Class')),
                Field('name', 'string', label=T('Name')),
                Field('alternate_name', 'string',
                      label=T('Alternate Name / Code')),
                Field('host_ip', 'string', label=T('IP')),
                Field('database_ip', 'string', label=T('DataBase IP')),
                Field('port', 'string', label=T('Port')),
                Field('model', 'string', label=T('Database')),
#               Field('account', 'string', label=T('User')),
#               Field('password', 'string', label=T('Password')),
#               Field('sync_time', 'integer', label=T('Sync Time')),
                Field('status', 'integer', label=T('Status'), default=0,
                      requires=IS_IN_SET(status_options)),
                format='%(name)s - %(host_ip)s')

db.define_table('currencies',
                Field('name', label=T('Name')),
                Field('symbol', label=T('Symbol')),
                format='%(name)s')

db.define_table('currencies_exchange_rates',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now),
                Field('currency', 'reference currencies',
                      label=T('Currency'), writable=False, readable=False),
                Field('rate', 'float', label=T('Rate'), default=0),
                Field('destination_currency', db.currencies,
                      label=T('Converted Currency')),
                format='%(currency)s')

db.define_table('tariffs_integrated',
                Field('id_tariff', label=T('Tariff')),
                Field('code_prefix', label=T('Prefix')),
                Field('description', label=T('Description')),
                Field('voice_rate', label=T('Rate')),
                format='%(id_tariff)s', migrate=False)

db.define_table('registered_users',
                Field('login_account', label=T('Login')),
                Field('client_type', label=T('Client Type')),
                Field('registration_time', label=T('Registration Time')),
                Field('ip_address', label=T('Ip Address')),
                Field('server_id', label=T('Server')),
                format='%(id)s', migrate=False)

db.define_table('packages',
                Field('service', 'integer', label=T('Service'),
                      requires=IS_IN_SET(services_options)),
                Field('name', 'string', label=T('Name')),
                Field('alternate_name', 'string', label=T('Alternate Name')),
                Field('description', 'text', label=T('Description')),
                Field('currency', 'reference currencies', label=T('Currency')),
                Field('tariff_code', 'integer', label=T('Tariff Code')),
                Field('setup_fee', 'float', label=T('Setup Fee'), default=0),
                Field('monthly_fee', 'float', label=T('Monthly Fee'), default=0),
                Field('status', 'integer', label=T('Status'), default=0,
                      requires=IS_IN_SET(status_options)),
                format='%(name)s')

db.define_table('customers',
                Field('register_time', 'datetime', label=T('Register'),
                      default=now, writable=False),
                Field('name', 'string', label=T('Commercial Name')),
                Field('legal_name', 'string', label=T('Legal Name')),
                Field('tax_id', 'string', label=T('Tax ID')),
                Field('activity_start', 'date', label=T('Activity Start')),
                Field('web_url', 'string', label=T('Web URL')),
                #                Field('legal_representative', 'string', label=T('Legal Representative')),
                Field('electronic_file', 'string', label=T('Electronic File')),
                #                Field('currency', 'reference currencies', label=T('Currency')),
                Field('account_type', 'integer', label=T('Account Type'),
                      default=0, requires=IS_IN_SET(account_types)),
                Field('business_area', db.business_areas, label=T('Business Area'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.business_areas, '%(name)s'))),
                Field('currency', db.currencies, label=T('Currency'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.currencies, '%(name)s'))),
                Field('payment_mean', db.payment_means, label=T('Payment Mean'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.payment_means, '%(name)s'))),
                Field('payment_method', db.payment_methods, label=T('Payment Method'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.payment_methods, '%(name)s'))),
                Field('commercial_document', db.commercial_documents, label=T('Commercial Document'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.commercial_documents, '%(name)s'))),
                Field('tax', 'boolean', label=T('Tax')),
                Field('test', 'boolean', label=T('Test')),
                Field('status', 'integer', label=T('Status'),
                      default=0, requires=IS_IN_SET(status_options)),
                format='%(name)s')

auth.settings.extra_fields['auth_user'] = [
    Field('phone', label=T('Phone')),
    Field('customer', db.customers, label=T('Customer'),
          requires=IS_EMPTY_OR(IS_IN_DB(db, db.customers, '%(name)s'))),
]

auth.define_tables(username=False, signature=False)

db.define_table('accounts',
                Field('server_id', label=T('Server')),
                Field('account', label=T('Account')),
##                Field('id_client', label=T('ID Client')),
                Field('id_currency', 'reference currencies',
                      label=T('Currency')),
##                Field('id_tariff', label=T('Tariff')),
                Field('account_state', label=T('Balance')),
                Field('tax_id', label=T('Taxes')),
                Field('client_type', label=T('Client Type')),
                Field('invoice_type', label=T('Invoice Type')),
                Field('sip_proxy', label=T('Proxy')),
                Field('customer', 'reference customers', label=T('Customer')),
                Field('seller', label=T('Seller')),
                format='%(id_call)s', migrate=False)

db.define_table('sellers',
                Field('name', 'string', label=T('Name')),
                Field('full_name', 'string', label=T('Full Name')),
                Field('document_id', 'string', label=T('ID')),
                Field('related_user', db.auth_user, label=T('Related User'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.auth_user, '%(email)s'))),
                format='%(name)s')

db.define_table('customers_sellers',
                Field('customer', 'reference customers', label=T('Customer')),
                Field('seller', 'reference sellers', label=T('Seller')),
                format='%(id)s')

db.define_table('customers_addresses',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('customer', 'reference customers', label=T('Customer')),
                Field('name', 'string', label=T('Name')),
                Field('address', 'string', label=T('Address')),
                Field('reference', 'string', label=T('Reference')),
                Field('country', 'string', label=T('Country')),
                Field('tax_address', 'boolean', label=T('Tax Address')),
                Field('main_phone', 'string', label=T('Main Phone')),
                Field('priority', 'integer', default=1, label=T('Position')),
                format='%(name)s')

db.define_table('customers_contacts',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('customer', 'reference customers',
                      label=T('Customer')),
                Field('area', 'string', label=T('Area')),
                Field('role', db.roles, label=T('Role'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.roles, '%(name)s'))),
                Field('document_id', 'string', label=T('DNI')),
                Field('name', 'string', label=T('Full Name')),
                #                Field('phone', 'string', label=T('Phone')),
                Field('email', 'string', label=T('Email')),
                Field('skype', 'string', label=T('Skype')),
                Field('facebook', 'string', label=T('Facebook')),
                Field('twitter', 'string', label=T('Twitter')),
                Field('linkedin', 'string', label=T('Linkedin')),
                Field('annotation', 'text', label=T('Annotation')),
                Field('main', 'boolean', label=T('Legal Representative')),
                Field('notification', 'boolean', label=T('Notification')),
                format='%(name)s')

db.define_table('customers_contacts_phones',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('customer_contact', 'reference customers_contacts',
                      label=T('Contact')),
                Field('name', 'string', label=T('Name')),
                Field('phone', 'string', label=T('Phone')),
                Field('extension', 'string', label=T('Extension')),
                Field('main', 'boolean', label=T('Main')),
                format='%(name)s')

db.define_table('customers_contracts',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('customer', 'reference customers', label=T('Customer')),
                Field('service', 'integer', label=T('Service'),
                      requires=IS_IN_SET(services_options)),
                Field('name', 'string', label=T('Name')),
                Field('start_date', 'date', label=T('Start Date')),
                Field('end_date', 'date', label=T('End Date')),
                Field('billing_period', 'reference billing_periods',
                      label=T('Billing Period')),
                Field('archive', 'upload', label=T('Archive')),
                Field('annotation', 'text', label=T('Annotation')),
                format='%(name)s')

db.define_table('customers_contracts_documents',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('customer_contract', 'reference customers_contracts',
                      label=T('Contract')),
                Field('name', 'string', label=T('Name')),
                Field('archive', 'upload', label=T('Archive')),
                Field('annotation', 'text', label=T('Annotation')),
                format='%(name)s')

db.define_table('customers_rates',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('customer', 'reference customers', label=T('Customer')),
                Field('service', 'integer', label=T('Service'),
                      requires=IS_IN_SET(services_options)),
                Field('package', db.packages,
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.packages, '%(name)s'))),
                Field('name', 'string', label=T('Name')),
                Field('rate', 'float', label=T('Rate'), default=0),
                Field('annotation', 'text', label=T('Annotation')),
                format='%(name)s')

db.define_table('customers_services',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('customer', 'reference customers', label=T('Customer')),
                Field('customer_contract', db.customers_contracts, label=T('Contract'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.customers_contracts, '%(name)s'))),
                Field('service', 'integer', label=T('Service'),
                      requires=IS_IN_SET(services_options)),
                Field('seller', db.sellers, label=T('Seller'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.sellers, '%(name)s'))),
                Field('package', 'reference packages', label=T('Package')),
                #                Field('name', 'string', label=T('Name')),
                Field('start_date', 'date', label=T('Start Date')),
                Field('end_date', 'date', label=T('End Date')),
                Field('billing_period', 'reference billing_periods',
                      label=T('Billing Period')),
                Field('currency', db.currencies, label=T('Currency'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.currencies, '%(name)s'))
                      ),
                Field('setup', 'float', label=T('SetUp'), default=0),
                Field('monthly', 'float', label=T('Monthly'), default=0),
                Field('country', db.countries, label=T('Country'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.countries, '%(name)s'))),
                Field('city', db.cities, label=T('City'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.cities, '%(name)s'))),
                Field('did', 'string', label=T('DID')),
                Field('account', 'string', label=T('Account')),
                Field('password', 'string', label=T('Password')),
                Field('server_host', 'string', label=T('Server Host')),
                Field('server_port', 'string', label=T('Server Port')),
                Field('details', 'text', label=T('Details')),
                Field('test', 'boolean', label=T('Test')),
                Field('status', 'integer', label=T('Status'), default=0,
                      requires=IS_IN_SET(status_options)),
                format='%(service)s-%(id)s')

db.define_table('customers_credits',
                Field('register_time', 'datetime', label=T('Date'),
                      default=now, writable=False),
                Field('credit_type', 'integer', label=T('Type'), default=1,
                      requires=IS_IN_SET(credits_types)),
                Field('customer', 'reference customers', label=T('Customer')),
                Field('service', 'integer', label=T('Service'),
                      requires=IS_IN_SET(services_options)),
                Field('currency', 'reference currencies', label=T('Currency')),
                Field('amount', 'float', label=T('Amount')),
                Field('customer_amount', 'float', default=0,
                      label=T('Customer Amount')),
                Field('credit_reference', 'integer', label=T('Reference')),
                Field('login_reference', 'string', label=T('Account')),
                Field('notes', 'string', label=T('Description')),
                Field('status_time', 'datetime', label=T('Status Time'),
                      default=now, writable=False),
                Field('condition_status', 'integer', label=T('Condition'),
                      default=2, requires=IS_IN_SET(invoices_options)),
                Field('serial', 'string', label=T('Serial'), writable=False),
                Field('correlative', 'integer', label=T('Correlative'), writable=False),
                Field('status', 'integer', label=T('Status'), default=0,
                      requires=IS_IN_SET(credits_options)),
                Field('seller', 'reference sellers', label=T('Seller')),
                format='%(id)s')

# db.define_table('customers_charges',
#                 Field('register_time', 'datetime', label=T('Date'),
#                       default=now, writable=False),
#                 Field('customer', 'reference customers', label=T('Customer')),
#                 Field('service', 'integer', label=T('Service'),
#                       requires=IS_IN_SET(services_options)),
#                 Field('currency', 'reference currencies', label=T('Currency')),
#                 Field('amount', 'float', label=T('Amount')),
#                 Field('customer_amount', 'float', default=0,
#                       label=T('Customer Amount')),
#                 Field('charge_reference', 'integer', label=T('Reference')),
#                 Field('login_reference', 'string', label=T('Account')),
#                 Field('notes', 'string', label=T('Description')),
#                 Field('status_time', 'datetime', label=T('Status Time'),
#                       default=now, writable=False),
#                 Field('status', 'integer', label=T('Status'), default=0,
#                       requires=IS_IN_SET(credits_options)),
#                 format='%(id)s')


db.define_table('invoices',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('commercial_document', 'reference commercial_documents',
                      label=T('Document')),
                Field('serial', 'string', label=T('Serial')),
                Field('correlative', 'string', label=T('Correlative')),
                Field('invoice_date', 'date', label=T('Date'), default=now),
                Field('invoice_due', 'date', label=T('Due Date'), default=now),
                Field('customer', 'reference customers', label=T('Customer')),
                Field('customer_address', 'reference customers_addresses', label=T('Address')),
                Field('start_time', 'date', label=T('Starting Period')),
                Field('end_time', 'date', label=T('Ending Period')),
                #                Field('service', 'integer', label=T('Service'), requires=IS_IN_SET(services_options)),
                Field('currency', 'reference currencies', label=T('Currency')),
                Field('sub_total', 'float', label=T('Sub Total')),
                Field('discount', 'float', label=T('Discount'), default=0),
                Field('gran_total', 'float', label=T('Gran Total')),
                Field('tax', 'float', label=T('Tax')),
                Field('notes', 'string', label=T('Observations')),
                Field('condition_status', 'integer', label=T('Condition'),
                      default=0, requires=IS_IN_SET(invoices_options)),
                Field('void_reason', 'string', label=T('Void Reason')),
                Field('status', 'integer', label=T('Status'), default=0,
                      requires=IS_IN_SET(invoices_status)),
                Field('deliver_date', 'date', label=T('Deliver Date'),
                      default=now),
                format='%(serial)s-%(correlative)s')

db.define_table('invoices_details',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('invoice', 'reference invoices', label=T('Invoice')),
                Field('customer_service', 'reference customers_services',
                      label=T('Customer Service')),
                Field('start_time', 'date', label=T('Start Time')),
                Field('end_time', 'date', label=T('End Time')),
                Field('sub_total', 'float', label=T('Sub Total')),
                Field('discount', 'float', label=T('Discount'), default=0),
                #                Field('service', 'integer', label=T('Service'), requires=IS_IN_SET(services_options)),
                Field('notes', 'string', label=T('Notes')),
                Field('status', 'integer', label=T('Status'), default=0,
                      requires=IS_IN_SET(invoices_status)),
                format='%(id)s')

db.define_table('invoices_collection',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('invoice', 'reference invoices', label=T('Invoice')),
                Field('payment_date', 'date', label=T('Date'), default=now),
                Field('kind', 'reference payment_kinds', label=T('Kind')),
                Field('amount', 'float', label=T('Amount')),
                Field('notes', 'string', label=T('Notes')),
                Field('status', 'integer', label=T('Status'), default=0,
                      requires=IS_IN_SET(status_options)),
                format='%(id)s')

db.define_table('whitelist_destinations',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('customer_service', 'reference customers_services',
                      label=T('Customer Service')),
                Field('host_ip', 'string', label=T('Host IP')),
                Field('destination', 'string', label=T('Destination')),
                Field('notes', 'string', label=T('Notes')),
                Field('status', 'integer', label=T('Status'), default=0,
                      requires=IS_IN_SET(status_options)),
                format='%(id)s')

db.define_table('blacklist_destinations',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('customer_service', 'reference customers_services',
                      label=T('Customer Service')),
                Field('host_ip', 'string', label=T('Host IP')),
                Field('destination', 'string', label=T('Destination')),
                Field('notes', 'string', label=T('Notes')),
                Field('status', 'integer', label=T('Status'), default=0,
                      requires=IS_IN_SET(status_options)),
                format='%(id)s')

db.define_table('services_hosts',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('customer_service', 'reference customers_services',
                      label=T('Customer Service')),
                Field('service_server', 'reference services_servers',
                      label=T('Service Server')),
                format='%(id)s')

db.define_table('providers',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('name', 'string', label=T('Name')),
                Field('commercial_name', 'string', label=T('Commercial Name')),
                Field('tax_id', 'string', label=T('Tax ID')),
                Field('web_url', 'string', label=T('Web URL')),
                Field('GMT', 'integer', label=T('GMT')),
                # Field('legal_representative', 'string', label=T('Legal Representative')),
                # Field('document_id_representative', 'string', label=T('DNI Representative')),
                # Field('electronic_file', 'string', label=T('Electronic File')),
                # Field('payment_mean', db.payment_means,
                #       requires=IS_EMPTY_OR(IS_IN_DB(db, db.payment_means, '%(name)s'))),
                # Field('payment_method', db.payment_methods,
                #       requires=IS_EMPTY_OR(IS_IN_DB(db, db.payment_methods, '%(name)s'))),
                # Field('invoice_type', 'integer', label=T('Invoice Type'), default=0, requires=IS_IN_SET(invoice_types)),
                Field('status', 'integer', label=T('Status'), default=0,
                      requires=IS_IN_SET(status_options)),
                format='%(name)s')

db.define_table('providers_addresses',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('provider', 'reference providers', label=T('Provider')),
                Field('name', 'string', label=T('Name')),
                Field('address', 'string', label=T('Address')),
                Field('reference', 'string', label=T('Reference')),
                Field('country', 'string', label=T('Country')),
                Field('main', 'boolean', label=T('Main')),
                format='%(name)s')

db.define_table('providers_contacts',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('provider', 'reference providers', label=T('Provider')),
                Field('name', 'string', label=T('Name')),
                Field('full_name', 'string', label=T('Full Name')),
                Field('area', 'string', label=T('Area')),
                Field('email', 'string', label=T('Email')),
                Field('annotation', 'text', label=T('Annotation')),
                format='%(name)s')

db.define_table('providers_contacts_phones',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('provider_contact', 'reference providers_contacts',
                      label=T('Contact')),
                Field('name', 'string', label=T('Name')),
                Field('phone', 'string', label=T('Phone')),
                Field('extension', 'string', label=T('Extension')),
                Field('main', 'boolean', label=T('Main')),
                format='%(name)s')

db.define_table('providers_banks',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('provider', 'reference providers', label=T('Provider')),
                Field('name', 'string', label=T('Name')),
                Field('bank_account_type', 'reference bank_account_types',
                      label=T('Account Kind')),
                Field('bank', 'reference banks', label=T('Bank')),
                Field('class_account', 'string', label=T('Class')),
                Field('code', 'string', label=T('Code')),
                Field('account_number', 'string', label=T('Account Number')),
                Field('priority', 'integer', label=T('Priority')),
                format='%(name)s')

db.define_table('providers_contracts',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('customer', 'reference providers', label=T('Provider')),
                Field('name', 'string', label=T('Name')),
                Field('start_date', 'date', label=T('Start Date')),
                Field('end_date', 'date', label=T('End Date')),
                Field('annotation', 'text', label=T('Annotation')),
                format='%(name)s')

db.define_table('providers_contracts_documents',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('provider_contract', 'reference providers_contracts',
                      label=T('Contract')),
                Field('name', 'string', label=T('Name')),
                Field('archive', 'upload', label=T('Archive')),
                Field('annotation', 'text', label=T('Annotation')),
                format='%(name)s')

db.define_table('services_configurations',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now, writable=False),
                Field('customer_service', 'reference customers_services',
                      label=T('Customer Service')),
                Field('service_server', 'reference services_servers',
                      label=T('Server')),
                Field('provider', db.providers, label=T('Proveedor'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.providers, '%(name)s'))),
                Field('billing_period', db.billing_periods, label=T('Billing Period'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.billing_periods, '%(name)s'))),
                Field('currency', db.currencies, label=T('Currency'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, db.currencies, '%(name)s'))),
                Field('rate_cost', 'float', label=T('Cost'), default=0),
                format='%(id)s')

db.define_table('tickets',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now),
                Field('customer', 'reference customers', label=T('Customer')),
                Field('area', 'reference areas', label=T('Area')),
                Field('service', 'integer', label=T('Service'),
                      requires=IS_IN_SET(services_options)),
                Field('user_req', 'reference auth_user', label=T('User')),
                Field('priority', 'integer', label=T('Priority'), default=0,
                      requires=IS_IN_SET(priority_options)),
                Field('brief', 'string', label=T('Brief')),
                Field('status', 'integer', label=T('Status'), default=0,
                      requires=IS_IN_SET(status_tickets)),
                format='%(id)s')

db.define_table('tickets_workflow',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now),
                Field('ticket', 'reference tickets', label=T('Ticket'),
                      writable=False, readable=False),
                Field('user_req', 'reference auth_user', label=T('User')),
                Field('content_data', 'text', label=T('Message')),
                Field('auxiliar_data', 'upload', label=T('Attachment'), uploadfolder=UPLOAD_PATH),
                format='%(ticket)s')

db.define_table('mail_queue',
                Field('register', 'datetime', label=T('Register Time'),
                      default=now),
                Field('email', label=T('E-mail')),
                Field('subject', label=T('Subject')),
                Field('content_message', label=T('Message')),
                Field('status', 'integer', label=T('Status')),
                format='%(id)s')

db.define_table('alerts',
                Field('register_time', 'datetime', label=T('Register Time'),
                      default=now),
                # Field('customer', 'reference customers', label=T('Customer')),
                Field('customer_service', 'reference customers_services',
                      label=T('Customer Service')),
                Field('amount', 'float', label=T('Amount')),
                format='%(id)s', migrate=False)

db.define_table('current_calls',
                Field('id_call', label=T('ID Call')),
                Field('account', label=T('Account')),
                Field('account_state', label=T('Credit')),
                Field('ani', label=T('Origin Number')),
                Field('dialed_number', label=T('Dialed Number')),
                Field('call_start', label=T('Start Time')),
                Field('duration', 'time', label=T('Duration')),
                Field('tariffdesc', label=T('Destination')),
                Field('route', label=T('Provider')),
                Field('call_state', label=T('State'),
                      requires=IS_IN_SET(calling_status)),
                Field('server_id', label=T('Server')),
                Field('seller', 'reference sellers', label=T('Seller')),
                format='%(id_call)s', migrate=False)

db.define_table('channels_customers',
                Field('data_time', 'datetime', label=T('Data Time')),
                Field('customer', 'reference customers', label=T('Customer')),
                Field('account', label=T('Account')),
                Field('provider', label=T('Provider')),
                Field('server_id', label=T('Server')),
                Field('seller', 'reference sellers', label=T('Seller')),
                Field('call_state', label=T('State'),
                      requires=IS_IN_SET(calling_status)),
                Field('channels', label=T('Channels')),
                format='%(id)s')

db.define_table('channels_providers',
                Field('data_time', 'datetime', label=T('Data Time')),
                Field('provider', label=T('Provider')),
                Field('server_id', label=T('Server')),
                Field('seller', 'reference sellers', label=T('Seller')),
                Field('call_state', label=T('State'),
                      requires=IS_IN_SET(calling_status)),
                Field('channels', label=T('Channels')),
                format='%(id)s')


db.accounts.account.requires = IS_NOT_IN_DB(db, 'accounts.account')
db.customers.tax_id.requires = IS_NOT_IN_DB(db, 'customers.tax_id')
db.customers_services.did.requires = IS_EMPTY_OR(IS_NOT_IN_DB(db, 'customers_services.did'))
db.customers.status.represent = lambda value, row: None if value is None else status_options[value]
db.customers.commercial_document.represent = lambda value, row: None if value is None else name_data(
    db.commercial_documents, value)
db.customers.business_area.represent = lambda value, row: None if value is None else name_data(db.business_areas, value)
db.customers.currency.represent = lambda value, row: None if value is None else name_data(db.currencies, value)
db.customers.payment_mean.represent = lambda value, row: None if value is None else name_data(db.payment_means, value)
db.customers.account_type.represent = lambda value, row: None if value is None else account_types[value]
db.customers_services.service.represent = lambda value, row: None if value is None else services_options[int(value)]
db.customers_services.currency.represent = lambda value, row: None if value is None else name_data(db.currencies, value)
db.customers_services.seller.represent = lambda value, row: None if value is None else name_data(db.sellers, value)
db.packages.service.represent = lambda value, row: None if value is None else services_options[int(value)]
db.auth_user.customer.represent = lambda value, row: None if value is None else name_data(db.customers, value)
db.tickets.area.represent = lambda value, row: None if value is None else name_data(db.areas, value)
db.tickets.service.represent = lambda value, row: None if value is None else services_options[int(value)]
db.tickets.status.represent = lambda value, row: None if value is None else status_tickets[value]
db.tickets.customer.represent = lambda value, row: None if value is None else name_data(db.customers, value)
db.tickets._after_update.append(lambda values, id: send_mail(values, id))
db.tickets_workflow._after_insert.append(lambda values, id: send_mail(values, id))
db.tickets_workflow.auxiliar_data.represent = lambda value, row: A(T('Download'), _href=URL('download', args=value))
# db.customers_services._after_insert.append(lambda values, id: update_rates(values, id))
# db.invoices_collection.invoice.represent = lambda value, row: None if value is None else name_data(db.invoices, value)
db.customers_credits.credit_type.represent = lambda value, row: None if value is None else credits_types[int(value)]
db.customers_credits.condition_status.represent = lambda value, row: None if value is None else invoices_options[
    int(value)]
db.customers_credits.status.represent = lambda value, row: None if value is None else credits_options[int(value)]
db.customers_credits._after_insert.append(lambda values, id: insert_rates(values, id))
# db.customers_credits._after_update.append(lambda values, id: prepaid_invoice(id, values))
# db.customers_charges.status.represent = lambda  value, row: None if value is None else credits_options[int(value)]
db.invoices.condition_status.represent = lambda value, row: None if value is None else invoices_options[value]
db.invoices.status.represent = lambda value, row: None if value is None else invoices_status[value]
db.invoices_details.customer_service.represent = lambda value, row: None if value is None else complex_data(value)
db.invoices_details.status.represent = lambda value, row: None if value is None else invoices_status[value]
db.invoices._after_update.append(lambda values, id: invoice_update(id, values))
