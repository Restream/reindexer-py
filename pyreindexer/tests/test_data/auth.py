USER_ROLES = ["data_read", "data_write", "db_admin", "owner"]

users_yml = '''
data_read:
    hash: dataread
    roles:
        *: data_read

data_write:
    hash: datawrite
    roles:
        *: data_write

db_admin:
    hash: dbadmin
    roles:
        *: db_admin

owner:
    hash: owner
    roles:
        *: owner
'''
