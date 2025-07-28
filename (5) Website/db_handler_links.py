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

def game_add_tag_link(game_id, tag_id, user_id, database=None, cursor=None, remove=False):
    try:
        no_cursor = False
        if database is None or cursor is None:
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
            no_cursor = True
        if remove is False:
            cursor.execute("INSERT INTO link_game_tag (game_id, tag_id, user_id) VALUES (%s, %s, %s)", (game_id, tag_id, user_id,))
        else:
            cursor.execute("DELETE FROM link_game_tag WHERE game_id = %s AND tag_id = %s AND user_id = %s", (game_id, tag_id, user_id,))
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
        cursor.execute("UPDATE link_game_user SET game_link_approved = 1, game_aDate = %s WHERE game_id = %s", (get_time(no_brackets=True), game_id))
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
    
def game_update_tags(tag_data, user_id, tag_get_id_function):
    try:
        added = False
        removed = False
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        for tag in tag_data["change_new_tags"]: #Add new tags
            tag_id = tag_get_id_function(tag, cursor=cursor)
            if tag_check_game_link_exists(tag_id, tag_data["change_game_id"], database=database, cursor=cursor) is False:
                game_add_tag_link(tag_data["change_game_id"], tag_id, user_id, database=database, cursor=cursor)
                added = True
        for tag in tag_data["change_old_tags"]:
            if tag not in tag_data["change_new_tags"]:
                game_add_tag_link(tag_data["change_game_id"], tag_get_id_function(tag, cursor=cursor), user_id, database=database, cursor=cursor, remove=True)
                removed = True
        cursor.close()
        database.close()
        return (added, removed, True)
    except:
        return (added, removed, False)

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
    
def game_get_approval_date(game_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT game_aDate FROM link_game_user WHERE game_id = %s", (game_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return fetch[0][0]
        else:
            return None
    except:
        return None
    
def game_get_devpub_links(game_id, is_devpub=False):
    try:
        devpubs = []
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT table_developers.developer_id, table_developers.developer_name FROM table_developers INNER JOIN link_game_developer ON table_developers.developer_id=link_game_developer.developer_id WHERE table_developers.developer_isPub = %s and link_game_developer.game_id = %s", (is_devpub, game_id,))
        fetch = cursor.fetchall()
        if len(fetch) > 0:
            for devpub in fetch:
                devpubs.append({
                    "developer_id": devpub[0],
                    "developer_name": devpub[1].replace("_", " ").title()
                })
            return devpubs
        else:
            return None
    except:
        return None
    
def game_get_tag_links(game_id, tag_type=None):
    try:
        tags = []
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        if tag_type is None:
            cursor.execute("SELECT table_tags.tag_id, table_tags.tag_name, table_tags.tag_type FROM table_tags INNER JOIN link_game_tag ON table_tags.tag_id=link_game_tag.tag_id WHERE link_game_tag.game_id = %s", (game_id,))
        else:
            cursor.execute("SELECT table_tags.tag_id, table_tags.tag_name, table_tags.tag_type FROM table_tags INNER JOIN link_game_tag ON table_tags.tag_id=link_game_tag.tag_id WHERE link_game_tag.game_id = %s AND table_tags.tag_type = %s", (game_id, tag_type,))
        fetch = cursor.fetchall()
        if len(fetch) > 0:
            for tag in fetch:
                tags.append({
                    "tag_id": tag[0],
                    "tag_name": tag[1].replace("_", " ").title(),
                    "tag_type": tag[2].title()
                })
            return tags
        else:
            return None
    except:
        return None
    
'''Tags'''
#Check
def tag_check_game_link_exists(tag_id, game_id, database=None, cursor=None):
    try:
        no_cursor = False
        if database is None or cursor is None:
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
            no_cursor = True
        cursor.execute("SELECT * FROM link_game_tag WHERE tag_id = %s AND game_id = %s", (tag_id, game_id,))
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
#Get
def tag_get_approved(tag_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT tag_link_approved FROM link_tag_user WHERE tag_id = %s", (tag_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return bool(fetch[0][0])
        else:
            return False
    except:
        return False
    
def tag_get_approval_date(tag_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT tag_aDate FROM link_tag_user WHERE tag_id = %s", (tag_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return fetch[0][0]
        else:
            return None
    except Exception as e:
        return None
    
def tag_get_denial(tag_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT tag_denied FROM link_tag_user WHERE tag_id = %s", (tag_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return bool(fetch[0][0])
        else:
            return None
    except:
        return None
    
def tag_get_denial_reason(tag_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT tag_dDes FROM link_tag_user WHERE tag_id = %s", (tag_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return fetch[0][0]
        else:
            return None
    except:
        return None
    
#Add
def tag_add_user_link(tag_id, user_id, database=None, cursor=None):
    try:
        no_cursor = False
        if database is None or cursor is None:
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
            no_cursor = True
        cursor.execute("INSERT INTO link_tag_user (tag_id, user_id, tag_cDate) VALUES(%s, %s, %s)", (tag_id, user_id, get_time(no_brackets=True),))
        database.commit()
        if no_cursor is True:
            cursor.close()
            database.close()
        return True
    except Exception as e:
        import traceback
        print(traceback.format_exc(), flush=True)
        return False

#Update
def tag_approve_user_link(tag_id, reset=False):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        if reset is False:
            cursor.execute("UPDATE link_tag_user SET tag_link_approved = 1, tag_aDate = %s WHERE tag_id = %s", (str(get_time(no_brackets=True)), tag_id,))
        else:
            cursor.execute("UPDATE link_tag_user SET tag_link_approved = 0, tag_aDate = null WHERE tag_id = %s", (tag_id,))
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        return False
    
def tag_deny_user_link(denial_data):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("UPDATE link_tag_user SET tag_denied = 1, tag_dDate = %s, tag_dDes = %s", (str(get_time(no_brackets=True)), denial_data["denial_text"],))
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        return False
    
'''DEVPUBS'''
#Check
def devpub_check_game_link_exists(developer_id, game_id, database=None, cursor=None):
    try:
        no_cursor = False
        if database is None or cursor is None:
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
            no_cursor = True
        cursor.execute("SELECET * FROM link_game_developer WHERE developer_id = %s AND game_id = %s", (developer_id, game_id))
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

#Get
def devpub_get_approved(developer_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT developer_link_approved FROM link_developer_user WHERE developer_id = %s", (developer_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return bool(fetch[0][0])
        else:
            return False
    except:
        return False
    
def devpub_get_denial(developer_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT developer_denied FROM link_developer_user WHERE developer_id = %s", (developer_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return bool(fetch[0][0])
        else:
            return None
    except:
        return None
    
def devpub_get_denial_reason(developer_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT developer_dDes FROM link_developer_user WHERE developer_id = %s", (developer_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return fetch[0][0]
        else:
            return None
    except:
        return None
    
def devpub_get_approval_date(developer_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SELECT developer_aDate FROM link_developer_user WHERE developer_id = %s", (developer_id,))
        fetch = cursor.fetchall()
        cursor.close()
        database.close()
        if len(fetch) > 0:
            return fetch[0][0]
        else:
            return None
    except Exception as e:
        return None

#Add
def devpub_add_user_link(developer_id, user_id, database=None, cursor=None):
    try:
        no_cursor = False
        if database is None or cursor is None:
            database = mysql.connector.connect(**get_db_config(deployed))
            cursor = database.cursor()
            no_cursor = True
        cursor.execute("INSERT INTO link_developer_user (developer_id, user_id, developer_cDate) VALUES(%s, %s, %s)", (developer_id, user_id, get_time(no_brackets=True),))
        database.commit()
        if no_cursor is True:
            cursor.close()
            database.close()
        return True
    except:
        return False
    
#Update
def devpub_approve_user_link(developer_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("UPDATE link_developer_user SET developer_link_approved = 1, developer_aDate = %s WHERE developer_id = %s", (str(get_time(no_brackets=True)), developer_id,))
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        return False
    
def devpub_deny_user_link(deny_data):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("UPDATE link_developer_user SET developer_denied = 1, developer_dDate = %s, developer_dDes = %s WHERE developer_id = %s", (get_time(no_brackets=True), deny_data["denial_text"], deny_data["denial_developer_id"],))
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        return False