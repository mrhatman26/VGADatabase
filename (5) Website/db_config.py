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
            'password': 'Apple_my_Sauce8253',
            'host': 'localhost',
            'port': 3306,
            'database': 'vgadatabase'
        }
    return db_config