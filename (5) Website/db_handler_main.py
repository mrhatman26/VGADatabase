import mysql.connector
from db_config import *
from misc import get_new_table_id

deployed = False

#Tags
def tag_check_exists(tag):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT tag_id FROM table_tags WHERE tag_name = %s", (str(tag),))
    if len(cursor.fetchall()) > 0:
        return True
    else:
        return False
    
#Aliases
def alias_check_exists(alias):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT alias_id FROM table_aliases WHERE alias_name = %s", (str(alias),))
    if len(cursor.fetchall()) > 0:
        return True
    else:
        return False
    
#Genres
def genre_check_eixsts(genre):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT genre_id FROM table_genres WHERE genre_name = %s", (str(genre),))
    if len(cursor.fetchall()) > 0:
        return True
    else:
        return False

#Developers
def developer_check_exists(developer):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT developer_id FROM table_developers WHERE developer_name = %s AND developer_isPub = 0", (str(developer),))
    if len(cursor.fetchall()) > 0:
        return True
    else:
        return False
    
#Publisher (Note: Publishers are developers in the database, but with developer_isPub set to True)
def publisher_check_exists(publisher):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT developer_id FROM table_developers WHERE developer_name = %s AND developer_isPub = 1", (str(publisher),))
    if len(cursor.fetchall()) > 0:
        return True
    else:
        return False

#Languages
def language_check_exists(language):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT lang_id FROM table_languages WHERE lang_name = %s", (str(language),))
    if len(cursor.fetchall()) > 0:
        return True
    else:
        return False