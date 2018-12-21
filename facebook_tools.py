from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException


from selenium.webdriver.chrome.options import Options as C_Options
from selenium.webdriver.firefox.options import Options as F_Options
import requests

from bs4 import BeautifulSoup

import os
import sys
import shutil
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
def get_profile():
    config = configparser.ConfigParser()
    config.sections()
    config.read('/home/daedalus/github/facebook_tools/config.ini')
    config.sections()

    profile = config.get("facebook_profile", "profile")
    return profile

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

def make_dir(dirname):
    current_path = os.getcwd()
    path = os.path.join(current_path, dirname)
    if not os.path.exists(path):
        os.makedirs(path)

def urls_from_elements(elements):
    urls = [];
    for element in elements:
        urls.append(element.get_attribute("href"))
    return urls
def driver_init(browser="firefox",debug=False):
    if browser is "firefox":
        if debug is True:
            return webdriver.Firefox()
        else:
            options = F_Options()
            options.set_headless(True)
            options.set_preference("disk-cache-size", 4096)
            options.set_preference("permissions.default.image", 2)
            return webdriver.Firefox(firefox_options=options)
    else:
        if debug is True:
            return webdriver.Chrome()
        else:
            options = C_Options()
            options.chrome_options.add_argument("--headless")
            options.chrome_options.add_argument("--disk-cache-size 4096")
            options.chrome_options.add_argument("--incognito")
            chrome_prefs = {}
            chrome_prefs["profile.default_content_settings"] = {"images": 2}
            chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
            options.experimental_options["prefs"] = chrome_prefs
            return webdriver.Chrome(chrome_options=options)

def wait_and_load(driver, initial_url):
    wait = WebDriverWait(driver, 10)
    try:
        page_loaded = wait.until(
            lambda driver: driver.current_url != initial_url
            )
    except TimeoutException:
        print("Loading timeout expired")
        print(driver.current_url)
    return driver


def facebook_login(driver, username, password):
    driver.get("https://m.facebook.com/login.php")

    assert "Facebook" in driver.title
    if "firefox" in str(driver):
        elem = driver.find_element_by_id("m_login_email")
        elem.send_keys(username)
        elem = driver.find_element_by_name("pass")
        elem.send_keys(password)
    else:
        elem = driver.find_element_by_id("m_login_email")
        elem.send_keys(username)
        elem = driver.find_element_by_id("m_login_password")
        elem.send_keys(password)
    elem.send_keys(Keys.RETURN)

    wait = WebDriverWait( driver, 10 )
    if "firefox" in str(driver):
        url='https://m.facebook.com/login/save-device/?login_source=login&refsrc=https%3A%2F%2Fm.facebook.com%2Flogin.php&_rdr#_=_'
    else:
        url="https://m.facebook.com/login/save-device/?login_source=login#_=_"
    try:
        page_loaded = wait.until(
            lambda driver: driver.current_url == url
            )
    except TimeoutException:
        print( "Loading timeout expired" )
        print(driver.current_url)
    return driver
