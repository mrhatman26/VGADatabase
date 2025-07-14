def pause(message=None):
    if message is None:
        input("(Press ENTER to continue)")
    else:
        input(message)

def get_new_table_id(cursor, table_name):
    cursor.execute("SELECT * FROM " + table_name)
    return len(cursor.fetchall())