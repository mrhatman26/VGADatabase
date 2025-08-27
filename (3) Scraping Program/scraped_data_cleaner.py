import pandas as pd
import ast

months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

def list_string_to_string(list_val, no_apostrophe=False):
    list_val = list_val.replace("[", "").replace("]", "")
    if no_apostrophe is False:
        list_val = list_val.replace("', ", "¬ ")
    else:
        list_val = list_val.replace(", ", "¬ ")
    list_val = list_val.replace('"', '')
    list_val = list_val.replace(",", "")
    list_val = list_val.replace("¬ ", ", ")
    list_val = list_val.replace("'", "")
    return list_val


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
original_dataset = pd.read_csv("scraped_steam_game_data.csv") #Load the CSV
#Remove Software, Hardware and N/A types
print("Converting columns to strings...", end="")
for column in original_dataset:
    if column != "game_price":
        original_dataset[column] = original_dataset[column].astype(str) #Ensure the type column is all Strings. N/A is converted to NaN by Pandas which is classed as a float.
print("Done\nRemoving all rows that are not of type 'Game'...", end="")
modified_data = original_dataset[original_dataset["type"] == "Game"] #Drop all rows that do not have "Game" as their type.
modified_data.reset_index() #Reset the index to match the different rows.
print("Done.\nRemoving 'type' and 'game_no' columns...", end="")
modified_data = modified_data.drop(columns={"type", "game_no"}, index=1) #Drop the type column as it is no longer needed.
print("Done.\nConverting date to year, month and day columns...", end="")
modified_data["release_year"] = "-1"
modified_data["release_month"] = "-1"
modified_data["release_day"] = "-1"
row_counter = 0
modified_data = modified_data.reset_index(drop=True)
for date in modified_data["game_release_date"]:
    try:
        date = date.replace(",", "").split(" ")
        date[1] = date[1].upper()
        modified_data.loc[row_counter, "release_year"] = str(date[2])
        modified_data.loc[row_counter, "release_month"] = str(months.index(date[1]) + 1)
        modified_data.loc[row_counter, "release_day"] = str(date[0])
    except:
        modified_data.loc[row_counter, "release_year"] = "-1"
        modified_data.loc[row_counter, "release_month"] = "-1"
        modified_data.loc[row_counter, "release_day"] = "-1"
    row_counter += 1
modified_data = modified_data.drop(columns={"game_release_date"}, index=1)
print("Done\nConverting developers list to string...", end="")
modified_data = modified_data.reset_index(drop=True)
row_counter = 0
for developer in modified_data["game_developer"]:
    try:
        developer = list_string_to_string(developer)
        modified_data.loc[row_counter, "game_developer"] = developer
    except:
        modified_data.loc[row_counter, "game_developer"] = "N/A"
    row_counter += 1
print("Done\nConverting publishers list to string...", end="")
modified_data = modified_data.reset_index(drop=True)
row_counter = 0
for publisher in modified_data["game_publisher"]:
    try:
        publisher = list_string_to_string(publisher)
        modified_data.loc[row_counter, "game_publisher"] = publisher
    except:
        modified_data.loc[row_counter, "game_publisher"] = "N/A"
    row_counter += 1
print("Done\nConverting user tags list to string...", end="")
modified_data = modified_data.reset_index(drop=True)
row_counter = 0
for user_tags in modified_data["game_user_tags"]:
    try:
        user_tags = list_string_to_string(user_tags)
        modified_data.loc[row_counter, "game_user_tags"] = user_tags
    except:
        modified_data.loc[row_counter, "game_user_tags"] = "N/A"
    row_counter += 1
print("Done\nConverting game features list to string...", end="")
modified_data = modified_data.reset_index(drop=True)
row_counter = 0
for features in modified_data["game_features"]:
    try:
        features = list_string_to_string(features)
        modified_data.loc[row_counter, "game_features"] = features
    except:
        modified_data.loc[row_counter, "game_features"] = "N/A"
    row_counter += 1
print("Done\nConverting language dicts to strings...", end="")
modified_data = modified_data.reset_index(drop=True)
row_counter = 0
length = str(len(modified_data["game_languages"]))
for language in modified_data["game_languages"]:
    lang_list = []
    try:
        language = ast.literal_eval(language)
        for lang_key, lang_val in language.items():
            for lang_feature in lang_val:
                for feat_key in lang_feature:
                    if lang_feature[feat_key] is True:
                        if lang_key not in lang_list:
                            lang_list.append(lang_key)
        modified_data.loc[row_counter, "game_languages"] = list_string_to_string(str(lang_list))
        modified_data = modified_data.reset_index(drop=True)
    except Exception as e:
        modified_data.loc[row_counter, "game_languages"] = "[]"
        modified_data = modified_data.reset_index(drop=True)
    row_counter += 1
print("Done\nConverting genres list to string...", end="")
modified_data = modified_data.reset_index(drop=True)
row_counter = 0
for genres in modified_data["genres"]:
    try:
        genres = list_string_to_string(genres, no_apostrophe=True)
        modified_data.loc[row_counter, "genres"] = genres
    except:
        modified_data.loc[row_counter, "genres"] = "N/A"
    row_counter += 1
print("Done\nNormalisation complete.")
#Save back to CSV
modified_data.to_csv("cleaned_steam_data.csv", index=False, encoding="utf-8-sig")