import praw
import pdb
import re
import os
from nltk.corpus import wordnet

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

# hold valid comments to reply to
possibles = []
# iterate through hot submissions
for submission in subreddit.hot(limit=10):
    # get rid of (load more comments) from CommentForest object
    submission.comments.replace_more(limit=0)
    # make sure we have not already replied to this post
    if submission.id not in posts_replied_to:
        try:
            # get first comment in submission
            first_comment = submission.comments[0]
            # add it to list of possibles
            possibles.append(first_comment)
        # exception case when there are no comments
        except IndexError:
            continue
            # submission.reply("Someday I will be the wordiest bot, but for now I just need to work.")
            # print("Bot replying to: ", submission.title)
            # posts_replied_to.append(submission.id)

def syngen(body):
    print('body = ', body)
    orig = body.split(' ')
    print('orig = ', orig)
    final = []
    for word in orig:
        curr = word
        for ss in wordnet.synsets(word):
            for lemma in ss.lemmas():
                if lemma.name() >= curr:
                    curr = lemma.name()
        final.append(curr)

    return " ".join(final)

new = syngen('We must eat this bread')

print("\n\n-------------------\n",'We must eat this bread', "\n-------------------\n")
print("\n\n-------------------\n", new, "\n-------------------\n")


with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
