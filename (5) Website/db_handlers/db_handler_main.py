import mysql.connector
from db_config import *
from misc import get_new_table_id

deployed = False

def language_check_exists(language):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT lang_id FROM table_languages WHERE lang_name = %s", (str(language),))
    if len(cursor.fetchall()) > 0:
        return True
    else:
        return False