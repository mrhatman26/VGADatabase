import requests, csv, time, pyperclip, json
from bs4 import BeautifulSoup as bs

base_url = "https://store.steampowered.com/"
infite_url = "https://store.steampowered.com/search/results/?query&start=50&count=1&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_230_7&infinite=1"
request_url = "https://store.steampowered.com/search/?term="
game_data = []
max_game_no = 500
current_game_no = 50

def get_page_data():
    pass

def save_game_data():
    pass

def new_infite_url(game_no):
    return "https://store.steampowered.com/search/results/?query&start=" + str(game_no) + "&count=50&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_230_7&infinite=1"

def error_check(main_soup, e):
    e = e.json()
    pyperclip.copy(main_soup.prettify())
    for title in main_soup.find_all("title"):
        if title.text == "Site Error":
            raise Exception("Steam returned 'Site Error' page and so the search page has no been loaded. Page HTML saved to clipboard")
    with open("json.json", "w", encoding="utf-8") as blah:
        json.dump(e, blah, ensure_ascii=False, indent=4)
    raise Exception("No games found. Page HTML saved to clipboard.")

while current_game_no < max_game_no:
    print(str(current_game_no) + "/" + str(max_game_no) + " games.")
    print("Next URL is:\n" + request_url + "\n")
    main_page = requests.get(request_url)
    main_soup = bs(main_page.content, "html.parser")
    all_games = main_soup.find_all("a", attrs={"class": "search_result_row ds_collapse_flag"})
    if len(all_games) < 1:
        error_check(main_soup, main_page)
    for item in all_games:
        print(item.find_all("span", attrs={"class": "title"})[0].text)
        current_game_no += 1
    request_url = new_infite_url(current_game_no)