from facebook_tools import *


def upload_photos(driver, folder, upload_list ):
    url = 'https://m.facebook.com/'+profile
    driver.get(url)
    driver.implicitly_wait(3)
    driver.find_element_by_xpath("//input[@type='submit' and @value='Photo']").click()
    all_uploaded = False
    while all_uploaded is not True:
        completed_uploads=[]
        photo_inputs = driver.find_elements_by_xpath("//input[@type='file' and @aria-label='Add Photo']")
        for photo, input in zip(upload_list, photo_inputs):
                input.send_keys(folder+"/"+photo.strip())
                with open('%s/posted.txt' % folder, 'a+') as f:
                    if os.path.isfile(folder+"/"+photo):
                        f.write(photo+"\n")
                        completed_uploads.append(photo)
                    else:
                        print("oops %s/%s is not an existing file")
        driver.find_element_by_xpath("//input[@type='submit' and @value='Preview']").click()
        upload_list = set(upload_list) - set(completed_uploads)
        driver.implicitly_wait(15)
        if not upload_list:
            all_uploaded = True
            driver.find_element_by_xpath("//input[@type='submit' and @value='Post']").click()
            driver.implicitly_wait(15)
            """
            I'm going to add an option for tagging here later.
            """
            text="multitag/confirm"
            driver.find_element_by_xpath('//a[contains(@href, "%s")]'%text).click()
        else:
            driver.find_element_by_xpath("//input[@alt='Add Photos' and @name='view_photo']").click()
            driver.implicitly_wait(3)
    return driver


def get_upload_list(folder):
    """checks to see if what photos have been uploaded and returns a list
    of those that haven't been previously uploaded"""
    posted_list = []
    photo_list = []
    with open('%s/posted.txt' % folder, 'r') as f:
        for line in f:
            posted_list.append(line.strip())
    image_ext=(".jpg", ".png", ".gif", ".jpeg", ".tiff", ".tif")
    for file in os.listdir(folder):
        if file.endswith(image_ext):
            photo_list.append(file)
    photo_list = set(photo_list)-set(posted_list)
    return photo_list


def get_profile_folder(profile):
    directory = os.path.abspath(sys.argv[0])
    folder_path=directory.replace(sys.argv[0], '')
    folder_path+="%s_photos"%(profile)
    print(folder_path)
    return (folder_path)


if __name__=="__main__":
    driver = driver_init(debug=True)
    profile = get_profile()
    username, password = get_credentials()

    old_profile="joshua.ferguson.902604"#old profile name
    folder=get_profile_folder(old_profile)

    driver = facebook_login(driver, username, password)
    #url='https://m.facebook.com/'+profile
    #driver.get(url)
    upload_list = get_upload_list(folder)
    driver = upload_photos(driver, folder, upload_list)
