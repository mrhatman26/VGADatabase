import mysql.connector
from global_vars import deployed
from db_config import *
from db_handler_main import *
from db_handler_users import user_check_admin, user_get_username
from misc import pause, get_new_table_id, get_time

def admin_add_scraped_data(game_dict, user_id, database, cursor):
    #try:
        #Add game data to database
        release_date = game_dict["game_release_year"] + "/" + game_dict["game_release_month"] + "/" + game_dict["game_release_day"]
        cursor.execute("INSERT INTO table_games (game_title, game_aka, game_desc, game_rdate, game_rstate, game_url) VALUES(%s, %s, %s, %s, %s, %s)", (game_dict["game_title"], None, game_dict["game_description"], release_date, None, game_dict["game_url"]))
        database.commit()
        game_id = game_get_id(game_dict["game_title"])
        #print(game_id)
        #pause()
        database.commit()
        current_time = str(get_time(no_brackets=True))
        #Add developer to database and link to game
        for developer in game_dict["game_developers"]:
            if developer_check_exists(developer, cursor) is False:
                cursor.execute("INSERT INTO table_developers (developer_name, developer_desc, developer_foundDate, developer_status, developer_defunctDate, developer_isPub) VALUES(%s, %s, %s, %s, %s, %s)", (str(developer), None, None, None, None, False,))
                database.commit()
            developer_id = developer_get_id(developer, cursor)
            if developer_id is not None: #Add link between developer and game (and user)
                cursor.execute("INSERT INTO link_game_developer (developer_id, game_id, user_id, developer_cDate, developer_link_approved, developer_aDate) VALUES(%s, %s, %s, %s, %s, %s)", (str(developer_id), str(game_id), str(user_id), current_time.strip(), True, current_time.strip(),))
                database.commit()
                cursor.execute("INSERT INTO link_developer_user (developer_id, user_id, developer_cDate, developer_link_approved, developer_aDate) VALUES(%s, %s, %s, %s, %s)", (str(developer_id), str(user_id), current_time.strip(), True, current_time.strip()))
                database.commit()
        #Add publishers to database
        for publisher in game_dict["game_developers"]:
            if publisher_check_exists(publisher, cursor) is False:
                cursor.execute("INSERT INTO table_developers (developer_name, developer_desc, developer_foundDate, developer_status, developer_defunctDate, developer_isPub) VALUES(%s, %s, %s, %s, %s, %s)", (str(publisher), None, None, None, None, True,))
                database.commit()
            publisher_id = developer_get_id(publisher, cursor)
            if publisher_id is not None: #Add link between developer and game (and user)
                cursor.execute("INSERT INTO link_game_developer (developer_id, game_id, user_id, developer_cDate, developer_link_approved, developer_aDate) VALUES(%s, %s, %s, %s, %s, %s)", (str(publisher_id), str(game_id), str(user_id), current_time.strip(), True, current_time.strip(),))
                database.commit()
                cursor.execute("INSERT INTO link_developer_user (developer_id, user_id, developer_cDate, developer_link_approved, developer_aDate) VALUES(%s, %s, %s, %s, %s)", (str(publisher_id), str(user_id), current_time.strip(), True, current_time.strip()))
                database.commit()
        #Add user tags to database and link to game and user
        for tag in game_dict["game_user_tags"]:
            if tag_check_exists(tag, cursor) is False:
                cursor.execute("INSERT INTO table_tags (tag_name, tag_desc, tag_type, tag_isNSFW) VALUES(%s, %s, %s, %s)", (tag, None, None, False,))
                database.commit()
            tag_id = tag_get_id(tag, cursor)
            if tag_id is not None:
                cursor.execute("INSERT INTO link_game_tag (game_id, tag_id, user_id, tag_cDate, tag_link_approved, tag_aDate) VALUES(%s, %s, %s, %s, %s, %s)", (str(game_id), str(tag_id), str(user_id), current_time, True, current_time,))
                database.commit()
                cursor.execute("INSERT INTO link_tag_user (tag_id, user_id, tag_cDate, tag_link_approved, tag_aDate) VALUES(%s, %s, %s, %s, %s)", (str(tag_id), str(user_id), current_time, True, current_time,))
                database.commit()
        #Add genres to database and link to game and user
        for genre in game_dict["game_genres"]:
            genre_id = None
            if genre_check_eixsts(genre, cursor) is False:
                cursor.execute("INSERT INTO table_genres (genre_name, genre_desc, genre_isNSFW) VALUES(%s, %s, %s)", (genre, None, False,))
                database.commit()
            genre_id = genre_get_id(genre, cursor)
            if genre_id is not None:
                cursor.execute("INSERT INTO link_game_genre (game_id, genre_id, user_id, genre_cDate, genre_link_approved, genre_aDate) VALUES(%s, %s, %s, %s, %s, %s)", (str(game_id), str(genre_id), str(user_id), current_time, True, current_time,))
                database.commit()
                cursor.execute("INSERT INTO link_genre_user (genre_id, user_id, genre_cDate, genre_link_approved, genre_aDate) VALUES(%s, %s, %s, %s, %s)", (str(genre_id), str(user_id), current_time, True, current_time,))
                database.commit()
        return True
    #except Exception as e:
    #    return False
    
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