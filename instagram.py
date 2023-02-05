import requests
from bs4 import BeautifulSoup

def get_instagram_info(username):
    url = f"https://www.instagram.com/{username}"
    response = requests.get(url)
    if response.status_code == 429:
        return {"error": "rate limit exceeded"}
    if response.status_code == 200:
        return_data = {}
        soup = BeautifulSoup(response.text, "html.parser")
        data = soup.find_all("meta", attrs={"property": "og:description"})
        if data:
            text = data[0].get("content").split()
            return_data['followers'] = text[0]
            return_data['following']  = text[2]
            return_data['posts'] = text[4]
        else:
            return_data["followers"] = 'Not found'
            return_data["following"] = 'Not found'
        data = soup.find_all("meta", attrs={"property": "og:image"})
        if data:
            image = data[0].get("content") 
            return_data["image_url"] = image
        else:
            return_data["image_url"] = 'no profile pic found'
        return return_data
    else:
        return {}

username = input("Enter Instagram username: ")
result = get_instagram_info(username)
if result:
    print(result)
else:
    print("Account not found.")
