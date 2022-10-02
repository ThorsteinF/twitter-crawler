from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import matplotlib.pyplot as plt
from selenium import webdriver
from bs4 import BeautifulSoup
import networkx as nx
import time
import re

# Initializees a graph. This is where all the hashtags will be appended to
G = nx.Graph()

# Scrolls down the page.
def scrolldown():
    for i in range(30):
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(.3)

# Waits for the page to load elements. Stops when a certain element is present.
def wait():
    WebDriverWait(driver, 40).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@class='css-1dbjc4n r-16y2uox r-1wbh5a2 r-1ny4l3l']")
        ))

nodes = []

# Initializing selenium.
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(executable_path="chromedriver.exe", service=s)

# Finds a specific hashtag and adds it to the graph.
def find_hashtag(hashtag):
    url = f'https://twitter.com/hashtag/{hashtag}?src=hashtag_click'
    driver.get(url)

    wait()
    scrolldown()

    # Initializing BeautifulSoup.
    bs = BeautifulSoup(driver.page_source, 'html.parser')
    # Finds all the hashtags on the given page
    hashtags = bs.find_all('a', {'href': re.compile('\/hashtag\/.*')})

    # Appends all the found hashtags to the graph.
    for link in hashtags:
        hashtag_text = link.get_text()
        if hashtag_text.startswith('#'):
            url = link.attrs['href']
            G.add_edge(hashtag, hashtag_text.lower()[1:])
            nodes.append(hashtag_text.lower())

find_hashtag("oslo")
find_hashtag("bergen")

nodes = list(set(nodes))
nodes2 = nodes.copy()

# Second pass of crawling. Crawling all the previous found hashtags for more hashtags.
for i in nodes2:
    find_hashtag(i[1:])

nx.draw(G, with_labels=True)
name = "network"
nx.write_graphml(G, f"{name}.graphml")

# Shows the completed graph of all the hashtags.
plt.show()

driver.quit()