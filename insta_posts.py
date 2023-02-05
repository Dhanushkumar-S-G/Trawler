import requests
from bs4 import BeautifulSoup

def get_instagram_posts(username):
    url = f"https://www.instagram.com/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        images = soup.find_all("img", class_="x5yr21d")
        print(images)
        posts = []
        for image in images:
            posts.append(image["src"])
        return posts
    else:
        return None

username = input("Enter Instagram username: ")
posts = get_instagram_posts(username)
if posts:
    print("Posts:")
    for post in posts:
        print(post)
else:
    print("Account not found.")