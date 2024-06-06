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

check_score = 5000
total_posts = 10000
limit = 1000

YTA = 0
NTA = 0

validFlairs = ["Asshole","Not the A-hole","Everyone Sucks","No A-holes here"]

posts = []
ids = []

while len(posts)<total_posts:
    
    print("Searching with score: ",check_score)
    search_results = list(subreddit.search(f'score:>{check_score}',limit=min(limit,total_posts-len(posts))))

    if not search_results:
        print("No results found")
        break
    
    print(len(search_results)," results found...")
    for post in search_results:
        title = post.title
        content = post.selftext
        verdict = post.link_flair_text
        id = post.id
        score = post.score

        if id in ids: continue

        if verdict in validFlairs and "[ Removed by Reddit ]" not in title:

            print("-----------------------------")
            print("Title -- ",title)
            print("Content -- ...")
            print("Verdict -- ",verdict)
            print("Score -- ",score)

            #store id in ids
            ids.append(id)

            #store object
            if verdict=="Asshole" or verdict=="Everyone Sucks": 
                YTA+=1
                verdict="Asshole"
            elif verdict=="Not the A-hole" or verdict=="No A-holes here": 
                NTA+=1
                verdict="Not the A-hole"
            postObj = {"title":title,"content":content,"verdict":verdict}
            posts.append(postObj)
        
            #set new max score
            check_score = score if score>check_score else check_score

    print("-----------------------------")
    print("TIMEOUT TO NOT GET BANNED")
    time.sleep(duration)
    

print("-----------------------------")
print("Total Content:")
print(f"Number of A-holes: {YTA} ({(YTA/len(posts))*100}%)")
print(f"Number of 'saints': {NTA} ({(NTA/len(posts))*100}%)")
print(f"Total posts: {len(posts)}")
print("-----------------------------")




#write to json file
with open(filepath, 'w') as json_file:
    json.dump(posts, json_file, indent=4)  