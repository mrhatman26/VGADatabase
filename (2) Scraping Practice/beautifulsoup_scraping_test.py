import requests, csv, pyperclip, re, time
from bs4 import BeautifulSoup as bs
from urllib.parse import unquote

start_time = time.time()
base_url = "https://en.wikipedia.org/"
request_url = "https://en.wikipedia.org/wiki/Special:AllPages"
page_max = 5
current_page_no = 0
page_data_list = []

def get_current_page_data(current_page_url, page_data_list):
    page_list = []
    request = requests.get(current_page_url)
    soup = bs(request.content, "html.parser")
    title_span = soup.find_all("span", attrs={"class": "mw-page-title-main"})
    title_list = soup.find_all("h1", attrs={"id": "firstHeading"})
    if len(title_span) >= 1 or len(title_list) >= 1:#Page is valid and not a redirect
        page_list.append(current_page_url)
        if (len(title_span) >= 1):
            page_list.append(title_span[0].get_text())
        else:
            page_list.append(title_list[0].get_text())
        contents_html = soup.find_all("ul", attrs={"class": "vector-toc-contents"})
        contents_list = []
        for list_item in contents_html: #For some reason, you must use three for loops to successfully loop through the contents list? Odd.
            for item in list_item:
                for sub_item in item:
                    if sub_item != "\n":
                        sub_item_text = sub_item.get_text().replace("\n", "")
                        slice_counter = 0
                        while slice_counter < len(sub_item_text):
                            if sub_item_text[slice_counter].isnumeric():
                                slice_counter += 1
                            else:
                                break
                        sub_item_text = sub_item_text[slice_counter:]
                        if re.search("\\.[0-9]+", sub_item_text) is not None:
                            sub_item_text = re.split("\\.[0-9]+", sub_item_text)
                        contents_list.append(sub_item_text)
        page_list.append(contents_list)
        page_list.append("")
        main_body = soup.find_all("div", attrs={"id": "mw-content-text"})
        for item in main_body:
            description = item.find_next("p")
            page_list[2] += description.get_text()
    else:
        print("No title detected, HTML added to clipboard")
        pyperclip.copy(str(soup.prettify()))
        input("(Press ENTER to continue)")
    if len(page_list) > 0:
        page_data_list.append(page_list)

def save_page_data(page_data_list):
    print("Saving scraped page data")
    with open("beautiful_soup_wiki_pages.csv", "w", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["url", "title", "contents", "description"])
        for item in page_data_list:
            writer.writerow(item)
    csvfile.close()


while current_page_no < page_max:
    print(str(current_page_no + 1) + "/" + str(page_max) + " pages")
    print("Next URL:\n" + str(request_url) + "\n")
    try:
        request = requests.get(request_url, allow_redirects=True)
    except Exception as e:
        print("Error: Request to " + request_url + " timed out or failed.")
        print("Actual error:\n" + str(e))
        break
    soup = bs(request.content, "html.parser")
    links = soup.find_all("a", attrs={"class":"mw-redirect"})
    no_links = len(links)
    link_no = 0
    for link in links:
        print("Scraping subpages: " + str(link_no + 1) + "/" + str(no_links), end="\r")
        get_current_page_data(base_url + link["href"], page_data_list)
        link_no += 1
    print("\n")
    next_page = soup.find_all("div", attrs={"class":"mw-allpages-nav"})
    for div in next_page:
        for link in div:
            if "Next page" in link.text:
                request_url = base_url + unquote(link["href"])
    current_page_no += 1
save_page_data(page_data_list)
print("Scraping took " + str(time.time() - start_time) + " seconds") 
time_file = open("beautifulsoup_scrape_time.txt", "w")
time_file.write("Scraping took " + str(time.time() - start_time) + " seconds")
time_file.close()
