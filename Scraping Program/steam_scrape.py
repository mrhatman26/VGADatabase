import requests, csv, time, pyperclip, json
from bs4 import BeautifulSoup as bs
from custom_print import cprint

base_url = "https://store.steampowered.com/"
infite_url = "https://store.steampowered.com/search/results/?query&start=0&count=50&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_230_7&infinite=1"
request_url = infite_url
game_data = []
max_game_no = 100
current_game_no = 0
sprint = False #sprint = Surpress Print
dev_row = []
tag_row = []
user_tags = []
features_row = []
features_list = []
mangen_block = []
genres = []

def get_page_data(page_url, title, price):
    current_game_data = [None] * 10 #Create a list of ten items each of which is None.
    game_page = requests.get(page_url)
    game_soup = bs(game_page.content, "html.parser")
    #Get title [0]
    current_game_data[0] = title#game_soup.find_all("div", attrs={"class": "apphub_AppName"})[0].text
    #Get description [1]
    current_game_data[1] = game_soup.find_all("div", attrs={"class": "game_description_snippet"})[0].text.replace("\n", "").replace("\t", "")
    #Get release date [2]
    current_game_data[2] = game_soup.find_all("div", attrs={"class": "date"})[0].text #IT CAN'T BE THAT SIMPLE!
    #Get developer and publisher [3] & [4]
    dev_row = game_soup.find_all("div", attrs={"class": "dev_row"})
    for row in dev_row:
        row_anchor = row.find_all("a")
        for anchor in row_anchor:
            if "developer" in anchor["href"]:
                current_game_data[3] = anchor.text
            else:
                current_game_data[4] = anchor.text
    #Get user defined tags [5]
    user_tags = []
    tag_row = game_soup.find_all("div", attrs={"class": "glance_tags popular_tags"})
    for tag in tag_row[0]:
        tag = tag.text.strip()
        if tag != "" and tag != "+":
            user_tags.append(tag)
    current_game_data[5] = user_tags
    #Get price [6]
    current_game_data[6] = price
    #Get game features [7]
    features_list = []
    features_row = game_soup.find_all("a", attrs={"class": "game_area_details_specs_ctn"})
    for feature in features_row:
        for div in feature:
            if div.has_attr("class") and div.text != "":
                features_list.append(div.text)
    current_game_data[7] = features_list
    #Get supported languages [8] (MAYBE)
    current_game_data[8] = []
    #Get genres [9]
    genres = []
    for span in game_soup.find_all("div", attrs={"id": "genresAndManufacturer"})[0].find_all("span"):
        genres.append(span.text)
    current_game_data[9] = genres
    #no = 0
    #for item in current_game_data:
    #    cprint(str(no) + ":\n" + str(item) + "\n")
    #    no += 1
    game_data.append(current_game_data)

def save_game_data():
    cprint("Saving scraped game data to CSV file...", end_para="\r")
    with open("scraped_steam_game_data.csv", "w", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["game_title", "game_description", "game_release_date", "game_developer", "game_publisher", "game_user_tags", "game_price", "game_features", "game_languages", "genres"])
        for game in game_data:
            writer.writerow(game)
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
    cprint(str(current_game_no) + "/" + str(max_game_no) + " games.", sprint)
    cprint("Next URL is:\n" + request_url + "\n", sprint)
    main_page = requests.get(request_url)
    main_soup = bs(main_page.json()["results_html"], "html.parser")
    all_games = main_soup.find_all("a", attrs={"class": "search_result_row ds_collapse_flag"})
    if len(all_games) < 1:
        error_check(main_soup, main_page)
    for game in all_games:
        get_page_data(game["href"], game.find_all("span", attrs={"class": "title"})[0].text, game.find_all("div", attrs={"class": "discount_final_price"})[0].text)
        current_game_no += 1
    request_url = new_infite_url(current_game_no)
save_game_data()