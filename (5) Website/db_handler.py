import mysql.connector
from db_config import *
from misc import pause

deployed = False

#ADMIN FUNCTIONS
def add_scraped_data(game_dict):
    #database = mysql.connector.connect(**get_db_config(deployed))
    #cursor = database.cursor()
    for k, v in game_dict.items():
        print(v)
    pause()
    