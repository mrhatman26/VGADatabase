def get_db_config(deployed):
    db_config = {}
    if deployed:
        db_config = {
            'user': 'root',
            'password': 'boundingthroughtime',
            'host': 'db',
            'database': 'VGDB'
        }
    else:
        db_config = {
            'user': 'root',
            'password': 'boundingthroughtime',
            'host': 'localhost',
            'port': 1234,
            'database': 'VGDB'
        }
    return db_config