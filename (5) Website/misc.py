def pause(message=None):
    if message is None:
        input("(Press ENTER to continue)")
    else:
        input(message)

def get_new_table_id(cursor, table_name):
    cursor.execute("SELECT * FROM " + table_name)
    return len(cursor.fetchall())

def get_time(no_brackets=False):
    current_time = dt.datetime.now()
    if no_brackets is False:
        return str("\n[" + current_time.strftime("%Y.%m.%d at %H:%M:%S") + "]")
    else:
        return str(current_time.strftime("%Y.%m.%d at %H:%M:%S"))