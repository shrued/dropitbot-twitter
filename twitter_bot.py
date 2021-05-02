import pandas as pd
import random
import tweepy
import time
from keys import *

FILE_NAME = 'last_seen_id.txt'
tracks = pd.read_csv("tracks.csv")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def find_track():
  rand_track = random.randint(0, len(tracks)-1)
  track = tracks['Name'][rand_track] + ' by ' + tracks['Artists'][rand_track]
  return(track)

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#dropit' in mention.full_text.lower():
            print('found #dropit!', flush=True)
            print('responding back...', flush=True)
            track = find_track()
            api.update_status('@' + mention.user.screen_name +
                    ' ' + track, mention.id)
while True:
    reply_to_tweets()
    time.sleep(1)