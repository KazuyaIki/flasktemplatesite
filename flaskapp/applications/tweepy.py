import tweepy
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(verbose=True, dotenv_path=dotenv_path)


def tweet_search(keywords, count):
    API_key = os.environ.get("API_KEY")
    API_key_secret = os.environ.get("API_KEY_SECRET")
    Access_token = os.environ.get("ACCESS_TOKEN")
    Access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(API_key, API_key_secret)
    auth.set_access_token(Access_token, Access_token_secret)
    api = tweepy.API(auth)

    tweet_list = []
    tweets = tweepy.Cursor(api.search, keywords, include_entities=True, tweet_mode='extended').items(count)
    for tweet in tweets:
        tweet_dict = {}
        dt = tweet.created_at + timedelta(hours=9)
        created_at = datetime.strftime(dt, '%Y-%m-%d %H:%M:%S')
        tweet_dict['created_at'] = created_at
        tweet_dict['screen_name'] = tweet.user.screen_name
        tweet_dict['name'] = tweet.user.name
        tweet_dict['full_text'] = tweet.full_text
        tweet_dict['favorite_count'] = tweet.favorite_count
        tweet_dict['retweet_count'] = tweet.retweet_count
        tweet_list.append(tweet_dict)

    return tweet_list