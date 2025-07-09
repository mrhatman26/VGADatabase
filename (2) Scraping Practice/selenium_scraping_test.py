from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import unquote
import time, csv
#https://www.selenium.dev/documentation/webdriver/interactions/windows/
#https://stackoverflow.com/questions/40022010/find-element-by-tag-name-within-element-by-tag-name-selenium
#https://www.geeksforgeeks.org/python/python-web-scraping-tutorial/
start_time = time.time()
base_url = "https://en.wikipedia.org/"
request_url = "https://en.wikipedia.org/wiki/Special:AllPages"
page_max = 5
current_page_no = 0
page_data_list = []
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)
original_tab = driver.current_window_handle

def save_page_data(page_data_list):
    print("Saving scraped page data")
    with open("selenium_wiki_pages.csv", "w", encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["url", "title", "contents", "description"])
        for item in page_data_list:
            writer.writerow(item)
    csvfile.close()

def safe_driver_find(driver, by, search, singular=False):
    results = None
    try:
        if singular is True:
            results = driver.find_element(by, search)
        else:
            results = driver.find_elements(by, search)
        return results
    except:
        return None

def get_current_page_data(driver, current_page_url, page_data_list):
    page_list = []
    driver.switch_to.new_window()
    wait.until(EC.number_of_windows_to_be(2))
    driver.get(current_page_url)
    title_span = None
    title_list = None
    try:
        title_span = driver.find_elements(By.CLASS_NAME, "mw-page-title-main")
        title_list = driver.find_elements(By.ID, "firstHeading")
    except:
        pass
    if len(title_span) > 0 or len(title_list) > 0:
        if len(title_span) > 0:
            page_list.append(title_span[0].text)
        else:
            page_list.append(title_list[0].text)
        contents_html = driver.find_elements(By.CLASS_NAME, "vector-toc-contents")
        if len(contents_html) > 0:
            contents_html = contents_html[0].find_elements(By.TAG_NAME, "li")
            contents_list = []
            for list_item in contents_html:
                if (list_item.text != " " and list_item.text != "" and list_item.text.isspace() is False and list_item.text != " (TOP)"):
                    contents_list.append(list_item.text)
            page_list.append(contents_list)
        else:
            page_list.append([])
        page_list.append("")
        main_body = driver.find_elements(By.ID, "mw-content-text")
        if len(main_body) > 0:
            main_body = main_body[0].find_elements(By.TAG_NAME, "p")
            for paragraph in main_body:
                page_list[2] = paragraph.text
    else:
        print("No title detected on page " + current_page_url + "\nPage will not be scraped")
    if len(page_list) > 0:
        page_data_list.append(page_list)
    driver.close()

while current_page_no < page_max:
    print(str(current_page_no + 1) + "/" + str(page_max) + " pages")
    print("Next URL:\n" + str(request_url) + "\n")
    wait.until(EC.number_of_windows_to_be(1))
    driver.switch_to.window(original_tab)
    driver.get(request_url)
    links = safe_driver_find(driver, By.CLASS_NAME, "mw-redirect")
    no_links = len(links)
    link_no = 0
    for link in links: #ToDo: Have the program get the next page link.
        wait.until(EC.number_of_windows_to_be(1))
        driver.switch_to.window(original_tab)
        print("Scraping subpage " + str(link_no + 1) + "/" + str(no_links) + " in new tab...")
        get_current_page_data(driver, link.get_attribute('href'), page_data_list)
        link_no += 1
    wait.until(EC.number_of_windows_to_be(1))
    driver.switch_to.window(original_tab)
    next_page = driver.find_elements(By.CLASS_NAME, "mw-allpages-nav")
    if len(next_page) > 0:
        for item in next_page[0].find_elements(By.TAG_NAME, "a"):
            if "Next page" in item.text:
                request_url = unquote(item.get_attribute("href"))
    else:
        print("Next page link not found, ending scraping.")
        break
    current_page_no += 1
driver.close()
print(page_data_list)
save_page_data(page_data_list)
print("Scraping took " + str(time.time() - start_time) + " seconds")
time_file = open("selenium_scrape_time.txt", "w")
time_file.write("Scraping took " + str(time.time() - start_time) + " seconds")
time_file.close()