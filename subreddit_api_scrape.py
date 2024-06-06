import praw
import json
import time

filepath = "AITA.json"
duration = 10

reddit = praw.Reddit(
    client_id="HpaWZsrVtjnXAXZFIZ0QoQ",
    client_secret = "MJjjwb-PJSFZkX7iDbM1wBRpEC_L7A",
    user_agent = "sentiment_analysis_test by u/Single-Candidate-411"
)

subreddit = reddit.subreddit("AmItheAsshole")


total_posts = 10000
posts_retrieved = 0
after = None

unused = 0
YTA =0
NTA = 0

validFlairs = ["Asshole","Not the A-hole","Everyone Sucks","No A-holes here"]

top_posts=None
posts = []

#Everybody sucks = YTA
#No A-holes here = NTA

while posts_retrieved<total_posts:

    #try the random() method?
    if after:
        top_posts = list(subreddit.top(limit=min(998,total_posts-posts_retrieved),params={'before': after}))
    else:
        top_posts = list(subreddit.top(limit=min(998,total_posts-posts_retrieved)))

    after = top_posts[-1].id
    if not top_posts:
        break
    posts_retrieved+=len(top_posts)

    for post in top_posts:
        title = post.title
        content = post.selftext
        verdict = post.link_flair_text
        id = post.id

        print("-----------------------------")
        print("Title -- ",title)
        print("Content -- ...")
        print("Verdict -- ",verdict)

        if verdict in validFlairs:

            if title=="[ Removed by Reddit ]":
                unused=unused+1
                continue

            if verdict=="Asshole" or verdict=="Everyone Sucks": 
                YTA+=1
                verdict="Asshole"
            elif verdict=="Not the A-hole" or verdict=="No A-holes here": 
                NTA+=1
                verdict="Not the A-hole"
            postObj = {"title":title,"content":content,"verdict":verdict}
            posts.append(postObj)

        else:
            unused=unused+1
            continue
        
    print("-----------------------------")
    print("TIMEOUT TO NOT GET BANNED")
    time.sleep(duration)
    


#analytics
print("-----------------------------")
print("Total Content:")
print(f"Number of A-holes: {YTA} ({(YTA/len(posts))*100}%)")
print(f"Number of 'saints': {NTA} ({(NTA/len(posts))*100}%)")
print(f"Discarded posts: {unused}")
print(f"Total posts: {len(posts)}/{total}")
print("-----------------------------")

#write to json file
with open(filepath, 'w') as json_file:
    json.dump(posts, json_file, indent=4)  





