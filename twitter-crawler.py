# Selenium: used to load javascript-content using Google Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
import time

# Initializes selenium
s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(executable_path="chromedriver.exe", service=s)

def crawl(tag, counter = 1):
    # Exit-condition
    if counter >= 7:
        driver.close()
        return

    # Loads twitter-URL
    driver.get('https://twitter.com/search?q=%23' + tag)
    # Waits for content to load
    time.sleep(5)
    # Finds all hashtags on the page and puts them in a list
    hashtags =  driver.find_elements(By.XPATH, '//a[contains(@href, "hashtag/")]')
    # Chooses a random hashtag from the list
    randomtag = hashtags[random.randrange(0,len(hashtags)-1)].text[1:]
    # Prints the chosen hashtag
    print(str(counter) + ": " + randomtag)
    # Recursive function-call
    return crawl(randomtag, counter+1)

crawl("Norway")