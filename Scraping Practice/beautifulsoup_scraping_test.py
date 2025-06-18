import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import unquote

base_url = "https://en.wikipedia.org/"
request_url = "https://en.wikipedia.org/wiki/Special:AllPages"
page_max = 5
current_page_no = 0

def get_current_page_data(current_page_url, current_page_no):
    request = requests.get(current_page_url)
    soup = bs(request.content, "html.parser")
    span = soup.find_all("span", attrs={"class": "mw-page-title-main"})
    if len(span) >= 1:
        if current_page_no == 0:
            wiki_page_file = open("wiki_pages.txt", "w", encoding="utf-8")
            wiki_page_file.write(span[0].text)
            wiki_page_file.close()
        else:
            wiki_page_file = open("wiki_pages.txt", "a", encoding="utf-8")
            wiki_page_file.write(span[0].text)
            wiki_page_file.close()

while current_page_no < page_max:
    print("Next URL:\n" + str(request_url) + "\n")
    request = requests.get(request_url)
    soup = bs(request.content, "html.parser")
    links = soup.find_all("a", attrs={"class":"mw-redirect"})
    if current_page_no == 0:
        temp_file = open("temp.txt", "w", encoding="utf-8")
    else:
        temp_file = open("temp.txt", "a", encoding="utf-8")
    link_no = 0
    for link in links:
        print("Saving pages: " + str(link_no) + "/" + str(len(links)), end="\r")
        temp_file.write(link.text)
        temp_file.write("\n")
        temp_file.write(link["href"])
        get_current_page_data(base_url + link["href"], current_page_no)
        temp_file.write("\n")
        link_no += 1
    temp_file.close()
    next_page = soup.find_all("div", attrs={"class":"mw-allpages-nav"})
    for div in next_page:
        for link in div:
            if "Next page" in link.text:
                request_url = base_url + unquote(link["href"])
    current_page_no += 1
    
