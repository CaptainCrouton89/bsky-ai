import os
import sqlite3
from datetime import datetime

from atproto import Client  # type: ignore
from dotenv import dotenv_values, load_dotenv
# importing necessary functions from dotenv library
from fetch.img import download_image_data
from reddit.reddit import Meme, get_top_post_from_last_week

load_dotenv() 


client = Client()
conn = sqlite3.connect("bsky-bot.db")
cursor = conn.cursor()

# client.login('botty-bot-bot.bsky.social', 'Dirhy7-bonciz-xipdyk')
client.login('silasrhyneer.bsky.social', os.getenv('BSKY_PW'))

def init_db():
    cursor.execute('''CREATE TABLE IF NOT EXISTS post_log (id INTEGER PRIMARY KEY, data TEXT, timestamp TEXT)''')
    conn.commit()

def post_dnd_meme():
    best_meme = get_top_post_from_last_week(
        {"not_flair": ["Comic", "Not Safe For Work Wednesday"]})
    image_data = download_image_data(best_meme.url, 950, "JPEG")
    post_meme(image_data, best_meme)

def post_meme(image_data, meme: Meme):
    caption = f"{meme.title}\n\nThe Monday Meme, credit to u/{meme.author}"
    byteStart = caption.find("u/")
    byteEnd = len(meme.author) + byteStart + 2
    try:

        client.send_image(
            text=caption, 
            image=image_data, 
            image_alt=caption, 
            facets=[
                {"index": 
                { "byteStart": byteStart, "byteEnd": byteEnd}, 
                "features": 
                [{"$type": 'app.bsky.richtext.facet#link', "uri": meme.full_permalink}]
                }],
            ) 
        
        cursor.execute("INSERT INTO post_log (data, timestamp) VALUES (?, ?)", ("MORNING", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
    except Exception as e:
        print(e)
        return

if __name__ == "__main__":
    init_db()
    post_dnd_meme()
    # if today is monday, post a dnd meme
    # if datetime.now().weekday() == 0:
    #     post_dnd_meme()
    # # if today is tuesday, post a 
    # if datetime.now().weekday() == 1:
    #     pass