from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import json
import time


URL = "https://www.reddit.com/r/AmItheAsshole/top/?t=all"
filePath = "AITA.json"
posts = []
articles = []
total_posts = 10000

validFlairs = ["Asshole","Not the A-hole","Everyone Sucks","No A-holes here"]

yta = 0
nta = 0

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options)


#parses information from article tags
#@params: article - article tags
#@return: object containing information
def parseArticle(article):
    global yta,nta

    strings = []

    tagsWithText = article.find_all(text=True)
    for tag in tagsWithText:
        strings.append(tag.strip())
    
    strings = [x for x in strings if x != ""]
    
    title = strings[0]
    user = strings[1]
    flair = strings[8]
    content = "\n".join(strings[9:])

    if flair in validFlairs and "[ Removed by Reddit ]" not in title:

        if flair=="Asshole" or flair=="Everyone Sucks": 
            yta = yta+1
            flair="Asshole"
        elif flair=="Not the A-hole" or flair=="No A-holes here": 
            nta = nta+1
            flair="Not the A-hole"
        
        obj = {
            "user":user,
            "title":title,
            "content":content,
            "label":flair
        }
        return obj




#selenium interacts with page to load more posts
def scrollDown():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)

#go to page
driver.get(URL)

while True:

    #retrieve HTML from page
    updatedHtml = driver.page_source
    soup = BeautifulSoup(updatedHtml,'html.parser')
    
    #retrieve (valid) article tags
    for article in soup.find_all("article",class_="w-full m-0"):
        articles.append(article)
    
    #count
    print(len(articles))

    if len(articles) < total_posts:
        for i in range(10):
            scrollDown()
        articles= []
    
    else:
        driver.quit()
        break


for post in articles:
    article = parseArticle(post)
    if article: posts.append(article)

print("Total posts: ",len(posts))
print(f"YTA: {yta} ({(yta/len(posts))*100}%)")
print(f"NTA: {nta} ({(nta/len(posts))*100}%)")

#write to json file
with open(filePath, 'w') as json_file:
    json.dump(posts, json_file, indent=4)  








