import requests, pyperclip
from bs4 import BeautifulSoup as bs

request = requests.get("https://en.wikipedia.org//wiki/!!!_(American_band)", allow_redirects=False)
#request = requests.get("https://en.wikipedia.org//wiki/!")
soup = bs(request.content, "html.parser")
search = soup.find_all("span", attrs={"class": "mw-redirectedfrom"})
print(search,"\n\n", type(search))
pyperclip.copy(soup.prettify())