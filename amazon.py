
'''load packages'''
import requests
from bs4 import BeautifulSoup

'''define URL where login form is located'''
site = 'https://www.amazon.com/gp/sign-in.html'

'''initiate session'''
session = requests.Session()

'''define session headers'''
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': site
}
'''get login page'''
resp = session.get(site)
html = resp.text

'''get BeautifulSoup object of the html of the login page'''
soup = BeautifulSoup(html, 'lxml')


'''scrape login page to get all the needed inputs required for login'''
data = {}
form = soup.find('form', {'name': 'signIn'})
for field in form.find_all('input'):
    try:
        data[field['name']] = field['value']

    except:
        pass

email_phno = input("enter email: ")
data[u'email'] = email_phno
# data[u'password'] = PASSWORD
post_resp = session.post('https://www.amazon.com/ap/signin', data=data)
post_soup = BeautifulSoup(post_resp.content, 'lxml')
result = post_soup.find_all("div", {"class": "a-alert-content"})

for i in result:
    if ("\n  Enter your password\n" in i.find_all(text=True, recursive=False)):
        print("iruku")
        
