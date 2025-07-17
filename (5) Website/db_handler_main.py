import mysql.connector
from db_config import *
from misc import get_new_table_id

deployed = False

#Tags
def tag_check_exists(tag):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT tag_id FROM table_tags WHERE tag_name = %s", (str(tag),))
    fetch = cursor.fetchall()
    cursor.close()
    database.close()
    if len(fetch) > 0:
        return True
    else:
        return False
    
def tag_get_id(tag):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT tag_id FROM table_tags WHERE tag_name = %s", (str(tag),))
    fetch = cursor.fetchall()
    cursor.close()
    database.close()
    if len(fetch) > 0:
        return fetch[0]
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
def genre_check_eixsts(genre):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT genre_id FROM table_genres WHERE genre_name = %s", (str(genre),))
    fetch = cursor.fetchall()
    cursor.close()
    database.close()
    if len(fetch) > 0:
        return True
    else:
        return False

def genre_get_id(genre):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT genre_id FROM table_aliases WHERE genre_name = %s", (str(genre),))
    fetch = cursor.fetchall()
    cursor.close()
    database.close()
    if len(fetch) > 0:
        return fetch[0]
    else:
        return None

#Developers
def developer_check_exists(developer):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT developer_id FROM table_developers WHERE developer_name = %s AND developer_isPub = 0", (str(developer),))
    fetch = cursor.fetchall()
    cursor.close()
    database.close()
    if len(fetch) > 0:
        return True
    else:
        return False
    
'''def developer_add_game_link(developer_id, game_id, pre_approve=False):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("INSERT INTO link_game_developer VALUES(%s, %s, %s, %s, %s, %s, %s)", (str))'''
    
def developer_get_id(developer):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT developer_id FROM table_developers WHERE developer_name = %s AND developer_isPub = 0", (str(developer),))
    fetch = cursor.fetchall()
    cursor.close()
    database.close()
    if len(fetch) > 0:
        return fetch[0][0]
    else:
        return None
    
#Publisher (Note: Publishers are developers in the database, but with developer_isPub set to True)
def publisher_check_exists(publisher):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT developer_id FROM table_developers WHERE developer_name = %s AND developer_isPub = 1", (str(publisher),))
    fetch = cursor.fetchall()
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