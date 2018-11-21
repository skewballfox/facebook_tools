from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

import configparser
import time


def get_credentials():
    config = configparser.ConfigParser()
    config.sections()
    config.read('/home/daedalus/github/facebook_tools/config.ini')
    config.sections()

    username = config.get("facebook_login", "username")
    password = config.get("facebook_login", "password")
    return username, password
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(3)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            return driver
        last_height = new_height


def facebook_login(driver, username, password):
    driver.get("https://m.facebook.com/login.php")

    print(driver.title)
    assert "Facebook" in driver.title
    elem = driver.find_element_by_id("m_login_email")
    elem.send_keys(username)
    elem = driver.find_element_by_id("m_login_password")
    elem.send_keys(password)
    elem.send_keys(Keys.RETURN)
    #WebDriverWait(driver, 20000)
    wait=WebDriverWait( driver, 10 )

    try:
        page_loaded = wait.until(
            lambda driver: driver.current_url == "https://m.facebook.com/login/save-device/?login_source=login#_=_"
            )
    except TimeoutException:
        print( "Loading timeout expired" )
        print(driver.current_url)
    return driver


def get_friends(driver):
    driver.get("https://mobile.facebook.com/friends/center/friends/")

    driver=scroll_to_bottom(driver)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    start_flag = False
    temp = ''
    for a in soup.find_all('a', href=True):
        if start_flag is True:
                if "/a/mobile/friends/add_friend.php" not in a['href']:
                    if a['href']!='#':
                            if a['href']!=temp:
                                temp = a['href']
                                with open('friends_list.txt', 'a+') as f:
                                    f.write(a['href'])
                                print("Found the profile:", a['href'])
        else:
            if a['href'] == '/friends/center/friends/?mff_nav=1':
                start_flag = True
"""
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)
"""

driver=webdriver.Chrome()
username, password = get_credentials()
driver=facebook_login(driver, username, password)

get_friends(driver)
