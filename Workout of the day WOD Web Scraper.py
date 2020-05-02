# Import packages
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Specify folder and excel location (script will create one automatically if no folder exists)
FOLDER_LOCATION = "FOLDER_PATH"
EXCEL_LOCATION = "EXCEL_PATH"
if not os.path.exists(FOLDER_LOCATION): os.mkdir(FOLDER_LOCATION)

# Assign url and date pattern for regex
URL = "https://comptrain.co/wod"
HEADERS = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
PATTERN = "\d+(\.|-)\d+(\.|-)\d{4}"

# Create empty dataframe - run only once
# WOD_df = pd.DataFrame(index=["Open Prep", "Games Prep"],
#                       columns=pd.date_range(start='2020-04-26', end='2022-04-26').strftime("%Y-%m-%d"))
# WOD_df.to_excel(EXCEL_LOCATION)

# Load excel to store workouts
WOD_df = pd.read_excel(EXCEL_LOCATION, index_col=0)

# Load web page and retrieve daily workout
response = requests.get(URL, headers=HEADERS)
soup = BeautifulSoup(response.text, "html.parser")

# Check html data for wod-wrap class and retrieve workouts
for data in soup.find_all("div", attrs={"class": "wod-wrap"}):
    html_text = data.text

    # Get date to match excel columns
    date = re.search(PATTERN, html_text).group(0)
    date = pd.to_datetime(date).strftime("%Y-%m-%d")

    # Retrieve workouts and save them in the dataframe
    open_prep, games_prep = html_text.split("OPEN PREP\n")[1].split("GAMES PREP\n")
    WOD_df.loc["Open Prep", date], WOD_df.loc["Games Prep", date] = open_prep, games_prep

WOD_df.to_excel(EXCEL_LOCATION)
