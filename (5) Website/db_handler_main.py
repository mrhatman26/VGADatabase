import mysql.connector, re
from db_config import *
from misc import get_new_table_id, pause
from global_vars import deployed

#Games 
def game_get_id(game, cursor=None):
    try:
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
    except:
        return None
    
def game_get_all(gid=None, no_pages=10):
    games = []
    if gid is None:
        gid = 0
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT * FROM table_games ORDER BY game_id DESC LIMIT %s, 11", (gid,))
    fetch = cursor.fetchall()
    for game in fetch:
        games.append({
            "game_id": game[0],
            "game_title": game[1],
            "game_aka": game[2],
            "game_desc": game[3],
            "game_rdate": game[4],
            "game_rstate": game[5],
            "game_url": game[6]
        })
    statement = cursor.statement
    no_pages = get_no_game_pages(statement, cursor, gid, no_pages)
    total_games = get_total_games(cursor.statement, cursor)
    cursor.close()
    database.close()
    return (games, no_pages, total_games)

def game_get_single(game_id=0):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT * FROM table_games WHERE game_id = %s", (game_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            fetch = fetch[0]
            game_data = {
                "game_id": fetch[0],
                "game_title": fetch[1],
                "game_aka": fetch[2],
                "game_desc": fetch[3],
                "game_rdate": fetch[4],
                "game_rstate": fetch[5],
                "game_url": fetch[6]
            }
            return game_data
        else:
            return None
    except:
        return None
    
def game_check_exists(game):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT * FROM table_games WHERE game_title = %s", (game,))
    fetch = cursor.fetchall()
    cursor.close()
    database.close()
    if len(fetch) > 0:
        return True
    else:
        return False
    
def game_create_new(game_data):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("INSERT INTO table_games (game_title, game_aka, game_desc, game_rdate, game_rstate, game_url) VALUES (%s, %s, %s, %s, %s, %s)", (game_data["game_title"], game_data["game_aka"], game_data["game_desc"], game_data["game_rdate"], None, None))
        database.commit()
        return True
    except:
        return False

def get_no_game_pages(command, cursor, gid, no_pages=10):
    command = re.sub("SELECT (.*?) FROM", "SELECT count(*) FROM", command)
    command = command.replace(str(gid) + ", ", "0 ,")
    cursor.execute(command)
    fetch = cursor.fetchall()[0][0]
    no_pages =  round(fetch / no_pages)
    if no_pages < 1 and fetch > 0:
        remander = fetch
    else:
        remander = fetch % no_pages
    if remander > 0:
        while True:
            remander -= 10
            no_pages += 1
            if remander < 1:
                break
    return no_pages

def get_total_games(command, cursor):
    command = re.sub("SELECT (.*?) FROM", "SELECT count(*) FROM", command)
    command = command.split(" ORDER")[0]
    cursor.execute(command)
    return cursor.fetchall()[0][0]

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