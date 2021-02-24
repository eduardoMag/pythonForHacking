import mechanize
#from python2 to python3 it was renamed
import http.cookiejar as cookielib

def printCookies(url):
    browser = mechanize.Browser()
    cookie_jar = cookielib.LWPCookieJar()
    browser.set_cookiejar(cookie_jar)
    page = browser.open(url)
    for cookie in cookie_jar:
        print(cookie)

url = 'http://www.syngress.com/'
printCookies(url)
