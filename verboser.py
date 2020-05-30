import praw
import pdb
import re
import os

# reddit instance 'bot1' is in the praw.ini
reddit = praw.Reddit('bot1')

# pick a subreddit
subreddit = reddit.subreddit("pythonforengineers")

# create txt of all posts commented on, if it doesn't exist
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

for submission in subreddit.hot(limit=10):
    if submission.id not in posts_replied_to:
        if re.search("i love python", submission.title, re.IGNORECASE):
            submission.reply("Nigerian scammer bot says: It's all about the Bass (and Python)")
            print("Bot replying to: ", submission.title)
            posts_replied_to.append(submission.id)

with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")