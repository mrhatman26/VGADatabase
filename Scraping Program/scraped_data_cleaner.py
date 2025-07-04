import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
original_dataset = pd.read_csv("scraped_steam_game_data.csv") #Load the CSV
#Remove Software, Hardware and N/A types
for column in original_dataset:
    if column != "game_price":
        original_dataset[column] = original_dataset[column].astype(str) #Ensure the type column is all Strings. N/A is converted to NaN by Pandas which is classed as a float.
modified_data = original_dataset[original_dataset["type"] == "Game"] #Drop all rows that do not have "Game" as their type.
modified_data.reset_index() #Reset the index to match the different rows.
modified_data = modified_data.drop(columns={"type", "game_no"}, index=1) #Drop the type column as it is no longer needed.
#Save back to CSV
modified_data.to_csv("cleaned_steam_data.csv", index=False, encoding="utf-8-sig")