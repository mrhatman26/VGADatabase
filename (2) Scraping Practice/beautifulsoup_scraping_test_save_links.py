import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import unquote

base_url = "https://en.wikipedia.org/"
request_url = "https://en.wikipedia.org/wiki/Special:AllPages"
page_max = 5
current_page_no = 0

while current_page_no < page_max:
    print("Next URL:\n" + str(request_url) + "\n")
    request = requests.get(request_url)
    soup = bs(request.content, "html.parser")
    links = soup.find_all("a", attrs={"class":"mw-redirect"})
    if current_page_no == 0:
        links_file = open("links.txt", "w", encoding="utf-8")
    else:
        links_file = open("links.txt", "a", encoding="utf-8")
    link_no = 0
    for link in links:
        print("Saving pages: " + str(link_no) + "/" + str(len(links)), end="\r")
        links_file.write(link.text)
        links_file.write("\n")
        links_file.write(link["href"])
        links_file.write("\n")
        link_no += 1
    links_file.close()
    next_page = soup.find_all("div", attrs={"class":"mw-allpages-nav"})
    for div in next_page:
        for link in div:
            if "Next page" in link.text:
                request_url = base_url + unquote(link["href"])
    current_page_no += 1
    
