import mechanize

def testUserAgent(url, userAgent):
    browser = mechanize.Browser()
    browser.addheaders = userAgent
    page = browser.open(url)
    source_code = page.read()
    print(source_code)

url = 'http://whatismyuseragent.dotdon.com/'
userAgent = [('User-agent', 'Mozilla/5.0 (x11: u: '+\'Linux 2.4.2 2 1586: en-US: mIB) Gecko/2000131 Netscape6/6.01')]
testUserAgent(url, userAgent)