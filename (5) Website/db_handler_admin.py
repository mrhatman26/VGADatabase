import mysql.connector
from global_vars import deployed
from db_config import *
from db_handler_main import *
from db_handler_users import user_check_admin, user_get_username
from misc import pause, get_new_table_id, get_time
from datetime import datetime as dt

def admin_add_scraped_data(game_dict, user_id, database, cursor):
    try:
        #Add game data to database
        release_date = game_dict["game_release_year"] + "/" + game_dict["game_release_month"] + "/" + game_dict["game_release_day"]
        released = "Unreleased"
        if game_dict["game_release_year"] != "-1":
            if dt.strptime(release_date, "%Y/%m/%d") < dt.now():
                released = "Released"
            else:
                released = "Unreleased"
        else:
            released = None
            release_date = None
        current_time = str(get_time(no_brackets=True))
        game_dict["game_title"] = game_dict["game_title"].replace(" ", "_").lower()
        cursor.execute("INSERT INTO table_games (game_title, game_aka, game_desc, game_rdate, game_rstate, game_url) VALUES(%s, %s, %s, %s, %s, %s)", (game_dict["game_title"], None, game_dict["game_description"], release_date, released, game_dict["game_url"]))
        database.commit()
        cursor.execute("INSERT INTO link_game_user (game_id, user_id, game_cDate, game_link_approved, game_aDate, game_denied) VALUES (%s, %s, %s, %s, %s, %s)", (game_get_id(game_dict["game_title"]), user_id, current_time, True, current_time, False,))
        database.commit()
        game_id = game_get_id(game_dict["game_title"])
        update_create(game_dict["game_title"], database=database, cursor=cursor)
        update_add_game_link(game_id, update_get_id(game_dict["game_title"]), user_id, database=database, cursor=cursor)
        #Add developer to database and link to game
        for developer in game_dict["game_developers"]:
            developer = developer.replace(" ", "_").lower()
            developer_exists = devpub_check_exists(developer, False, database, cursor)
            if developer_exists is False:
                cursor.execute("INSERT INTO table_developers (developer_name, developer_desc, developer_foundDate, developer_status, developer_defunctDate, developer_isPub) VALUES(%s, %s, %s, %s, %s, %s)", (str(developer), None, None, None, None, False,))
                database.commit()
            developer_id = devpub_get_id(developer, False, database, cursor)
            if developer_id is not None: #Add link between developer and game (and user)
                if devpub_check_game_link_exists(developer_id, game_id, database, cursor) is False:
                    cursor.execute("INSERT INTO link_game_developer (developer_id, game_id, user_id, developer_cDate, developer_link_approved, developer_aDate) VALUES(%s, %s, %s, %s, %s, %s)", (str(developer_id), str(game_id), str(user_id), current_time, True, current_time,))
                    database.commit()
                if developer_exists is False:
                    cursor.execute("INSERT INTO link_developer_user (developer_id, user_id, developer_cDate, developer_link_approved, developer_aDate) VALUES(%s, %s, %s, %s, %s)", (str(developer_id), str(user_id), current_time, True, current_time))
                    database.commit()
        #Add publishers to database
        for publisher in game_dict["game_developers"]:
            publisher = publisher.replace(" ", "_").lower()
            publisher_exists = devpub_check_exists(publisher, True, database, cursor)
            if publisher_exists is False:
                cursor.execute("INSERT INTO table_developers (developer_name, developer_desc, developer_foundDate, developer_status, developer_defunctDate, developer_isPub) VALUES(%s, %s, %s, %s, %s, %s)", (str(publisher), None, None, None, None, True,))
                database.commit()
            publisher_id = devpub_get_id(publisher, True, database, cursor)
            if publisher_id is not None: #Add link between developer and game (and user)
                if devpub_check_game_link_exists(publisher_id, game_id, database, cursor) is False:
                    cursor.execute("INSERT INTO link_game_developer (developer_id, game_id, user_id, developer_cDate, developer_link_approved, developer_aDate) VALUES(%s, %s, %s, %s, %s, %s)", (str(publisher_id), str(game_id), str(user_id), current_time, True, current_time,))
                    database.commit()
                if publisher_exists is False:
                    cursor.execute("INSERT INTO link_developer_user (developer_id, user_id, developer_cDate, developer_link_approved, developer_aDate) VALUES(%s, %s, %s, %s, %s)", (str(publisher_id), str(user_id), current_time, True, current_time))
                    database.commit()
        #Add genres to database and link to game and user (These are considered Tags though)
        for genre in game_dict["game_genres"]:
            if genre != "nan":
                genre = genre.replace(" ", "_").replace("&", "and").lower()
                genre_exists = tag_check_exists(genre, database=database, cursor=cursor)
                if genre_exists is False:
                    cursor.execute("INSERT INTO table_tags (tag_name, tag_desc, tag_type, tag_isNSFW) VALUES(%s, %s, %s, %s)", (genre, None, "genre", False,))
                    database.commit()
                genre_id = tag_get_id(genre, "genre", cursor)
                if genre_id is not None:
                    if tag_check_game_link_exists(genre_id, game_id, database, cursor) is False:
                        cursor.execute("INSERT INTO link_game_tag (game_id, tag_id, user_id, tag_cDate, tag_link_approved, tag_aDate) VALUES(%s, %s, %s, %s, %s, %s)", (str(game_id), str(genre_id), str(user_id), current_time, True, current_time,))
                        database.commit()
                    if genre_exists is False:
                        cursor.execute("INSERT INTO link_tag_user (tag_id, user_id, tag_cDate, tag_link_approved, tag_aDate) VALUES(%s, %s, %s, %s, %s)", (str(genre_id), str(user_id), current_time, True, current_time,))
                        database.commit()
        #Add user tags to database and link to game and user
        for tag in game_dict["game_user_tags"]:
            tag = tag.replace(" ", "_").replace("&", "and").lower()
            tag_exists = tag_check_exists(tag, tag_type=None, database=database, cursor=cursor)
            if tag_exists is False:
                cursor.execute("INSERT INTO table_tags (tag_name, tag_desc, tag_type, tag_isNSFW) VALUES(%s, %s, %s, %s)", (tag, None, "normal", False,))
                database.commit()
            tag_id = tag_get_id(tag, "normal", cursor)
            if tag_id is not None:
                if tag_check_game_link_exists(tag_id, game_id, database, cursor) is False:
                    cursor.execute("INSERT INTO link_game_tag (game_id, tag_id, user_id, tag_cDate, tag_link_approved, tag_aDate) VALUES(%s, %s, %s, %s, %s, %s)", (str(game_id), str(tag_id), str(user_id), current_time, True, current_time,))
                    database.commit()
                if tag_exists is False:
                    cursor.execute("INSERT INTO link_tag_user (tag_id, user_id, tag_cDate, tag_link_approved, tag_aDate) VALUES(%s, %s, %s, %s, %s)", (str(tag_id), str(user_id), current_time, True, current_time,))
                    database.commit()
        return True
    except Exception as e:
        print(traceback.format_exc())
        pause()
        return False
    
#Users
def admin_swap_stat(user_id, swap_mod=False):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        admin_status = user_check_admin(user_get_username(user_id))
        if swap_mod is False:
            admin_status = not(admin_status[1])
            cursor.execute("UPDATE table_users SET user_isAdmin = %s, user_isMod = 1 WHERE user_id = %s", (admin_status, str(user_id),))
        else:
            admin_status = not(admin_status[0])
            cursor.execute("UPDATE table_users SET user_isMod = %s WHERE user_id = %s", (admin_status, str(user_id),))
        database.commit()
        cursor.close()
        database.close()
        return True
    except:
        return False
    
#Dump
def admin_dump_database():
    try:
        import os
        os.system("mysqldump -u root -pApple_my_Sauce8253 vgadatabase > db_backup.dump")
        return (True, None)
    except Exception as e:
        return (False, e)  
#Misc
def admin_reset_increment():
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        cursor.execute("SHOW TABLES")
        for table in cursor.fetchall():
            cursor.execute("ALTER TABLE " + table[0] + " AUTO_INCREMENT = -1")
            database.commit()
        return True
    except:
        return False