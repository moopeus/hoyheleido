import tweepy
from keys import *
import time


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

ID_FILE_NAME = "last_seen_id.txt"


def retrieve_last_seen_id(file_name):
    f_read = open(file_name, "r")
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, "w")
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def reply_to_tweets():
    print("Retrieving tweets and then replying to them...")
    last_seen_id = retrieve_last_seen_id(ID_FILE_NAME)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode="extended")
    for mention in reversed(mentions):
        print(str(mention.id) + " - " + mention.full_text)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, ID_FILE_NAME)
        if "#trigger" in mention.full_text.lower():
            print("Found tweet containing #HelloWorld!")
            print("Responding back...")
            api.update_status("@" + mention.user.screen_name +
                              "Test reply", mention.id)


while True:
    reply_to_tweets()
    time.sleep(15)
