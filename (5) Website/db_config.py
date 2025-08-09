from global_vars import local_password
def get_db_config(deployed):
    db_config = {}
    if deployed:
        db_config = {
            'user': 'root',
            'password': 'boundingthroughtime',
            'host': 'localhost',
            'port': 1234,
            'database': 'vgadatabase'
        }
    else:
        db_config = {
            'user': 'root',
            'password': local_password,
            'host': 'localhost',
            'port': 3306,
            'database': 'vgadatabase'
        }
    return db_config