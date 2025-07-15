import mysql.connector, hashlib
from db_config import *
from misc import get_new_table_id

deployed = False

def string_hash(text):
    text = text.encode('utf-8')
    hash = hashlib.sha256()
    hash.update(text)
    return hash.hexdigest()

#Checks
def user_check_exists(username):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT user_id FROM table_users WHERE user_name = %s", (str(username),))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return True
        else:
            return False
    except:
        return False

def user_check_reconfirm(user_id):
    user = []
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT user_id, user_name, user_isMod, user_isAdmin FROM table_users WHERE user_id = %s", (str(user_id),))
    for item in cursor.fetchall():
        user.append(item[0])
        user.append(item[1])
        user.append(item[2])
        user.append(item[3])
    cursor.close()
    database.close()
    return user
    
#Add/Modify
def user_add_new(new_userdata, set_mod=False, set_admin=False):
    try:
        if set_admin is True:
            set_mod = True
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        new_userdata["id"] = get_new_table_id(cursor, "table_users")
        new_userdata["user_password"] = string_hash(new_userdata["user_password"])
        cursor.execute("INSERT INTO table_users VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (str(new_userdata["id"]), new_userdata["user_name"], new_userdata["user_password"], new_userdata["user_email"], None, None, set_admin, set_mod,))
        database.commit()
        cursor.close()
        database.close()
        return True
    except Exception as e:
        print(str(e), flush=True)
        return False