import csv, ast, mysql.connector
from db_handler_admin import admin_add_scraped_data
from db_config import *
from global_vars import deployed
from file_paths import scraped_file_dir
from misc import get_new_table_id, pause

limit = None

def convert_to_list(data):
    try:
        return data.split(", ")
    except:
        return data

def read_scraped_data(user_id):
    database = mysql.connector.connect(**get_db_config(deployed))
    cursor = database.cursor()
    with open(scraped_file_dir, "r", encoding="utf-8-sig") as scraped_data:
        reader = csv.reader(scraped_data)
        data = list(reader)
        row_length = len(data)
        if limit is not None:
            if row_length > limit:
                row_length = limit
        row_counter = 0
        game_dict = {}
        for row in data:
            if row_counter > 0:
                game_dict = {
                    "game_title": row[0],
                    "game_description": row[1],
                    "game_developers": convert_to_list(row[2]),
                    "game_publishers": convert_to_list(row[3]),
                    "game_user_tags": convert_to_list(row[4]),
                    "game_features": convert_to_list(row[6]),
                    "game_languages": convert_to_list(row[7]),
                    "game_genres": convert_to_list(row[8]),
                    "game_url": row[9],
                    "game_release_year": row[10],
                    "game_release_month": row[11],
                    "game_release_day": row[12],
                    "link_user_id": user_id
                }#Price is not included here because this website is a database of games, not a storefront.
                admin_add_scraped_data(game_dict, user_id, database, cursor)
            row_counter += 1
            print(str(row_counter + 1) + "/" + str(row_length) + " rows loaded from scraped_steam_gamescraped_steam_game_data.csv", flush=True, end="\r")
            if row_counter >= row_length:
                break
        print(str(row_counter + 1) + "/" + str(row_length) + " rows loaded from scraped_steam_gamescraped_steam_game_data.csv\nLoading finished.", flush=True)
    scraped_data.close()
    cursor.close()
    database.close()