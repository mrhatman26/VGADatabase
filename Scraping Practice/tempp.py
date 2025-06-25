from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import unquote

driver = webdriver.Firefox()
driver.get("https://en.wikipedia.org/w/index.php?title=Special:AllPages&from=%22Air%22+from+Johann+Sebastian+Bach%27s+Orchestral+Suite+No.+3")
temp = driver.find_element(By.CLASS_NAME, "mw-allpages-nav") 
for item in temp.find_elements(By.TAG_NAME, "a"):
    print(item.text)
    if "Next page" in item.text:
        print(unquote(item.get_attribute("href")))
driver.close()