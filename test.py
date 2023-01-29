# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# import time
# from selenium.webdriver.common.keys import Keys
# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
# options = webdriver.ChromeOptions()
# options.headless = False
# options.add_argument("user-data-dir=C:\\Users\\dhanu\\AppData\\Local\\Google\\Chrome\\User Data")
# options.add_argument(f'user-agent={user_agent}')
# options.add_argument("--window-size=1920,1080")
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--allow-running-insecure-content')
# options.add_argument("--disable-extensions")
# options.add_argument("--proxy-server='direct://'")
# options.add_argument("--proxy-bypass-list=*")
# options.add_argument("--start-maximized")
# options.add_argument('--disable-gpu')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--no-sandbox')
# driver = webdriver.Chrome(options=options)


# time.sleep(3)

# driver.get("https://www.truecaller.com/reverse-phone-number-lookup")

# input_field = driver.find_element(By.XPATH,'//*[@id="__nuxt"]/div/main/div[2]/section[1]/div/form/input')
# time.sleep(3)
# input_field.click()
# input_field.send_keys("8637497248")
# input_field.send_keys(Keys.ENTER)
# time.sleep(3)
# address = driver.find_element(By.XPATH,'//*[@id="__nuxt"]/div/main/div[2]/div/div[2]/div/div/div[2]/div[2]/a[2]/div/div[2]')
# name = driver.find_element(By.XPATH,'//*[@id="__nuxt"]/div/main/div[2]/div/div[2]/div/div/div[2]/header/div[1]/div[3]')
# print(name.text,address.text)


import requests
from bs4 import BeautifulSoup

phone_number = input("Enter a number: ")
URL = f"https://calltracer.org/?q={phone_number}"
r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html.parser') # If this line causes an error, run 'pip install html5lib' or install html5lib

output = {}
rows = soup.find_all('tr')
for i in rows:
    row = i.find_all('td')
    try:
        output[row[0].text] = row[1].text
    except:
        pass
print(output)