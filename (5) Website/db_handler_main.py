import mysql.connector, re, traceback
from datetime import datetime
from db_config import *
from db_handler_links import *
from misc import get_new_table_id, pause, get_no_pages, get_total_items
from global_vars import deployed

#Games 
def game_get_id(game, cursor=None):
    try:
        no_cursor = False
        if cursor is None:
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
            no_cursor = True
        cursor.execute("SELECT game_id FROM table_games WHERE game_title = %s", (str(game),))
        fetch = cursor.fetchall()
        if no_cursor is None:
            cursor.close()
            database.close()
        if len(fetch) > 0:
            return fetch[0][0]
        else:
            return None
    except:
        return None
    
def game_get_name(game_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        print(game_id)
        cursor.execute("SELECT game_title FROM table_games WHERE game_id = %s", (game_id,))
        fetch = cursor.fetchall()
        if len(fetch) > 0:
            return fetch[0][0]
        else:
            return None
    except:
        return None
    
def game_get_selection(pid=None, no_results=10):
    games = []
    if pid is None:
        pid = 0
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT * FROM table_games INNER JOIN link_game_user ON table_games.game_id=link_game_user.game_id WHERE link_game_user.game_link_approved = 1 ORDER BY table_games.game_id DESC LIMIT %s, %s", (pid, no_results + 1,))
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
    no_pages = get_no_pages(statement, cursor, pid, no_results)
    total_games = get_total_items(statement, cursor)
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
    
def game_create_new(game_data, user_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        if game_data["game_aka"].isspace() or game_data["game_aka"] == "":
            game_data["game_aka"] = None
        if game_data["game_desc"].isspace() or game_data["game_desc"] == "":
            game_data["game_desc"] = None
        if dt.strptime(game_data["game_rdate"], "%Y/%m/%d") < dt.now():
            game_data["game_rstate"] = "Released"
        else:
            game_data["game_rstate"] = "Unreleased"
        cursor.execute("INSERT INTO table_games (game_title, game_aka, game_desc, game_rdate, game_rstate, game_url) VALUES (%s, %s, %s, %s, %s, %s)", (game_data["game_title"], game_data["game_aka"], game_data["game_desc"], game_data["game_rdate"], game_data["game_rstate"], None))
        database.commit()
        game_add_user_link(game_get_id(game_data["game_title"]), user_id, database, cursor)
        cursor.close()
        database.close()
        return True
    except:
        return False
    
def game_get_unapproved():
    try:
        games = []
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT table_games.game_id, table_games.game_title, table_games.game_rdate FROM table_games INNER JOIN link_game_user ON table_games.game_id=link_game_user.game_id WHERE link_game_user.game_link_approved = 0 AND link_game_user.game_denied = 0")
        fetch = cursor.fetchall()
        for game in fetch:
            games.append({
                "game_id": game[0],
                "game_title": game[1],
                "game_rdate": game[2],
            })
        cursor.close()
        database.close()
        return games
    except Exception as e:
        print(e)
        pause()
        return None

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
    
#Devpub (Developers AND Publishers()
def devpub_get_id(devpub, is_pub=False, database=None, cursor=None):
    try:
        no_cursor = False
        if cursor is None or database is None:
            no_cursor = True
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
        cursor.execute("SELECT developer_id FROM table_developers WHERE developer_name = %s AND developer_isPub = %s", (devpub, is_pub,))
        fetch = cursor.fetchall()
        if no_cursor is True:
            cursor.close()
            database.close()
        if len(fetch) > 0:
            return fetch[0][0]
        else:
            return None
    except:
        return None

def devpub_check_exists(devpub, is_pub=False, database=None, cursor=None):
    try:
        no_cursor = False
        if cursor is None or database is None:
            no_cursor = True
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
        cursor.execute("SELECT developer_id FROM table_developers WHERE developer_name = %s AND developer_isPub = %s", (devpub, is_pub,))
        fetch = cursor.fetchall()
        if no_cursor is True:
            cursor.close()
            database.close()
        if len(fetch) > 0:
            return True
        else:
            return False
    except:
        return False

def devpub_add_new(devpub_data, user_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        devpub_data["developer_status"] = "Unknown"
        devpub_data["developer_isPub"] = bool(devpub_data["developer_isPub"])
        #Check description
        if devpub_data["developer_desc"].isspace() is True or devpub_data["developer_desc"] == "":
            devpub_data["developer_desc"] = None
        #Check founding date
        if devpub_data["developer_foundDate"].isspace() is True or devpub_data["developer_foundDate"] == "":
            devpub_data["developer_foundDate"] = None
            devpub_data["developer_status"] = "Unknown"
        else:
            if dt.strptime(devpub_data["developer_foundDate"], "%Y/%m/%d") > dt.now():
                devpub_data["developer_status"] = "Open for Business"
        #Check defunct date
        if devpub_data["developer_defunctDate"].isspace() is True or devpub_data["developer_defunctDate"] == "":
            devpub_data["developer_defunctDate"] = None
        else:
            if dt.strptime(devpub_data["developer_foundDate"], "%Y/%m/%d") > dt.now():
                devpub_data["developer_status"] = "Defunct"
        cursor.execute("INSERT INTO table_developers (developer_name, developer_desc, developer_foundDate, developer_status, developer_defunctDate, developer_isPub) VALUES (%s, %s, %s, %s, %s, %s)", (devpub_data["developer_name"], devpub_data["developer_desc"], devpub_data["developer_foundDate"], devpub_data["developer_status"], devpub_data["developer_defunctDate"], devpub_data["developer_isPub"],))
        database.commit()
        devpub_data["developer_id"] = devpub_get_id(devpub_data["developer_name"], devpub_data["developer_isPub"])
        devpub_add_user_link(devpub_data["developer_id"], user_id, database=database, cursor=cursor)
        database.commit()
        cursor.close()
        database.close()
        return True
    except Exception as e:
        print(traceback.format_exc())
        pause()
        return False

def devpub_get_selection(pid=None, no_results=10):
    devpubs = []
    if pid is None:
        pid = 0
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    cursor.execute("SELECT * FROM table_developers INNER JOIN link_developer_user ON table_developers.developer_id=link_developer_user.developer_id WHERE link_developer_user.developer_link_approved = 1 ORDER BY table_developers.developer_id DESC LIMIT %s, %s", (pid, no_results + 1))
    fetch = cursor.fetchall()
    import pyperclip
    pyperclip.copy(str(cursor.statement))
    for developer in fetch:
        devpubs.append({
            "developer_id": developer[0],
            "developer_name": developer[1],
            "developer_desc": developer[2],
            "developer_foundDate": developer[3],
            "developer_status": developer[4],
            "developer_defunctDate": developer[5],
            "developer_isPub": developer[6]
        })
    statement = cursor.statement
    no_pages = get_no_pages(statement, cursor, pid, no_results)
    total_devpubs = get_total_items(statement, cursor)
    cursor.close()
    database.close()
    return (devpubs, no_pages, total_devpubs)

#Languages
def language_check_exists(language):
    try:
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
    except:
        return False