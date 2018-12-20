
from facebook_tools import *

def scrape_friends(driver, profile):
    url='https://m.facebook.com/'+profile
    driver.get(url)
    driver.implicitly_wait(3)
    driver.find_element_by_xpath('//a[contains(@href, "friends&lst")]').click()
    driver.implicitly_wait(3)
    More_Friends = True
    while More_Friends is True:
        friends = driver.find_elements_by_xpath('//a[contains(@href, "fref=fr_tab")]')
        with open('%s_friends_list.txt' % profile, 'a+') as f:
            for friend in friends:
                f.write(friend.text+"\n")
                f.write(str(friend.get_attribute("href")).replace("https://m.facebook.com",'').replace("fref=fr_tab",'')[:-1]+"\n")
        try:
            initial_url = driver.current_url;
            div = driver.find_element_by_id("m_more_friends")
            url = div.find_element_by_css_selector('a').get_attribute('href')
            driver.get(url)
            wait_and_load(driver, initial_url)
            print('more friends exist')
        except NoSuchElementException:
            More_Friends = False
            print("Done")
    return driver


if __name__ == '__main__':

    driver = driver_init(debug=True)
    profile = get_profile()
    username, password = get_credentials()
    driver=facebook_login(driver, username, password)

    scrape_friends(driver, profile)
