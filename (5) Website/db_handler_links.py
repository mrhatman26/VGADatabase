import mysql.connector
from global_vars import deployed
from db_config import *
from misc import pause, get_new_table_id, get_time
from datetime import datetime as dt

'''Games'''
#Add
def game_add_user_link(game_id, user_id, database=None, cursor=None):
    try:
        no_cursor = False
        if database is None or cursor is None:
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
            no_cursor = True
        cursor.execute("INSERT INTO link_game_user (game_id, user_id, game_cDate, game_link_approved, game_aDate) VALUES (%s, %s, %s, %s, %s)", (game_id, user_id, get_time(no_brackets=True), False, None,))
        database.commit()
        if no_cursor is True:
            cursor.close()
            database.close()
        return True
    except:
        return False
#Update    
def game_approve_user_link(game_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("UPDATE link_game_user SET game_link_approved = 1, game_aDate = %s", (get_time(no_brackets=True),))
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        return False
    
def game_deny_user_link(deny_data):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("UPDATE link_game_user SET game_denied = 1, game_dDate = %s, game_dDes = %s WHERE game_id = %s", (get_time(no_brackets=True), deny_data["denial_text"], deny_data["denial_game_id"],))
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        return False

#Get
def game_get_approved(game_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT * FROM link_game_user WHERE game_link_approved = 1 AND game_id = %s", (game_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return True
        else:
            return False
    except:
        return False
    
def game_get_denied(game_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT game_id FROM link_game_user WHERE game_id = %s AND game_denied = 1", (str(game_id),))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return True
        else:
            return False
    except:
        return False
    
def game_get_denial_reason(game_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT game_dDes FROM link_game_user WHERE game_id = %s AND game_denied = 1", (str(game_id),))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return fetch[0][0]
        else:
            return None
    except:
        return None