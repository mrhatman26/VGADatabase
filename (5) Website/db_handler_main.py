import mysql.connector, re, traceback
from datetime import datetime
from db_config import *
from db_handler_links import *
from db_handler_users import user_get_username
from misc import get_new_table_id, pause, get_no_pages, get_total_items, to_bool, fprint
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
        cursor.execute("SELECT game_title FROM table_games WHERE game_id = %s", (game_id,))
        fetch = cursor.fetchall()
        if len(fetch) > 0:
            return fetch[0][0]
        else:
            return None
    except:
        return None
    
def game_get_selection(pid=None, search=None, no_results=10):
    try:
        games = []
        if pid is None:
            pid = 0
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        if search == "":
            cursor.execute("SELECT * FROM table_games INNER JOIN link_game_user ON table_games.game_id=link_game_user.game_id WHERE link_game_user.game_link_approved = 1 ORDER BY table_games.game_id DESC LIMIT %s, %s", (pid, no_results + 1,))
            fetch = cursor.fetchall()
        else:
            search = re.sub(" +", " ", search)
            search = search.split("+")
            search_tags = []
            command_params = []
            for tag in search:
                if tag != "" and tag.isspace() is False:
                    tag_id = tag_get_id(tag, cursor=cursor)
                    search_tags.append(tag_id)
                    command_params.append(tag_id)
            command = "SELECT table_games.game_id, table_games.game_title, table_games.game_aka, table_games.game_desc, table_games.game_rdate, table_games.game_rstate, table_games.game_url" #Select
            command = command + " FROM table_games INNER JOIN link_game_tag ON table_games.game_id=link_game_tag.game_id INNER JOIN table_tags ON link_game_tag.tag_id=table_tags.tag_id" #Inner Join
            command = command + " WHERE table_tags.tag_id IN (%s" + (", %s" * (len(search_tags) - 1)) + ")" #Where
            command = command + " GROUP BY table_games.game_id" #Group
            command = command + " HAVING count(distinct table_tags.tag_id) = %s" #Having
            command = command + " ORDER BY table_games.game_id" #Order
            command = command + " DESC LIMIT %s, %s" #Limit
            command_params.append(len(search_tags))
            command_params.append(pid)
            command_params.append(no_results)
            command_params = tuple(command_params)
            cursor.execute(command, command_params)
            fetch = cursor.fetchall()
            statement = cursor.statement
            import pyperclip
            pyperclip.copy(statement)
            for game in fetch:
                    games.append({
                    "game_id": game[0],
                    "game_title": game[1].replace("_", " ").title(),
                    "game_aka": game[2],
                    "game_desc": game[3],
                    "game_rdate": game[4],
                    "game_rstate": game[5],
                    "game_url": game[6]
                })
            total_games = get_total_items(statement, cursor)
            no_pages = get_no_pages(cursor, pid, no_results, no_items=total_games)
            return (games, no_pages, total_games)
        for game in fetch:
            games.append({
                "game_id": game[0],
                "game_title": game[1].replace("_", " ").title(),
                "game_aka": game[2],
                "game_desc": game[3],
                "game_rdate": game[4],
                "game_rstate": game[5],
                "game_url": game[6]
            })
        statement = cursor.statement
        no_pages = get_no_pages(cursor, pid, no_results, command=statement)
        total_games = get_total_items(statement, cursor)
        cursor.close()
        database.close()
        return (games, no_pages, total_games)
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        import pyperclip
        statement = cursor.statement
        print(statement, flush=True)
        pyperclip.copy(statement)
        pause()
        return None

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
                "game_title": fetch[1].replace("_", " ").title(),
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
    game = game.replace("&", "and")
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
        game_data["game_title"] = game_data["game_title"].replace(" ", "_").replace("&", "and").lower()
        cursor.execute("INSERT INTO table_games (game_title, game_aka, game_desc, game_rdate, game_rstate, game_url) VALUES (%s, %s, %s, %s, %s, %s)", (game_data["game_title"], game_data["game_aka"], game_data["game_desc"], game_data["game_rdate"], game_data["game_rstate"], None))
        database.commit()
        game_add_user_link(game_get_id(game_data["game_title"]), user_id, database, cursor)
        update_create(game_data["game_title"], database=database, cursor=cursor)
        update_add_game_link(game_get_id(game_data["game_title"]), update_get_id(game_data["game_title"]), user_id, database=database, cursor=cursor)
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
                "game_title": game[1].replace("_", " ").title(),
                "game_rdate": game[2],
            })
        cursor.close()
        database.close()
        return games
    except:
        return None
    
def game_get_tags(game_id, cursor=None):
    try:
        tags = []
        no_cursor = False
        if cursor is None:
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
            no_cursor = True
        cursor.execute("SELECT table_tags.tag_name FROM table_tags INNER JOIN link_game_tag ON table_tags.tag_id=link_game_tag.tag_id WHERE link_game_tag.game_id = %s", (game_id,))
        fetch = cursor.fetchall()
        if no_cursor is True:
            cursor.close()
            database.close()
        if len(fetch) > 0:
            for tag in fetch:
                tags.append(tag[0])
            return tags
        else:
            return []
    except:
        return []
    
def game_check_release_date(game_id=None, game_rdate=None):
    try:
        if game_id is None or game_rdate is None:
            return False
        else:
            if dt.strptime(game_rdate, "%Y/%m/%d") < dt.now():
                database = mysql.connector.connect(**get_db_config(deployed))
                cursor = database.cursor()
                cursor.execute("UPDATE table_games SET game_rstate = 'Released' WHERE game_id = %s", (game_id,))
                database.commit()
                cursor.close()
                database.close()
                return True
            else:
                return False
    except:
        return False

#Tags
def tag_check_exists(tag, tag_type=None, database=None, cursor=None):
    try:
        tag = tag.strip()
        no_cursor = False
        if cursor is None or database is None:
            no_cursor = True
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
        tag = tag.replace("&", "and")
        if tag_type is not None:
            cursor.execute("SELECT tag_id FROM table_tags WHERE tag_name = %s AND tag_type = %s", (tag, tag_type,))
        else:
            cursor.execute("SELECT tag_id FROM table_tags WHERE tag_name = %s", (tag,))
        fetch = cursor.fetchall()
        if no_cursor is True:
            cursor.close()
            database.close()
        if len(fetch) > 0:
            return True
        else:
            return False
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        pause()
        return False
    
def tag_get_id(tag, tag_type=None, cursor=None):
    try:
        if cursor is None:
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
        if tag_type is not None:
            cursor.execute("SELECT tag_id FROM table_tags WHERE tag_name = %s AND tag_type = %s", (str(tag), tag_type,))
        else:
            cursor.execute("SELECT tag_id FROM table_tags WHERE tag_name = %s", (str(tag),))
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
    
def tag_get_name(tag_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT tag_name FROM table_tags WHERE tag_id = %s", (tag_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return fetch[0][0]
        else:
            return None
    except Exception as e:
        return None
    
def tag_get_selection(pid=None, no_results=10):
    try:
        tags = []
        if pid is None:
            pid = 0
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT * FROM table_tags INNER JOIN link_tag_user ON table_tags.tag_id=link_tag_user.tag_id WHERE link_tag_user.tag_link_approved = 1 ORDER BY table_tags.tag_id DESC LIMIT %s, %s", (pid, no_results + 1,))
        fetch = cursor.fetchall()
        for tag in fetch:
            tags.append({
                "tag_id": tag[0],
                "tag_name": tag[1].replace("_", " ").title(),
                "tag_decs": tag[2],
                "tag_type": tag[3].title(),
                "tag_isNSFW": bool(tag[4])
            })
        statement = cursor.statement
        no_pages = get_no_pages(cursor, pid, no_results, command=statement)
        total_tags = get_total_items(statement, cursor)
        cursor.close()
        database.close()
        return (tags, no_pages, total_tags)
    except:
        return None

def tag_get_individual(tag_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT * FROM table_tags WHERE tag_id = %s", (tag_id,))
        fetch = cursor.fetchall()
        if len(fetch) > 0:
            fetch = fetch[0]
            return {
                    "tag_id": fetch[0],
                    "tag_name": fetch[1].replace("_", " ").title(),
                    "tag_desc": fetch[2],
                    "tag_type": fetch[3].title(),
                    "tag_isNSFW": bool(fetch[4])
                }
        else:
            return None
    except Exception as e:
        return None

def tag_add_new(tag_data, user_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        if tag_data["tag_desc"].isspace() or tag_data["tag_desc"] == "":
            tag_data["tag_desc"] = None
        tag_data["tag_name"] = tag_data["tag_name"].replace(" ", "_").replace("&", "and")
        cursor.execute("INSERT INTO table_tags (tag_name, tag_desc, tag_type, tag_isNSFW) VALUES (%s, %s, %s, %s)", (tag_data["tag_name"], tag_data["tag_desc"], tag_data["tag_type"], tag_data["tag_isNSFW"],))
        database.commit()
        tag_data["tag_id"] = tag_get_id(tag_data["tag_name"], tag_data["tag_type"])
        tag_add_user_link(tag_data["tag_id"], user_id, database=database, cursor=cursor)
        cursor.close()
        database.close()
        return True
    except:
        return False

def tag_get_unapproved():
    try:
        tags = []
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT table_tags.tag_id, table_tags.tag_name, table_tags.tag_type, table_tags.tag_isNSFW FROM table_tags INNER JOIN link_tag_user ON table_tags.tag_id=link_tag_user.tag_id WHERE link_tag_user.tag_link_approved = 0 AND link_tag_user.tag_denied = 0")
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            for tag in fetch:
                tags.append({
                    "tag_id": tag[0],
                    "tag_name": tag[1].replace("_", " ").title(),
                    "tag_type": tag[2].title(),
                    "tag_isNSFW": tag[3]
                })
            return tags
        else:
            return None
    except:
        return None
    
def tag_type_change(type_data):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("UPDATE table_tags SET tag_type = %s WHERE tag_id = %s", (type_data["type_newtype"], type_data["type_tag_id"],))
        tag_approve_user_link(type_data["type_tag_id"], reset=True)
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        return False
    
def tag_get_games(tag_id):
    try:
        games = []
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT table_games.game_id, table_games.game_title FROM table_games INNER JOIN link_game_tag ON table_games.game_id=link_game_tag.game_id WHERE link_game_tag.tag_id = %s", (tag_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            for game in fetch:
                games.append({
                    "game_id": game[0],
                    "game_name": game[1].replace("_", " ").title()
                })
            return games
        else:
            return None
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        pause()
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
    
def devpub_get_name(developer_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT developer_name FROM table_developers WHERE developer_id = %s", (developer_id,))
        fetch = cursor.fetchall()
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
        devpub_data["developer_isPub"] = to_bool(devpub_data["developer_isPub"])
        #Check description
        if devpub_data["developer_desc"].isspace() is True or devpub_data["developer_desc"] == "":
            devpub_data["developer_desc"] = None
        #Check founding date
        if devpub_data["developer_foundDate"].isspace() is True or devpub_data["developer_foundDate"] == "":
            devpub_data["developer_foundDate"] = None
            devpub_data["developer_status"] = "Unknown"
        else:
            if dt.strptime(devpub_data["developer_foundDate"], "%Y/%m/%d") < dt.now():
                devpub_data["developer_status"] = "Open for Business"
        #Check defunct date
        if devpub_data["developer_defunctDate"] is not None:
            if devpub_data["developer_defunctDate"].isspace() is True or devpub_data["developer_defunctDate"] == "":
                devpub_data["developer_defunctDate"] = None
            else:
                if dt.strptime(devpub_data["developer_foundDate"], "%Y/%m/%d") < dt.now():
                    devpub_data["developer_status"] = "Defunct"
        devpub_data["developer_name"] = devpub_data["developer_name"].replace(" ", "_").lower()
        cursor.execute("INSERT INTO table_developers (developer_name, developer_desc, developer_foundDate, developer_status, developer_defunctDate, developer_isPub) VALUES (%s, %s, %s, %s, %s, %s)", (devpub_data["developer_name"], devpub_data["developer_desc"], devpub_data["developer_foundDate"], devpub_data["developer_status"], devpub_data["developer_defunctDate"], devpub_data["developer_isPub"],))
        database.commit()
        devpub_data["developer_id"] = devpub_get_id(devpub_data["developer_name"], devpub_data["developer_isPub"])
        devpub_add_user_link(devpub_data["developer_id"], user_id, database=database, cursor=cursor)
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        return False

def devpub_get_selection(pid=None, no_results=10, is_pub=False):
    try:
        devpubs = []
        if pid is None:
            pid = 0
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT * FROM table_developers INNER JOIN link_developer_user ON table_developers.developer_id=link_developer_user.developer_id WHERE link_developer_user.developer_link_approved = 1 AND table_developers.developer_isPub = %s ORDER BY table_developers.developer_id DESC LIMIT %s, %s", (is_pub, pid, no_results + 1))
        fetch = cursor.fetchall()
        for developer in fetch:
            devpubs.append({
                "developer_id": developer[0],
                "developer_name": developer[1].replace("_", " ").title(),
                "developer_desc": developer[2],
                "developer_foundDate": developer[3],
                "developer_status": developer[4],
                "developer_defunctDate": developer[5],
                "developer_isPub": developer[6]
            })
        statement = cursor.statement
        no_pages = get_no_pages(cursor, pid, no_results, command=statement)
        total_devpubs = get_total_items(statement, cursor)
        cursor.close()
        database.close()
        return (devpubs, no_pages, total_devpubs)
    except:
        return None

def devpub_get_individual(developer_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT * FROM table_developers WHERE developer_id = %s", (developer_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            fetch = fetch[0]
            return {
                "developer_id": fetch[0],
                "developer_name": fetch[1].replace("_", " ").title(),
                "developer_desc": fetch[2],
                "developer_foundDate": fetch[3],
                "developer_status": fetch[4],
                "developer_defunctDate": fetch[5],
                "developer_isPub": bool(fetch[6])
            }
        else:
            return None
    except:
        return None
    
def devpub_get_unapproved():
    try:
        devpubs = []
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT table_developers.developer_id, table_developers.developer_name, table_developers.developer_isPub FROM table_developers INNER JOIN link_developer_user ON table_developers.developer_id=link_developer_user.developer_id WHERE link_developer_user.developer_link_approved = 0 AND link_developer_user.developer_denied = 0")
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            for devpub in fetch:
                devpubs.append({
                    "developer_id": devpub[0],
                    "developer_name": devpub[1].replace("_", " ").title(),
                    "developer_isPub": bool(devpub[2]),
                })
            return devpubs
        else:
            return None
    except:
        return None
    
def devpub_get_games(devpub_id):
    try:
        games = []
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT table_games.game_id, table_games.game_title FROM table_games INNER JOIN link_game_developer ON table_games.game_id=link_game_developer.game_id WHERE link_game_developer.developer_id = %s", (devpub_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            for game in fetch:
                games.append({
                    "game_id": game[0],
                    "game_name": game[1].replace("_", " ").title()
                })
            return games
        else:
            return None
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        pause()
        return None

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
    
#Update History
def update_get_id(name, database=None, cursor=None, u_type="game"):
    try:
        no_cursor = False
        if database is None or cursor is None:
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
            no_cursor = True
        cursor.execute("SELECT update_id FROM table_update_history WHERE update_name = %s AND update_type = %s", (name, u_type,))
        fetch = cursor.fetchall()
        if no_cursor is True:
            cursor.close()
            database.close()
        if len(fetch) > 0:
            return fetch[-1][0]
        else:
            return None
    except:
        return None
    
def update_create(name, database=None, cursor=None, changed=None, u_type="game"):
    try:
        no_cursor = False
        if database is None or cursor is None:
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
            no_cursor = True
        if changed is None:
            cursor.execute("INSERT INTO table_update_history (update_name, update_type) VALUES(%s, %s)", (name, u_type,))
        else:
            next_version = update_get_previous_version(name, database=database, cursor=cursor) + 1
            added = ""
            removed = ""
            if len(changed[0]) > 0:
                for item in changed[0]:
                    if added == "":
                        added = item
                    else:
                        added = added + ", " + item
            else:
                added = None
            if len(changed[1]) > 0:
                for item in changed[1]:
                    if removed == "":
                        removed = item
                    else:
                        removed = removed + ", " + item
            else:
                removed = None
            cursor.execute("INSERT INTO table_update_history (update_version, update_name, update_type, update_added, update_removed) VALUES(%s, %s, %s, %s, %s)", (next_version, name, u_type, added, removed,))
        database.commit()
        if no_cursor is True:
            cursor.close()
            database.close()
        return True
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        pause()
        return False
    
def update_get_previous_version(name, database=None, cursor=None, u_type="game"):
    try:
        no_cursor = False
        if database is None or cursor is None:
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
            no_cursor = True
        cursor.execute("SELECT update_version FROM table_update_history WHERE update_name = %s AND update_type = %s", (name, u_type,))
        fetch = cursor.fetchall()
        if no_cursor is True:
            cursor.close()
            database.close()
        if len(fetch) > 0:
            return fetch[-1][0]
        else:
            return 1
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        pause()
        return 1
    
def update_get_all_versions(id, database=None, cursor=None, u_type="game"):
    import pyperclip
    try:
        updates = []
        no_cursor = False
        if database is None or cursor is None:
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
            no_cursor = True
        if u_type == "game":
            cursor.execute("SELECT table_update_history.update_version, table_update_history.update_name, table_update_history.update_added, table_update_history.update_removed, link_game_update.user_id, link_game_update.update_cDate FROM table_update_history INNER JOIN link_game_update ON table_update_history.update_id=link_game_update.update_id WHERE link_game_update.game_id = %s", (id,))
        fetch = cursor.fetchall()
        if no_cursor is True:
            cursor.close()
            database.close()
        if len(fetch) > 0:
            for update in fetch:
                updates.append({
                    "update_version": str(update[0]),
                    "update_name": update[1].replace("_", " ").title(),
                    "update_added": str(update[2]),
                    "update_removed": str(update[3]),
                    "update_username": user_get_username(update[4]),
                    "update_cDate": update[5]
                })
            return updates
        else:
            return None
    except Exception as e:
        print(traceback.format_exc(), flush=True)
        pyperclip.copy(cursor.statement)
        pause()
        return None