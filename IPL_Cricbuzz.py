# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 18:52:57 2021

@author: Dell
"""

#import requests
#
#page = requests.get("https://www.cricbuzz.com/live-cricket-scorecard/10557/rcb-vs-kkr-1st-match-indian-premier-league-2008")
#page.content
#
#from bs4 import BeautifulSoup
#soup = BeautifulSoup(page.content, "html.parser")
#soup
#soup.find_all("td")
#soup.find_all("div", string="Playing")
#
#import re
#soup.find_all("div", string=re.compile("Squad$"))
#soup.find_all("a", string=re.compile("\(wk\)$"))
#soup.find_all("a", string=re.compile(')'))
#soup.find_all("div").find_all()
#
#soup.find_all("div").find_all("a")
#soup.find_all("div", {"class":"cb-col cb-col-73"})
#playersoup.find_all("a", {"class":"margin0 text-black text-hvr-underline"})


import requests
from bs4 import BeautifulSoup
import re
import os
os.chdir("F:\\All\\IPL")

#main_page_url = "https://www.cricbuzz.com/cricket-series/2058/indian-premier-league-2008/matches"
#main_page_url = "https://www.cricbuzz.com/cricket-series/2059/indian-premier-league-2009/matches"
main_page_url = "https://www.cricbuzz.com/cricket-series/2060/indian-premier-league-2010/matches"
main_page = requests.get(main_page_url)
main_page_soup = BeautifulSoup(main_page.content, "html.parser")

matches_url = ["https://www.cricbuzz.com" + link["href"] for link in main_page_soup.find_all("a", {"class":"text-hvr-underline"})]
matches_url = matches_url[:-2]

url_lists = []
#man_of_the_match_list = []
for url in matches_url:
    match_page = requests.get(url)
    match_soup = BeautifulSoup(match_page.content, "html.parser")
#    mom = match_soup.find("a", {"ng-bind":"mom.fullName"})
#    man_of_the_match_list.append(mom)
    score_card_url = "https://www.cricbuzz.com" + match_soup.find("a", string = "Scorecard")["href"]
    
    url_lists.append(score_card_url)


import pandas
data = pandas.DataFrame(columns = ["Team 1", "Team 2", "Team 1 Captain",	"Team 2 Captain",	"Team 1 Wicket Keeper",	"Team 2 Wicket Keeper"])
index = 0
for match_url in url_lists:
    index = index + 1
    page = requests.get(match_url)
#    print(page)
    
    soup = BeautifulSoup(page.content, "html.parser")
    
    teams = [team.text[:-6] for team in soup.find_all("div", string = re.compile("Squad$"))]
#    print(teams)
#    all_teams = all_teams + teams
    
    captains = [captain.text[:([m.start() for m in re.finditer(r"\(", captain.text)][0] - 1)] for captain in soup.find_all("a", string = re.compile("\(c"))]
#    print(captains)
#    all_captains = all_captains + captains
    
    wicket_keepers = [keeper.text[:([m.start() for m in re.finditer(r"\(", keeper.text)][0] - 1)] for keeper in soup.find_all("a", string = re.compile("wk\)"))]
#    print(wicket_keepers)
#    all_keepers = all_keepers + wicket_keepers
    
#    date = soup.find("span", {"class":"schedule-date ng-isolate-scope"}).text
#    print(f"{teams[0]}    {teams[1]}     {captains[0]}    {captains[1]}     {wicket_keepers[0]}    {wicket_keepers[1]}")
    data.loc[index] = [teams[0], teams[1], captains[0], captains[1], wicket_keepers[0], wicket_keepers[1]]

#data.to_csv("Captain2008.csv", index = False)
#data.to_csv("Captain2009.csv", index = False)
data.to_csv("Captain2010.csv", index = False)
