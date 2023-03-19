import os
import praw
import requests
import time
import dotenv

dotenv.load_dotenv()

reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent=os.environ.get("REDDIT_USER_AGENT"),
)

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL") or ""
SUBREDDIT_NAME = os.environ.get("SUBREDDIT_NAME") or ""
PING_ID = os.environ.get("PING_ID")

UPVOTE_THRESHOLD = 10000
INTERVAL = 5

published = []


def send_webhook(post):
    title = post.title
    url = post.url
    upvotes = post.score
    data = {
        "content": f"<@{PING_ID}>",
        "embeds": [
            {"title": title, "url": url, "footer": {"text": f"Score: {upvotes}"}}
        ]
    }
    requests.post(WEBHOOK_URL, json=data)

    print(data["embeds"][0])


def review():
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    hot_posts = subreddit.hot(limit=50)
    for post in hot_posts:
        if post.score >= UPVOTE_THRESHOLD and post.id not in published:
            send_webhook(post)
            published.append(post.id)


while True:
    review()
    time.sleep(60 * 5)
