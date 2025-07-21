import mysql.connector
from global_vars import deployed
from db_config import *
from misc import pause, get_new_table_id, get_time
from datetime import datetime as dt

#Games
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