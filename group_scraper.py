from facebook_tools import *


def scrape_group(driver, group_url):
    driver.get(group_url)
    text="view=members"
    driver.find_element_by_xpath('//a[contains(@href, "%s")]'%text).click()
    driver.implicitly_wait(3)
    text="/browse/group/members"
    driver.find_element_by_xpath('//a[contains(@href, "%s")]'%text).click()







if __name__=="__main__":
    username, password = get_credentials()
    driver = driver_init(debug=True)
    driver = facebook_login(driver, username, password)
    url="https://m.facebook.com/groups/885013951579995?_rdr"
    scrape_group(driver, url)
