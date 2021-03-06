"""
Build and Tweet
"""
 # importing modules
import re
import os
import csv
import time
import random
import pathlib
import tweepy
# setup
root = pathlib.Path(__file__).parent.parent.resolve()

# secrets
consumer_key = os.getenv('c_key')
consumer_secret = os.getenv('c_secret')
access_token = os.getenv('a_token')
access_token_secret = os.getenv('a_secret')

# functions
def replace_chunk(content, marker, chunk):
    replacer = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(marker, marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(marker, chunk, marker)
    return replacer.sub(chunk, content)

# authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# processing
with open('data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    random_row = random.choice(list(reader))
    data_item_text = random_row['text']

if __name__ == "__main__":
    readme = root / "README.md"
    readme_contents = readme.open().read()
    rewritten = replace_chunk(readme_contents, "crisis_item", data_item_text)
    readme.open("w").write(rewritten)

    print (data_item_text)
    api.update_status(status = "#CrisisChelsea Today's crisis at Chelsea is " + data_item_text)
