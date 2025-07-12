import pandas as pd
import ast

months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

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
        modified_data.loc[row_counter, "release_month"] = str(months.index(date[1]))
        modified_data.loc[row_counter, "release_day"] = str(date[0])
    except:
        modified_data.loc[row_counter, "release_year"] = "-1"
        modified_data.loc[row_counter, "release_month"] = "-1"
        modified_data.loc[row_counter, "release_day"] = "-1"
    row_counter += 1
print("Done\nConverting language dicts to strings...", end="")
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
        modified_data.loc[row_counter, "game_languages"] = str(lang_list).strip()
        modified_data = modified_data.reset_index(drop=True)
    except Exception as e:
        #print(str(e))
        modified_data.loc[row_counter, "game_languages"] = "[]"
        modified_data = modified_data.reset_index(drop=True)
    row_counter += 1
print("Done")
#modified_data = modified_data.drop(columns={"game_languages"}, index=1)
#Save back to CSV
modified_data.to_csv("cleaned_steam_data.csv", index=False, encoding="utf-8-sig")