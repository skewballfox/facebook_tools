from facebook_tools import *


def add_friend(driver, profile):
    url = 'https://m.facebook.com/'+profile
    driver.get(url)
    try:
        text="add_friend"
        driver.find_element_by_xpath('//a[contains(@href, "%s")]'%text).click()
        print("added " + profile)
    except NoSuchElementException:
        print("could not add " + profile)
    return driver

def add_from_scraper(driver , filename):
    with open(filename) as input_file:
        for line in input_file:
            if str(line).startswith("/"):
                add_friend(driver, str(line)[1:])
    return driver


if __name__ == "__main__":

    driver = driver_init()
    username, password = get_credentials()
    profile = "joshua.ferguson.902604"
    driver = facebook_login(driver, username, password)
    driver = add_from_scraper(driver, "%s_friends_list.txt"% profile)
    driver.quit()
