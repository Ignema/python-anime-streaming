# playing video
import sys
import requests
import webbrowser
from bs4 import BeautifulSoup

# Get keyword from the shell 
link = sys.argv[1]

def play(link):
    page = "https://gogo-play.net" + link;
    
    # sending get request and saving the response as response object
    try:
        r = requests.get(url = page)    
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

    webbrowser.open("https:" + soup.find("iframe")['src'], new=2, autoraise=True) 

play(link)