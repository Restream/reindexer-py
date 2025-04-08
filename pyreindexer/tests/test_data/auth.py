USER_ROLES = ["data_read", "data_write", "db_admin", "owner"]

users_yml = '''
data_read:
    hash: data_read
    roles:
        *: data_read

data_write:
    hash: data_write
    roles:
        *: data_write

db_admin:
    hash: db_admin
    roles:
        *: db_admin

owner:
    hash: owner
    roles:
        *: owner
'''
