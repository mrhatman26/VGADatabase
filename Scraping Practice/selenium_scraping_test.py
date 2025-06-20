from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("https://en.wikipedia.org/wiki/Special:AllPages")
links = driver.find_elements(By.CLASS_NAME, "mw-redirect")
#driver.execute_script("window.open('https//www.google.com')")
driver.switch_to.new_window()
driver.get("https://www.google.com")
input("...")
driver.close()
input("...")
for link in links:
    print(link.text)

driver.close()