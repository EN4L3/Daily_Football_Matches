 
#Import Packages

import requests
from bs4 import BeautifulSoup

#Get Website Data
get_url = "https://www.statarea.com/predictions"
req_url = requests.get(get_url)
soup = BeautifulSoup(req_url.content)

#Find Elements
teams = soup.find_all("div", class_="teams")
texts = [team.text for team in teams]


#Print Elements
for text in texts:
    print(text)
