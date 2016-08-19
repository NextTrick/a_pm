### we prepend t_ to tablenames and f_ to fieldnames for disambiguity
db.auth_group.update_or_insert(role='root')
#db.auth_group.update_or_insert(role='backoffice')
#db.auth_group.update_or_insert(role='support_chief')
#db.auth_group.update_or_insert(role='support')
#db.auth_group.update_or_insert(role='administration')
#db.auth_group.update_or_insert(role='direction')
db.auth_group.update_or_insert(role='sales')
db.auth_group.update_or_insert(role='users')

sales_group_id = db.auth_group(db.auth_group.role == 'sales')['id']
users_group_id = db.auth_group(db.auth_group.role == 'users')['id']

auth.settings.everybody_group_id = users_group_id
