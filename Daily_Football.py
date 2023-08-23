
 
#Import Packages

import requests
from bs4 import BeautifulSoup
import pandas as pd



#URL of the website statarea.com
url = "https://www.statarea.com/predictions/date/2023-08-19/"

# Send a request to the website and get the response
response = requests.get(url)

#BeautifulSoup to parse the HTML
soup = BeautifulSoup(response.content, "html.parser")

# Create an empty list to store the data
matches = []

# Find all the div tags with the class 'match'
match_divs = soup.find_all("div", {"class": "match"})
for m_div in match_divs:
    #Find the Time for Match
    match_time = m_div.find("div", {"class": "date"}).get_text() 
    # Find the host team name
    host_team = m_div.find("div", {"class": "hostteam"}).get_text().strip()
    # Find the guest team name
    guest_team = m_div.find("div", {"class": "guestteam"}).get_text().strip()   
    
    # Find all the div tags with the class 'coefbox'
    divs = m_div.find_all("div", {"class": "coefbox"})
    for div in divs:
        text = div.get_text()
        
        # Try to convert the text content to a float
        try:
            coef = float(text)
        except ValueError:
            continue
        
        # Check if the coefficient of over 1.5 goals is greater 95
        if coef > 1.5 and coef < 99:
            matches.append((match_time,host_team, guest_team, coef))


# Create a DataFrame from the list of tuples

Teams_Data = pd.DataFrame(matches, columns=['Time','Host_Team', 'Guest_Team', 'Coefficient'])
Teams_Data['Time'] = pd.to_datetime(Teams_Data['Time'])


Team_List= Teams_Data.groupby(['Time','Host_Team', 'Guest_Team']).agg({'Coefficient': 'max'})
Team_List['Coefficient'] = Team_List['Coefficient'].astype(int)

Team_List.loc[Team_List['Coefficient'] > 95].value_counts().sum()
