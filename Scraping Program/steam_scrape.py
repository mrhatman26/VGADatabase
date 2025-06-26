import requests, csv, time
from bs4 import BeautifulSoup as bs

base_url = "https://store.steampowered.com/"
request_url = "https://store.steampowered.com/search/"
main_page = requests.get(request_url)
main_soup = bs(main_page.content, "html.parser")
game_data = []
max_game_no = 10
current_game_no = 0

def get_page_data():
    pass

def save_game_data():
    pass

counter = 0
while current_game_no < max_game_no:
    print(str(current_game_no) + "/" + str(max_game_no) + " games.")
    print("Next URL is:\n" + request_url + "\n")
    all_games = main_soup.find_all("a", attrs={"class": "search_result_row ds_collapse_flag"})
    for item in all_games:
        print(item.find_all("span", attrs={"class": "title"})[0].text)
        counter += 1
    break
print(counter)