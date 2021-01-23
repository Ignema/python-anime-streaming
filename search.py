# importing the requests library 
import sys
import requests
from bs4 import BeautifulSoup
from menu import *

# Get keyword from the shell 
keyword = sys.argv[1]

# api-endpoint 
URL = "https://gogo-play.net/search.html?keyword=" + keyword

# get an html file
def get_html_soup(url):

    # sending get request and saving the response as response object
    try:
        r = requests.get(url = url)    
    except:
        print("Error fetching data...")
        exit(404) 

    # extracting data in json format
    try:
        soup = BeautifulSoup(r.content, "html.parser")
        # print(html)
    except:
        print("Couldn't parse payload...")
        exit(0)

    return soup

# fetch episodes
def getEpisodes(url):
    soup = get_html_soup("https://gogo-play.net" + url)
    episodes = soup.find('ul', attrs={'class':'listing items lists'}).find_all("li")

    # generating candidates 
    candidates = []
    for episode in episodes:
        candidates.append({ 'title': episode.a.find('div', attrs={'class':'name'}).string.strip(), 'type': COMMAND, 
        'command': "python play.py " + episode.a['href'] })

    return candidates

if __name__ == "__main__":
    # get html soup 
    soup = get_html_soup(URL)

    # extracting movies 
    videos = soup.body.find_all('li', attrs={'class':'video-block'})

    # generating candidates 
    candidates = []
    for video in videos:
        candidates.append({ 'title': video.a.find('div', attrs={'class':'name'}).string.strip(), 'type': MENU, 'subtitle': "Select an episode", 'options': getEpisodes(video.a['href']) })
        

    # constructing menu of anime options
    menu_data = {
    'title': "Anime Found!", 'type': MENU, 'subtitle': "Please start scrolling with keyboard...",
    'options': candidates
    }

    # show the menu
    processmenu(menu_data)
