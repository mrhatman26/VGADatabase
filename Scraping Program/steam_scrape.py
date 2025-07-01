import requests, csv, time, pyperclip, json
from bs4 import BeautifulSoup as bs
from custom_print import cprint

infite_url = "https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_230_7&infinite=1"
request_url = infite_url
game_data = []
while True:
    try:
        max_game_no = int(input("How many games?: "))
        break
    except:
        print("Please enter a valid number")
        time.sleep(3)
current_game_no = 0
sprint = False #sprint = Surpress Print
auto_retry = True #If set to True, the program will automatically try requesting the game page again without asking the user.
dev_row = []
is_developer = False
publishers = []
developers = []
publisher_found = False
tag_row = []
user_tags = []
features_row = []
features_list = []
mangen_block = []
genres = []
genres_span = []
language_table = []
language_dict = {}
language_features = []
current_language = ""
row_counter = 0
column_counter = 0
game_type = []
na = "N/A"
start_time = time.time() #Get the time of when the program (roughly) began

def get_page_data(page_url, title, price):
    #This function gets each game's data from the URL provided.
    #However, the price and title of each game are provided from the main page as it is easier to get them on the main page than the game page.
    cprint("Scraping game page of " + title, surpress=sprint)
    current_game_data = [None] * 12
    #Create a list of ten empty items. This list will hold the game data about to be collected.
    game_page = requests.get(page_url, allow_redirects=True)
    game_page.encoding = "utf-8"
    game_soup = bs(game_page.content, "html.parser", exclude_encodings=["iso-8859-7", "iso-8859-1"])
    #Get the game's page and parse it with BeautifulSoup. Like the main page, use UTF-8 encoding.
    #Get title [0]
    current_game_data[0] = title
    #Get description [1]
    current_game_data[1] = game_soup.find_all("div", attrs={"class": "game_description_snippet"})
    if len(current_game_data[1]) > 0: #Check to see if the description as a divider exists
        current_game_data[1] = current_game_data[1][0].text.replace("\n", "").replace("\t", "") #Save the description if it exists.
    else: #If it does not exist, it might be a paragprah tag without a class or ID instead of a div with a class.
        current_game_data[1] = game_soup.find_all("div", attrs={"class": "glance_details"})
        if len(current_game_data[1]) > 0: #Check to see if the description as a paragraph exists.
            current_game_data[1] = current_game_data[1][0].find_all("p")[0].text #Save the description if it exists.
        else: #The description as a paragraph does not exist either. The page might no be a game page at all! Set game description to N/A
            current_game_data[1] = na
    #Get release date [2]
    current_game_data[2] = game_soup.find_all("div", attrs={"class": "date"})
    #Get the release date divider and save the release date.
    if len(current_game_data[2]) > 0:
        current_game_data[2] = current_game_data[2][0].text
    else:
        #If no release date is found, save N/A instead.
        current_game_data[2] = na
    #Get developer and publisher [3] & [4]
    dev_row = game_soup.find_all("div", attrs={"class": "dev_row"})
    #Get the developer information from the developer divider.
    publishers = []
    developers = []
    publisher_found = False
    if len(dev_row) > 0:
        for row in dev_row:
            for item in row.find_all("div", attrs={"class": "subtitle column"}):
                if item.text.strip() == "Developer:":
                    is_developer = True
                if item.text.strip() == "Publisher:":
                    publisher_found = True
                    is_developer = False
            row_anchor = row.find_all("a") #Get the anchors in the developer divider. They hold the developer's names.
            for anchor in row_anchor:
                if is_developer is True:
                    if anchor.text not in developers:
                        developers.append(anchor.text)
                    current_game_data[3] = developers
                else:
                    if anchor.text not in publishers:
                        publishers.append(anchor.text)
                    current_game_data[4] = publishers
        if publisher_found is False or len(publishers) < 1:
            current_game_data[4] = na
        if len(developers) < 1:
            current_game_data[3] = na
    else:
        current_game_data[3] = na
        current_game_data[4] = na
        #If the developer divider cannot be found, save the developer and publisher as N/A instead.
    #Get user defined tags [5]
    user_tags = []
    tag_row = game_soup.find_all("div", attrs={"class": "glance_tags popular_tags"})
    #Get the user tags from the 'glance tags' divider. 
    if len(tag_row) > 0:
        for tag in tag_row[0]:
            #For each tag, strip the text of artefacts and, if the tag is not empty and is not the plus (+) button, append it to user_tags.
            tag = tag.text.strip()
            if tag != "" and tag != "+":
                user_tags.append(tag)
        current_game_data[5] = user_tags
        #Save the user_tags list to the current_game_data list.
    else:
        #If the glance tags divider cannot be found, save the tags as N/A instead.
        current_game_data[5] = na
    #Get price [6]
    current_game_data[6] = price
    #Get game features [7]
    features_list = []
    features_row = game_soup.find_all("a", attrs={"class": "game_area_details_specs_ctn"})
    #Get game features from the features area.
    if len(features_row) > 0:
        #For each divider in each feature, if the divider has the class attribute and is not empty, save to the features list.
        for feature in features_row:
            for div in feature:
                if div.has_attr("class") and div.text != "":
                    features_list.append(div.text)
        current_game_data[7] = features_list
        #Save the features list to current_game_data.
    else:
        #If the features anchor cannot be found, save the features as N/A instead.
        current_game_data[7] = na
    #Get supported languages [8]
    row_counter = 0
    current_language = ""
    language_features = []
    language_table = game_soup.find_all("table", attrs={"class": "game_language_options"})
    #Find the language table. 
    if len(language_table) > 0:
        for row in language_table[0]:
            #For each row in the language table, make sure the row is not blank and is not only spaces.
            if str(row) != "" and str(row).isspace() is False:
                #Then, try and find the headers (features) and the languages (rows)
                features = row.find_all("th")
                languages = row.find_all("td")
                if len(features) > 0:
                    #If the features are found, and they are not blank or just spaces, save them to the language_features list.
                    for feature in features:
                        #Oddly, the features are sometimes BeautifulSoup objects and other times, they are just strings. Either way, they are stripped of artefacts here.
                        if type(feature) == str:
                            feature = feature.strip()
                        else:
                            feature = feature.text.strip()
                        if feature != "" and feature.isspace() is False:
                            language_features.append(feature)
                if len(languages) > 0:
                    #If the languages are found...
                    column_counter = 0
                    for column in languages:
                        #Oddly, the languages are sometimes BeautifulSoup objects and other times, they are just strings. Either way, they are stripped of artefacts here.
                        if type(column) == str:
                            column = column.strip()
                        else:
                            column = column.text.strip()
                        if column_counter == 0:
                            #If on the first column of the row, then it is a new language. Save the language to the current_language.
                            current_language = column
                            language_dict[current_language] = [None] * len(language_features)
                            #Save the new language to the language_dict and set its value to a list of None (where the number of None is equal to the number of language_features).
                        else:
                            if column == "✔": #If the column contains a check mark...
                                language_dict[current_language][column_counter - 1] = {language_features[column_counter - 1]: True}
                                #Set the current language to have the language feature by setting it to a dictionary which holds the language feature as the key and True as its value.
                            else:
                                language_dict[current_language][column_counter - 1] = {language_features[column_counter - 1]: False}
                                #Set the current language to NOT have the language feature by setting it to a dictionary which holds the language feature as the key and False as its value.
                        column_counter += 1
        current_game_data[8] = language_dict
        #Save the languages found to current_game_data.
        #This chunk of code is honestly scary. AND I WROTE IT!
    else:
        #If the languages cannot be found, save them as N/A
        current_game_data[8] = na
    #Get genres [9]
    genres = []
    genres_span = game_soup.find_all("div", attrs={"id": "genresAndManufacturer"})
    #Get the genres divider with the id of "genresAndManufacturer" (genres_span is a relic name from when the code targeted a span instead of a dividr)
    if len(genres_span) > 0:
        genres_span = genres_span[0].find_all("span")
        #For each span found in the genres divider, loop through the span and save the genres found to the genres list.
        if len(genres_span) > 0:
            for span in genres_span:
                genres.append(span.text)
            current_game_data[9] = genres
            #Save the genres list to current_game_data
        else:
            #If no genres can be found, save them as N/A instead.
            current_game_data[9] = na
    else:
        #If no genres can be found, save them as N/A instead.
        current_game_data[9] = na
    #Save type (Game, software, hardware, bundles, etc.) [10] #All found within the top bit that goes All Games > Game
    game_type = game_soup.find_all("div", attrs={"class": "blockbg"})
    if len(game_type) > 0:
        for item in game_type:
            item = item.text.upper()
            if "GAMES" in item:
                current_game_data[10] = "Game"
            elif "BUNDLE" in item:
                current_game_data[10] = "Bundle"
            elif "HARDWARE" in item:
                current_game_data[10] = "Hardware"
            elif "SOFTWARE" in item:
                current_game_data[10] = "Software"
            else:
                current_game_data[10] = na
    else:
        current_game_data[10] = na
    #Save game's URL
    current_game_data[11] = page_url
    #Save ALL collected game data to the game_data list.
    game_data.append(current_game_data)

def save_game_data():
    #This function saves the collected game data to a CSV file.
    #If the CSV file is open in Excel (or is failed to be written to for another reason), the user is given the choice to try saving it again.
    while True:
        print("Saving scraped game data to CSV file...", end="")
        try:
            with open("scraped_steam_game_data.csv", "w", encoding="utf-8-sig", newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["game_no", "game_title", "game_description", "game_release_date", "game_developer", "game_publisher", "game_user_tags", "game_price", "game_features", "game_languages", "genres", "type", "steam_url"])
                game_no = str(len(game_data))
                counter = 1
                for game in game_data:
                    cprint("Saving " + str(counter) + " of " + game_no + " games...", surpress=sprint)
                    game.insert(0, counter - 1)
                    writer.writerow(game)
                    counter += 1
            csvfile.close()
            print("Done")
            break
        except Exception as e:
            try:
                csvfile.close()
            except:
                pass
            print("Failed.\nFailed to save data to CSV file. Most likely the file is open in Excel.\n Actual error: " + str(e))
            if input("Try again? (Y/N): ").upper() in "YES" "Y":
                print("Trying again...")
            else:
                print("Saving failed...")
                break

def new_infite_url(game_no):
    #Set the inifite URL to contain the current game number. 
    #From experimentation, the count number does not change the number of games returned; it is always 50 so I've left it as that.
    return "https://store.steampowered.com/search/results/?query&start=" + str(game_no) + "&count=50&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_230_7&infinite=1"

def error_check(main_page):
    #This function checks alerts the user to a faulty game page. If it detects "Site Error" page in the title, then the page returned was Steam's own error page, else, something worse went wrong.
    #This was necessary on the 26th of June because Steam was overloaded due to starting its summer sale.
    main_page = bs(main_page.content, "html.parser")
    pyperclip.copy(main_page.prettify())
    for title in main_page.find_all("title"):
        if title.text == "Site Error":
            raise Exception("Steam returned 'Site Error' page and so the search page has no been loaded. Page HTML saved to clipboard")
    raise Exception("No games found. Page HTML saved to clipboard.")

def convert_time(time):
    time = round(time)
    hours = 0
    minutes = 0
    seconds = 0
    while True:
        if time >= 3600: #An hour
            time -= 3600
            hours += 1
        elif time >= 60: #A minute
            time -= 60
            minutes += 1
        elif time >= 1: #A second
            time -= 1
            seconds += 1
        else:
            break
    return [hours, minutes, seconds]

while current_game_no < max_game_no:
    print("\n" + str(current_game_no) + "/" + str(max_game_no) + " games.")
    print("Next URL is:\n" + request_url + "\n")
    main_page = requests.get(request_url) #Get the next 50 games using the infinite URL.
    if main_page.status_code == 200: #If the request returned a 200 (OK) HTTP code, continue to scrape recieved game data.
        main_page.encoding = "utf-8" #Set encoding to UTF-8 to avoid encoding artefacts.
        if 'application/json' in main_page.headers.get('Content-Type'):
            main_soup = bs(main_page.json()["results_html"], "html.parser", exclude_encodings=["iso-8859-7", "iso-8859-1"])
            #Have BeautifulSoup parse the HTML from the recieved JSON file. Sometimes, BeautifulSoup would use the wrong encodings and so the ones it kept guessing are excluded.
            all_games = main_soup.find_all("a", attrs={"class": "search_result_row ds_collapse_flag"})
            #Find all of the video games in the HTML. Each one is an achor tag with the class of "search_result_row ds_collapse_flag".
            if len(all_games) < 1: #If there are no games, that meanss the page recieved is not the correct one.
                error_check(main_soup, main_page)
            for game in all_games:
                price = game.find_all("div", attrs={"class": "discount_final_price"}) #Get the the divider that holds the game's price.
                if len(price) > 0: #If the price is found, save the text.
                    price = price[0].text
                else: #Some games are free and this is shown as FREE in place of the price. However, some games are free, but the price is blank. So if that is the case, set them to free here.
                    price = "Free"
                get_page_data(game["href"], game.find_all("span", attrs={"class": "title"})[0].text, price) #Get the game data using the game's anchor element href.
                current_game_no += 1
            request_url = new_infite_url(current_game_no)
        else:
            print("Main Page request has no JSON file to read. Status code of the request was: " + str(main_page.status_code))
            if auto_retry is False:
                if input("Try again? (Y/N)").upper() in "YES" "Y":
                    print("Trying again...")
                else:
                    print("Scraping failed...")
                    import sys
                    sys.exit()
            else:
                print("Trying again...")
    else: #If the request returned any other HTTP code (usually 502 for some reason), warn the user and ask if they'd like to try again (unless auto_retry is True)
        print("Main Page request got " + str(main_page.status_code) + " status code instead of 200.")
        if auto_retry is False:
            if input("Try again? (Y/N)").upper() in "YES" "Y":
                print("Trying again...")
            else:
                print("Scraping failed...")
                import sys
                sys.exit()
        else:
            print("Trying again...")
#With all game data collected, save it to a CSV file.
save_game_data()
actual_final_time = time.time() - start_time
final_time = convert_time(actual_final_time)
print("Scraping took " + str(final_time[0]) + " hours, " + str(final_time[1]) + " minutes and " + str(final_time[2]) + " seconds")
print("(Actual time was " + str(actual_final_time) + " seconds)") 
#Save the time it took the program to the scrape_time.txt file.
time_file = open("scrape_time.txt", "w")
time_file.write("Scraping took " + str(time.time() - start_time) + " seconds")
time_file.write("\n(" + str(final_time[0]) + " hours, " + str(final_time[1]) + " minutes and " + str(final_time[2]) + " seconds)")
time_file.close()
#END OF LINE