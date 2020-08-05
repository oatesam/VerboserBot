import praw
import pdb
import re
import os
from nltk.corpus import wordnet

def syngen(body):
    orig = body.split(' ')
    final = []
    for word in orig:
        curr = word
        for ss in wordnet.synsets(word):
            for lemma in ss.lemmas():
                if lemma.name() >= curr:
                    curr = lemma.name()
        final.append(curr)

    return " ".join(final)

# reddit instance 'bot1' is in the praw.ini
reddit = praw.Reddit('bot1')

# pick a subreddit
subreddit = reddit.subreddit("FreeKarma4U")

# standard bot writeup
bot_boilerplate = ">Salutations. I am known as VerboserBot, the most uncoordinated arrangement of directives ever compiled in a reddit bot."


# create txt of all posts commented on, if it doesn't exist
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))


# iterate through hot submissions
for submission in subreddit.hot(limit=10):
    # get rid of (load more comments) from CommentForest object
    submission.comments.replace_more(limit=0)
    # make sure we have not already replied to this post
    if submission.id not in posts_replied_to:
        try:
            # get first comment in submission
            first_comment = submission.comments[0]
            # generate synonyms for body
            verbosity_achieved = syngen(first_comment.body)
            reply = verbosity_achieved + "\n" + bot_boilerplate
            first_comment.reply(reply)
        # exception case when there are no comments
        except IndexError:
            continue
            # submission.reply("Someday I will be the wordiest bot, but for now I just need to work.")
            # print("Bot replying to: ", submission.title)
            # posts_replied_to.append(submission.id)

with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
