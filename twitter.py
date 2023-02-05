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

# driver.get("https://twitter.com/Dhanushkumar_SG")

# time.sleep(3)
# user_name = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/h2/div/div/div/div/span[1]/span/span').text
# descriptions = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[2]/div[3]/div/div/span').text
# tweets_count = driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div').text
# professional_category = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[2]/div[4]/div/span[1]/span/span').text
# joined_at = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[2]/div[4]/div/span[2]/span')
# following_count = driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div[2]/div[5]/div[1]/a/span[1]/span').text
# if tweets_count == '0 Tweets':
#     print("no tweets")
# else:
#     print(tweets_count)
# print(descriptions)
# print(professional_category)
# time.sleep(120)

# # import requests
# # from bs4 import BeautifulSoup

# # phone_number = input("Enter a number: ")
# # URL = f"https://calltracer.org/?q={phone_number}"
# # r = requests.get(URL)

# # soup = BeautifulSoup(r.content, 'html.parser') # If this line causes an error, run 'pip install html5lib' or install html5lib

# # output = {}
# # rows = soup.find_all('tr')
# # for i in rows:
# #     row = i.find_all('td')
# #     try:
# #         output[row[0].text] = row[1].text
# #     except:
# #         pass
# # print(output)



import tweepy
import configparser


config = configparser.ConfigParser()
config.read('config.ini')


api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# auth = tweepy.OAuthHandler(api_key,api_key_secret)
# auth.set_access_token(access_token,access_token_secret)

# auth = tweepy.OAuth2BearerHandler("AAAAAAAAAAAAAAAAAAAAAKFclgEAAAAAMzIfccTLM%2BZ1gBnUJ14ewzzo9xU%3D6wz2xdSvLDvqfpr68cKwGu574XzuSP0Ns3iEEzphsaXlMO7aZL")

auth = tweepy.OAuth1UserHandler(
   api_key , api_key_secret, access_token, access_token_secret
)
api = tweepy.API (auth)




# tweets = []
# for status in tweepy.Cursor(api.user_timeline, screen_name='Dhanushkumar_SG', tweet_mode="extended").items():
#     tweets.append(status.full_text)

# for tweet in tweets:
#     print(tweet)
public_tweets = api.user_timeline(screen_name='Dhanushkumar_SG',count=1,tweet_mode="extended")
print(public_tweets[0]._json)
details = public_tweets[0]
# print(details)
user = details.user

return_data = {}
return_data['name'] =  user.name
return_data['screnn name'] = user.screen_name
return_data['location'] = user.location
return_data['description'] = user.description
return_data['followers_count'] = user.followers_count
return_data['friends count'] = user.friends_count
return_data['created at'] = user.created_at
return_data['favourites count'] =  user.favourites_count
return_data['time zone'] = user.time_zone
return_data['geo enabled'] = user.geo_enabled
return_data['verified'] = user.verified
return_data['statuses count'] = user.statuses_count
return_data['lang'] =  user.lang
return_data['background_img_url'] = user.profile_background_image_url
return_data['profile_image_url'] = user.profile_image_url_https

# print(return_data)