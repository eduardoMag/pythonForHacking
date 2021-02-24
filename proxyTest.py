import mechanize

def testproxy(url, proxy):
    browser = mechanize.Browser()
    browser.set_proxies(proxy)
    page = browser.open(url)
    source_code = page.read()
    print(source_code)

url = 'http://ip.nefsc.noaa.gov/'
hideMeProxy =('http', '216.155.139.135:3128')
testproxy(url, hideMeProxy)