import os
from datetime import datetime, timedelta

import praw
from dotenv import dotenv_values, load_dotenv

load_dotenv() 


class Meme():
    def __init__(self, title: str, author: str, score: int, url: str, link_flair_text: str, created: str, permalink: str):
        self.title = title
        self.author = author
        self.score = score
        self.url = url
        self.link_flair_text = link_flair_text
        self.created = created
        self.permalink = permalink
        self.full_permalink = f"https://reddit.com{permalink}"

def get_top_post_from_last_week(filter={}):
    # Reddit API credentials
    reddit = praw.Reddit(
        client_id="Q4rmZgiOKQbL3auTM1p5xg",
        client_secret=os.getenv("REDDIT_SECRET"),
        user_agent="Post Analysis",
    )

    subreddit_name = "DnDmemes"
    subreddit = reddit.subreddit(subreddit_name)

    # Fetch the top posts from the past week
    top_posts = subreddit.top(time_filter="week", limit=10)
    if not top_posts:
        return None
    top_posts = list(top_posts)
    for post in top_posts:
        skip = False
        for key, value in filter.items():
            if key == "not_flair" and post.link_flair_text in value:
                skip = True
            if key == "not_author" and post.author.name in value:
                skip = True
        if skip:
            continue
        top_post = post
        break

    return Meme(
        title=top_post.title,
        author=top_post.author.name,
        score=top_post.score,
        url=top_post.url,
        link_flair_text=top_post.link_flair_text,
        created=datetime.fromtimestamp(top_post.created_utc).strftime("%Y-%m-%d %H:%M:%S"),
        permalink=top_post.permalink
    )

if __name__ == "__main__":
    best_meme = get_top_post_from_last_week({"not_flair": ["Comic", "Not Safe For Work Wednesday"]})
    print(best_meme.title)
    print(best_meme.author)
    print(best_meme.score)
    print(best_meme.url)
    print(best_meme.link_flair_text)
    print(best_meme.created)
    print(best_meme.permalink)