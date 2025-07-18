import mysql.connector
from db_config import *
from misc import get_new_table_id, pause
from global_vars import deployed

#Games 
def game_get_id(game, cursor=None):
    if cursor is None:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
    cursor.execute("SELECT game_id FROM table_games WHERE game_title = %s", (str(game),))
    fetch = cursor.fetchall()
    if cursor is None:
        cursor.close()
        database.close()
    if len(fetch) > 0:
        return fetch[0][0]
    else:
        return None
    
def game_get_all(gid=None):
    if gid is None:
        gid = 0
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT game_title, game_aka, game_desc, game_rdate, game_rstate, game_url FROM table_games ORDER BY game_id DESC LIMIT %s, 11" (str(gid),))
    for game in cursor.fetchall():
        print(game)
        print(type(game))
        pause()
    cursor.close()
    database.close()

#Tags
def tag_check_exists(tag, cursor=None):
    if cursor is None:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
    cursor.execute("SELECT tag_id FROM table_tags WHERE tag_name = %s", (str(tag),))
    fetch = cursor.fetchall()
    if cursor is None:
        cursor.close()
        database.close()
    if len(fetch) > 0:
        return True
    else:
        return False
    
def tag_get_id(tag, cursor=None):
    if cursor is None:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
    cursor.execute("SELECT tag_id FROM table_tags WHERE tag_name = %s", (str(tag),))
    fetch = cursor.fetchall()
    if cursor is None:
        cursor.close()
        database.close()
    if len(fetch) > 0:
        return fetch[0][0]
    else:
        return None
    
#Aliases
def alias_check_exists(alias):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT alias_id FROM table_aliases WHERE alias_name = %s", (str(alias),))
    fetch = cursor.fetchall()
    cursor.close()
    database.close()
    if len(fetch) > 0:
        return True
    else:
        return False
    
def alias_get_id(alias):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT alias_id FROM table_aliases WHERE alias_name = %s", (str(alias),))
    fetch = cursor.fetchall()
    cursor.close()
    database.close()
    if len(fetch) > 0:
        return fetch[0]
    else:
        return None
    
#Genres
def genre_check_eixsts(genre, cursor=None):
    if cursor is None:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
    cursor.execute("SELECT genre_id FROM table_genres WHERE genre_name = %s", (str(genre),))
    fetch = cursor.fetchall()
    if cursor is None:
        cursor.close()
        database.close()
    if len(fetch) > 0:
        return True
    else:
        return False

def genre_get_id(genre, cursor=None):
    if cursor is None:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
    cursor.execute("SELECT genre_id FROM table_genres WHERE genre_name = %s", (str(genre),))
    fetch = cursor.fetchall()
    if cursor is None:
        cursor.close()
        database.close()
    if len(fetch) > 0:
        return fetch[0][0]
    else:
        return None

#Developers
def developer_check_exists(developer, cursor=None):
    if cursor is None:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
    cursor.execute("SELECT developer_id FROM table_developers WHERE developer_name = %s AND developer_isPub = 0", (str(developer),))
    fetch = cursor.fetchall()
    if cursor is None:
        cursor.close()
        database.close()
    if len(fetch) > 0:
        return True
    else:
        return False
    
def developer_get_id(developer, cursor=None):
    if cursor is None:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
    cursor.execute("SELECT developer_id FROM table_developers WHERE developer_name = %s AND developer_isPub = 0", (str(developer),))
    fetch = cursor.fetchall()
    if cursor is None:
        cursor.close()
        database.close()
    if len(fetch) > 0:
        return fetch[0][0]
    else:
        return None
    
#Publisher (Note: Publishers are developers in the database, but with developer_isPub set to True)
def publisher_check_exists(publisher, cursor=None):
    if cursor is None:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
    cursor.execute("SELECT developer_id FROM table_developers WHERE developer_name = %s AND developer_isPub = 1", (str(publisher),))
    fetch = cursor.fetchall()
    if cursor is None:
        cursor.close()
        database.close()
    if len(fetch) > 0:
        return True
    else:
        return False
    
def publisher_get_id(publisher):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT developer_id FROM table_aliases WHERE developer_name = %s AND developer_isPub = 1", (str(publisher),))
    fetch = cursor.fetchall()
    cursor.close()
    database.close()
    if len(fetch) > 0:
        return fetch[0]
    else:
        return None

#Languages
def language_check_exists(language):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT lang_id FROM table_languages WHERE lang_name = %s", (str(language),))
    fetch = cursor.fetchall()
    cursor.close()
    database.close()
    if len(fetch) > 0:
        return True
    else:
        return False