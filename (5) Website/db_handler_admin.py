import mysql.connector
from db_config import *
from db_handler_main import *
from db_handler_users import user_check_admin, user_get_username
from misc import pause, get_new_table_id, get_time

deployed = False

def admin_add_scraped_data(game_dict, user_id):
    try:
        database = mysql.connector.connect(**get_db_config(deployed))
        cursor = database.cursor()
        meh = ""
        #Add game data to database
        game_id = get_new_table_id(cursor, "table_games")
        release_date = game_dict["game_release_year"] + "/" + game_dict["game_release_month"] + "/" + game_dict["game_release_day"]
        cursor.execute("INSERT INTO table_games VALUES(%s, %s, %s, %s, %s, %s, %s)", (str(game_id), game_dict["game_title"], None, game_dict["game_description"], release_date, None, game_dict["game_url"]))
        database.commit()
        #Add developer to database
        for developer in game_dict["game_developers"]:
            developer_id = None
            if developer_check_exists(developer) is False:
                developer_id = get_new_table_id(cursor, "table_developers")
                cursor.execute("INSERT INTO table_developers VALUES(%s, %s, %s, %s, %s, %s, %s)", (str(developer_id), str(developer), None, None, None, None, False,))
                database.commit()
            else:
                developer_id = developer_get_id(developer)
            if developer_id is not None: #Add link between developer and game (and user)
                link_id = get_new_table_id(cursor, "link_game_developer")
                cursor.execute("INSERT INTO link_game_developer VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", (str(link_id), str(developer_id), str(game_id), str(user_id), True, str(get_time(no_brackets=True)).strip(), True, str(get_time(no_brackets=True)).strip(),))
                database.commit()
        cursor.close()
        database.close()
        return True
    except Exception as e:
        print(e)
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