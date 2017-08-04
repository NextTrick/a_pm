response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description

home = [(T('Home'), False, URL('default','index'), [])]

customer_home = [(T('Home'), False, URL('services','index'), [])]

internal_home = home

configuration = [
    (T('Configuration'), False, None,
     [
        (T('Basics'), False, None,[
            (T('Customers'), False, URL('config', 'customers'),[]),
            (T('Packages'), False, URL('config', 'packages'),[]),
            (T('Areas'), False, URL('config', 'areas'),[]),
            (T('Roles'), False, URL('config', 'roles'),[]),
            (T('Business Areas'), False, URL('config', 'business_areas'),[]),
            (T('Services Classes'), False, URL('config', 'services_classes'),[]),
            (T('Countries'), False, URL('config', 'countries'),[]),
            (T('Cities'), False, URL('config', 'cities'),[]),
            (T('Mail Notifications'), False, URL('config', 'mail_notifications'),[]),
        ]),
        (T('Commercial'), False, None,[
            (T('Currencies'),False,URL('config','currencies'),[]),
            (T('Billing Periods'),False,URL('config','billing_periods'),[]),
            (T('Payment Means'),False,URL('config','payment_means'),[]),
            (T('Payment Methods'),False,URL('config','payment_methods'),[]),
            (T('Payment Kinds'),False,URL('config','payment_kinds'),[]),
            (T('Commercial Documents'),False,URL('config','commercial_documents'),[]),
            (T('Banks'),False,URL('config','banks'),[]),
            (T('Banks Account Types'),False,URL('config','banks_account_types'),[]),
            (T('Services Descriptions'),False,URL('config','services_descriptions'),[]),
        ]),
        (T('Users'), False, None,[
            (T('Manage'),False,URL('config','users_manage'),[]),
            (T('Groups'),False,URL('config','users_groups'),[]),
            (T('Memberships'),False,URL('config','users_membership'),[]),
            (T('Sellers'),False,URL('config','sellers'),[]),
        ]),
     ]
    ),
]

network = [
    (T('Network'), False, None,
     [
         (T('VOIPSwitch Servers'), False, URL('network', 'ip_switch'),[]),
         (T('SMS Servers'), False, URL('network', 'sms'),[]),
         (T('SMTP Servers'), False, URL('network', 'smtp'),[]),
         (T('FTP Servers'), False, URL('network', 'ftp'),[]),
         (T('CACTI Servers'), False, URL('network', 'cacti'),[]),
#         (T('Extra Parameters'), False, URL('network', 'extra_parameters'),[]),
     ]
    ),
]

customers = [
    (T('Customers'), False, None,
     [
         (T('Control Panel'), False, URL('customer_service', 'customer'),[]),
         (T('Services'), False, URL('customer_service', 'service'),[]),
#         (T('Price List'), False, URL('customer_service', 'price_list'),[]),
         (T('Contracts'), False, URL('customer_service', 'contract'),[]),
     ]
    ),
]

providers = [
    (T('Providers'), False, None,
     [
         (T('Control Panel'), False, URL('providers', 'provider'),[]),
#         (T('Costs List'), False, URL('providers', 'price_list'),[]),
#         (T('Contracts'), False, URL('providers', 'contract'),[]),
     ]
    ),
]

# services = [
#     (T('Services'), False, None,
#      [
#          (T('DID'), False, None,[
#             (T('List'), False, URL('services', 'did_list'),[]),
#             (T('Rates'), False, URL('services', 'did_rates'),[]),
#             (T('Requests'), False, URL('services', 'did_requests'),[]),
#          ]),
#          (T('Retail IP Telephony'), False, URL('services', 'voip_accounts', vars=dict(service=1)),[
#             # (T('Whilelist'), False, URL('services', 'whitelist'),[]),
#             # (T('Blacklist'), False, URL('services', 'blacklist'),[]),
#             # (T('Information'), False, URL('services', 'voip_accounts'),[]),
#             # (T('Rates'), False, URL('services', 'retail_rates'),[]),
#             # (T('CDR'), False, URL('services', 'retail_cdr'),[]),
#             # (T('Reports'), False, URL('reports', 'retail_reports'),[]),
#          ]),
#          (T('Wholesale IP Telephony'), False, URL('services', 'voip_accounts', vars=dict(service=2)),[
#             # (T('Rates'), False, URL('services', 'wholesale_rates'),[]),
#             # (T('CDR'), False, URL('services', 'wholesale_cdr'),[]),
#             # (T('Reports'), False, URL('reports', 'wholesale_reports'),[]),
#          ]),
#          (T('Cloud PBX'), False, URL('services', 'cloud_pbx'),[]),
#          (T('Dedicated Servers'), False, None,[
#             (T('List'), False, URL('services', 'dedicated_list'),[]),
#             (T('Rates'), False, URL('services', 'dedicated_rates'),[]),
#             (T('Requests'), False, URL('services', 'dedicated_requests'),[]),
#          ]),
#          (T('Massive IVR'), False, URL('services', 'massive_ivr'),[]),
#          (T('Massive SMS'), False, URL('services', 'massive_sms'),[]),
#          (T('E-mail Marketing'), False, URL('services', 'email_marketing'),[]),
#      ]
#     ),
# ]

services = [(T('Services'), False, URL('services','service_list'), [])]

administrative = [
    (T('Administrative'), False, None,
     [
#         (T('Service Control'), False, URL('administrative', 'service_control'),[]),
#         (T('Pre Paid Control'), False, None,[
#             (T('Billing'), False, URL('administrative', 'pre_paid_billing'),[]),
#             (T('Reload'), False, URL('administrative', 'credits'),[]),
# #            (T('Charges'), False, URL('administrative', 'charges'),[]),
#         ]),
#         (T('Post Paid Control'), False, None,[
# #            (T('Automatic Billing'), False, URL('administrative', 'post_paid_automatic_billing'),[]),
#             (T('Billing'), False, URL('administrative', 'post_paid_billing'),[]),
# #            (T('Invoice Control'), False, URL('administrative', 'invoice_control'),[]),
#         ]),
        (T('Invoice Control'), False, None,[
            (T('Collection'), False, URL('administrative', 'collection'),[]),
            (T('Pendent Invoices'), False, URL('administrative', 'customer_balance'),[]),
#            (T('Invoice Control'), False, URL('administrative', 'invoice_control'),[]),
            (T('Invoice List'), False, URL('administrative', 'invoice_list'),[]),
        ]),
#         (T('Parameters'), False, URL('administrative', 'parameters'),[]),
        (T('Reports'), False, None,[
            (T('Graphics Reports'), False, URL('administrative', 'graphics'),[]),
            (T('CDR Reports'), False, URL('reports', 'cdr_reports'),[]),
            (T('Administrative Reports'), False, URL('reports', 'admin_reports'),[]),
        ]),
     ]
    ),
]

billing = [
    (T('Billing'), False, None,
     [
         (T('Service Control'), False, URL('administrative', 'service_control'),[]),
         (T('Pre paid'), False, URL('administrative', 'pre_paid_billing'),[]),
         (T('Post paid'), False, URL('administrative', 'post_paid_billing'),[]),
     ]
    ),
]

balance = [
    (T('Charges'), False, None,
     [
         (T('Request Charge'), False, URL('support', 'charge_new'),[]),
         (T('Reload'), False, URL('services', 'credits'),[]),
     ]
    ),
]


support = [
    (T('Support'), False, None,
     [
         (T('Tickets'), False, URL('support', 'tickets'),[]),
     ]
    ),
]

status = [
    (T('Status'), False, None,
     [
         (T('Accounts'), False, URL('reports', 'accounts'),[]),
         (T('VOIP Current Calls'), False, URL('reports', 'current_calls'),[]),
         (T('Registered Users'), False, URL('reports', 'registered_users'),[]),
     ]
    ),
]


profile = [
         (T('Profile'), False, URL('customer_service', 'profile'),[]),
#         (T('Add Funds'), False, URL('services', 'add_funds'),[]),
]



response.menu = home
#response.menu += services
if auth.user:
    user = auth.user.id
    customer = auth.user.customer
    try:
        customer_type = db.customers(db.customers.id==customer).account_type
    except:
        customer_type = None
    if auth.has_membership(user_id=auth.user.id, role='root'):
        response.menu += configuration
        response.menu += network
        response.menu += customers
        response.menu += providers
        #response.menu += services
        response.menu += administrative
        response.menu += billing
        response.menu += status
        response.menu += support
        response.menu += profile
    elif auth.has_membership(user_id=auth.user.id, role='customer'):
        response.menu = customer_home
        response.menu += profile
        if customer_type == 0:
            response.menu += balance
        response.menu += services
        response.menu += support
    elif auth.has_membership(user_id=auth.user.id, role='support'):
        response.menu += support
