def get_db_config(deployed):
    db_config = {}
    if deployed:
        db_config = {
            'user': 'root',
            'password': 'boundingthroughtime',
            'host': 'db',
            'database': 'vgadatabase'
        }
    else:
        db_config = {
            'user': 'root',
            'password': 'boundingthroughtime',
            'host': 'localhost',
            'port': 1234,
            'database': 'vgadatabase'
        }
    return db_config