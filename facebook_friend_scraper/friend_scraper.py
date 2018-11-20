import urllib.request
from bs4 import BeautifulSoup
import http.cookiejar
import requests
import pyquery
import configparser


def facebook_login(username, password):
    """Attempts to Login to Facebook, This Frakenstein's monster is a mixture of
    tutorials I found on the web in the process of learning more about a few of
    the options I have available for webscraping

    https://stackoverflow.com/questions/34257186/facebook-login-with-python-requests-and-beautifulsoup
    because the fogetting curve is a bitch

    https://gist.github.com/UndergroundLabs/fad38205068ffb904685
    this is a good bit of the content came. I was originally using a definition
    from another script of I wrote to generate a random user for a database.
    I'm going to put it in it's own repository soon.

    some other stuff:


    https://stackoverflow.com/questions/34257186/facebook-login-with-python-requests-and-beautifulsoup


    https://facebook-sdk.readthedocs.io/en/latest/
    """

    session = requests.session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'})

    login_credentials={
        'email': username,
        'pass': password
        }

    #turns out encoding isn't necessary with the request library
    #as it is handled automatically when posting
    #data = urllib.parse.urlencode(login_credentials).encode("utf-8")

    response = session.post('https://m.facebook.com/login.php', login_credentials,
    allow_redirects=False)

    if 'c_user' in response.cookies:
        # Make a request to homepage to get fb_dtsg token
        homepage_resp = session.get('https://m.facebook.com/home.php')

        dom = pyquery.PyQuery(homepage_resp.text.encode('utf8'))
        fb_dtsg = dom('input[name="fb_dtsg"]').val()

        return fb_dtsg, response.cookies['c_user'], response.cookies['xs']
    else:
        return False


def get_credentials():
    config = configparser.ConfigParser()
    config.sections()
    config.read('/home/daedalus/github/facebook_tools/config.ini')
    config.sections()

    username = config.get("facebook_login", "username")
    password = config.get("facebook_login", "password")
    return username, password


if __name__ == "__main__":

    username, password=get_credentials();

    fb_dtsg, user_id, xs = facebook_login(username, password)

    if user_id:
        print ('{0}:{1}:{2}'.format(fb_dtsg, user_id, xs))
    else:
        print ('Login Failed')

#soup = BeautifulSoup(resp, 'lxml')
