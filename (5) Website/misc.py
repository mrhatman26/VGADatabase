import datetime as dt, re, traceback

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
    
def get_current_page(pid, no_results=10):
    current_page = 0
    if pid <= 0:
        return 0
    else:
        while True:
            if pid >= no_results:
                current_page += 1
                pid -= no_results
            else:
                if pid > 0:
                    current_page += 1
                break
        return current_page
    
def test_datetime(date):
    try:
        dt.datetime.strptime(date, "%Y/%m/%d")
        return True
    except:
        return False
    
def get_no_pages(command, cursor, pid, no_results=10):
    command = re.sub("SELECT (.*?) FROM", "SELECT count(*) FROM", command)
    command = command.replace(str(pid) + ", ", "0 ,")
    cursor.execute(command)
    fetch = cursor.fetchall()[0][0]
    no_pages = 0
    if fetch <= 0:
        no_pages =  0
    else:
        while True:
            fetch -= no_results
            no_pages += 1
            if fetch < 1:
                break
    return no_pages

def get_total_items(command, cursor):
    command = re.sub("SELECT (.*?) FROM", "SELECT count(*) FROM", command)
    command = command.split(" ORDER")[0]
    cursor.execute(command)
    return cursor.fetchall()[0][0]