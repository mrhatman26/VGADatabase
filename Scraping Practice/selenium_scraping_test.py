from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = "https://en.wikipedia.org/"
request_url = "https://en.wikipedia.org/wiki/Special:AllPages"
page_max = 10
current_page_no = 0
page_data_list = []
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)
driver.get("https://en.wikipedia.org/wiki/Special:AllPages")
original_tab = driver.current_window_handle

def get_current_page_data(driver, current_page_url, page_data_list):
    page_list = []
    driver.switch_to.new_window()
    wait.until(EC.number_of_windows_to_be(2))
    driver.get(current_page_url)
    for item in driver.find_elements(By.CLASS_NAME, "mw-page_title-main"):
        print(item.text)
    driver.close()

while current_page_no < page_max:
    print(str(current_page_no + 1) + "/" + str(page_max) + " pages")
    print("Next URL:\n" + str(request_url) + "\n")
    wait.until(EC.number_of_windows_to_be(1))
    driver.switch_to.window(original_tab)
    links = driver.find_elements(By.CLASS_NAME, "mw-redirect")
    no_links = len(links)
    link_no = 0
    for link in links: #ToDo: Have the program get the next page link.
        wait.until(EC.number_of_windows_to_be(1))
        driver.switch_to.window(original_tab)
        print("Scraping subpages in new tab...")
        get_current_page_data(driver, link.get_attribute('href'), page_data_list)
    wait.until(EC.number_of_windows_to_be(1))
    driver.switch_to.window(original_tab)
    current_page_no += 1
driver.close()