import datetime as dt

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
    
def get_current_page(gid, no_results=10):
    current_page = 0
    if gid <= 0:
        return 0
    else:
        while True:
            if gid >= no_results:
                current_page += 1
                gid -= 10
            else:
                if gid > 0:
                    current_page += 1
                break
        return current_page
    
def test_datetime(date):
    try:
        dt.datetime.strptime(date, "%Y/%m/%d")
        return True
    except:
        return False