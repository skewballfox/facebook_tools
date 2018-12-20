from facebook_tools import *



def get_photos(driver, profile):
    """currently just defaults to save photo, eventually want to rewrite to
    return a list of photo urls, and have a list of options of what to do with
    that list of photos"""

    url='https://m.facebook.com/'+profile
    driver.get(url)
    driver.implicitly_wait(3)
    driver.find_element_by_link_text('Photos').click()
    driver.implicitly_wait(3)

    text = "photoset"
    albums = urls_from_elements(driver.find_elements_by_xpath('//a[contains(@href, "%s")]' % text))

    photo_dir = profile+"_photos"
    make_dir(photo_dir)

    for album in albums:
        driver.get(album)
        driver.implicitly_wait(2)
        end_of_photos = False
        photo_count = 1
        while end_of_photos is False:
            photos = urls_from_elements(driver.find_elements_by_xpath('//a[contains(@class, "ba bb bc")]'))
            for photo in photos:
                driver=save_photo(driver, photo_dir, photo, photo_count)
                photo_count += 1
            try:
                initial_url=driver.current_url;
                driver.implicitly_wait(2)
                driver.find_element_by_id("m_more_item").click()
                wait_and_load(driver, initial_url)
                print('more photos exist')
            except NoSuchElementException:
                end_of_photos = True
                print("Done")
    return driver


def save_photo(driver, photo_dir, url, index):
    driver.get(url)
    text = "view_full_size"
    driver.find_element_by_xpath('//a[contains(@href, "%s")]' % text).click()
    response = requests.get(driver.current_url, stream=True)
    save_image_to_file(response, photo_dir, index)
    return driver

def save_image_to_file(image, dirname, suffix):
    with open('{dirname}/img_{suffix}.jpg'.format(dirname=dirname, suffix=suffix), 'wb') as out_file:
        shutil.copyfileobj(image.raw, out_file)


if __name__ == '__main__':
    username, password = get_credentials()
    profile=get_profile()
    driver=driver_init()
    driver=facebook_login(driver, username, password)

    get_photos(driver, profile)
    url = "https://m.facebook.com/photo.php?fbid=10210636558025136&id=1683223478&set=a.1159436721099&source=56"

    driver.quit()
