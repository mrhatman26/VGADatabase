import requests, csv, time, pyperclip, json
from bs4 import BeautifulSoup as bs
from custom_print import cprint

base_url = "https://store.steampowered.com/"
infite_url = "https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_230_7&infinite=1"
request_url = infite_url
game_data = []
max_game_no = int(input("How many games?: "))
current_game_no = 0
sprint = False #sprint = Surpress Print
dev_row = []
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
na = "N/A"

def get_page_data(page_url, title, price):
    cprint("Scraping game page of " + title, surpress=sprint)
    current_game_data = [None] * 10 #Create a list of ten items each of which is None.
    game_page = requests.get(page_url, allow_redirects=True)
    game_page.encoding = "utf-8"
    game_soup = bs(game_page.content, "html.parser", exclude_encodings=["iso-8859-7", "iso-8859-1"])
    #Check for age verification page
    #Get title [0]
    current_game_data[0] = title
    #Get description [1]
    current_game_data[1] = game_soup.find_all("div", attrs={"class": "game_description_snippet"})
    if len(current_game_data[1]) > 0: #Check to see if the description as a divider exists
        current_game_data[1] = current_game_data[1][0].text.replace("\n", "").replace("\t", "")
    else: #If it does not exist, it might be a paragprah tag without a class or ID instead of a div with a class.
        current_game_data[1] = game_soup.find_all("div", attrs={"class": "glance_details"})
        if len(current_game_data[1]) > 0: #Check to see if the description as a paragraph exists.
            current_game_data[1] = current_game_data[1][0].find_all("p")[0].text
        else: #The description as a paragraph does not exist either. The page might no be a game page at all! So return instead
            current_game_data[1] = na
    #Get release date [2]
    current_game_data[2] = game_soup.find_all("div", attrs={"class": "date"})
    if len(current_game_data[2]) > 0:
        current_game_data[2] = current_game_data[2][0].text
    else:
        current_game_data[2] = na
    #Get developer and publisher [3] & [4]
    dev_row = game_soup.find_all("div", attrs={"class": "dev_row"})
    if len(dev_row) > 0:
        for row in dev_row:
            row_anchor = row.find_all("a")
            for anchor in row_anchor:
                if "developer" in anchor["href"]:
                    current_game_data[3] = anchor.text
                else:
                    current_game_data[4] = anchor.text
    else:
        current_game_data[3] = na
        current_game_data[4] = na
    #Get user defined tags [5]
    user_tags = []
    tag_row = game_soup.find_all("div", attrs={"class": "glance_tags popular_tags"})
    if len(tag_row) > 0:
        for tag in tag_row[0]:
            tag = tag.text.strip()
            if tag != "" and tag != "+":
                user_tags.append(tag)
        current_game_data[5] = user_tags
    else:
        current_game_data[5] = na
    #Get price [6]
    current_game_data[6] = price
    #Get game features [7]
    features_list = []
    features_row = game_soup.find_all("a", attrs={"class": "game_area_details_specs_ctn"})
    if len(features_row) > 0:
        for feature in features_row:
            for div in feature:
                if div.has_attr("class") and div.text != "":
                    features_list.append(div.text)
        current_game_data[7] = features_list
    else:
        current_game_data[7] = na
    #Get supported languages [8] (MAYBE)
    row_counter = 0
    current_language = ""
    language_features = []
    language_table = game_soup.find_all("table", attrs={"class": "game_language_options"})
    if len(language_table) > 0:
        for row in language_table[0]:
            if str(row) != "" and str(row).isspace() is False:
                features = row.find_all("th")
                languages = row.find_all("td")
                if len(features) > 0:
                    for feature in features:
                        if type(feature) == str:
                            feature = feature.strip()
                        else:
                            feature = feature.text.strip()
                        if feature != "" and feature.isspace() is False:
                            language_features.append(feature)
                if len(languages) > 0:
                    column_counter = 0
                    for column in languages:
                        if type(column) == str:
                            column = column.strip()
                        else:
                            column = column.text.strip()
                        if column_counter == 0:
                            current_language = column
                            language_dict[current_language] = [None] * len(language_features)
                        else:
                            print(column)
                            print(language_features, "\n", column_counter)
                            if column == "✔":
                                language_dict[current_language][column_counter - 1] = {language_features[column_counter - 1]: True}
                            else:
                                language_dict[current_language][column_counter - 1] = {language_features[column_counter - 1]: False}
                        column_counter += 1
        print(language_dict, "\n", language_features)
        current_game_data[8] = language_dict
    else:
        current_game_data[8] = na
    input("...")
    #Get genres [9]
    genres = []
    genres_span = game_soup.find_all("div", attrs={"id": "genresAndManufacturer"})
    if len(genres_span) > 0:
        genres_span = genres_span[0].find_all("span")
        if len(genres_span) > 0:
            for span in genres_span:
                genres.append(span.text)
            current_game_data[9] = genres
        else:
            current_game_data[9] = na
    else:
        current_game_data[9] = na
    game_data.append(current_game_data)

def save_game_data():
    cprint("Saving scraped game data to CSV file...", end_para="")
    with open("scraped_steam_game_data.csv", "w", encoding="utf-8-sig", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["game_title", "game_description", "game_release_date", "game_developer", "game_publisher", "game_user_tags", "game_price", "game_features", "game_languages", "genres"])
        game_no = str(len(game_data))
        counter = 1
        for game in game_data:
            cprint("Saving " + str(counter) + " of " + game_no + " games...", surpress=sprint)
            writer.writerow(game)
            counter += 1
    csvfile.close()
    cprint("Done")

def new_infite_url(game_no):
    return "https://store.steampowered.com/search/results/?query&start=" + str(game_no) + "&count=50&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_230_7&infinite=1"

def error_check(main_page):
    main_page = bs(main_page.content, "html.parser")
    pyperclip.copy(main_page.prettify())
    for title in main_page.find_all("title"):
        if title.text == "Site Error":
            raise Exception("Steam returned 'Site Error' page and so the search page has no been loaded. Page HTML saved to clipboard")
    raise Exception("No games found. Page HTML saved to clipboard.")

while current_game_no < max_game_no:
    print(str(current_game_no) + "/" + str(max_game_no) + " games.")
    print("Next URL is:\n" + request_url + "\n")
    main_page = requests.get(request_url)
    main_page.encoding = "utf-8"
    main_soup = bs(main_page.json()["results_html"], "html.parser", exclude_encodings=["iso-8859-7", "iso-8859-1"])
    all_games = main_soup.find_all("a", attrs={"class": "search_result_row ds_collapse_flag"})
    if len(all_games) < 1:
        error_check(main_soup, main_page)
    for game in all_games:
        price = game.find_all("div", attrs={"class": "discount_final_price"})
        if len(price) > 0:
            price = price[0].text
        else:
            price = "Free"
        get_page_data(game["href"], game.find_all("span", attrs={"class": "title"})[0].text, price)
        current_game_no += 1
    request_url = new_infite_url(current_game_no)
save_game_data()