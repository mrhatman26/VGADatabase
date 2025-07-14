import mysql.connector
from db_config import *
from misc import pause, get_new_table_id

deployed = False

#ADMIN FUNCTIONS
def admin_add_scraped_data(game_dict):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    #Add game data to database
    game_id = get_new_table_id(cursor, "table_games")
    release_date = game_dict["game_release_year"] + "/" + game_dict["game_release_month"] + "/" + game_dict["game_release_day"]
    cursor.execute("INSERT INTO table_games VALUES(%s, %s, %s, %s, %s, %s, %s)", (str(game_id), game_dict["game_title"], None, game_dict["game_description"], release_date, None, game_dict["game_url"]))
    database.commit()
    cursor.close()
    database.close()