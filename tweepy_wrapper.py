from os import stat
import tweepy
import time

class TweepyWrapper:
    def __init__(this, PATH):
        this.PATH = PATH
        this.api = this.__init_tweepy()
        
    def get_api(this):
        return this.api

    def __load_twitter_secrets(this):
        filename = this.PATH + "/secrets.conf"
        try:
            with open(filename) as f:
                lines = f.readlines()
        except IOError:
            print("Error: " + filename + " does not exist")
            
        secrets = dict()
        
        for line in lines:
            (key, val) = line.strip().split("=")
            secrets[key] = val

        params = ["CONSUMER_KEY", "CONSUMER_SECRET", "ACCESS_TOKEN", "ACCESS_TOKEN_SECRET"]
        for param in params:
            if param not in secrets.keys() or not secrets[param]:
                raise Exception("ERROR: " + param + " is missing in " + filename)

        return secrets

    def __init_tweepy(this):

        __twitter_secrets = this.__load_twitter_secrets()
        auth = tweepy.OAuthHandler(__twitter_secrets["CONSUMER_KEY"], __twitter_secrets["CONSUMER_SECRET"])
        auth.set_access_token(__twitter_secrets["ACCESS_TOKEN"], __twitter_secrets["ACCESS_TOKEN_SECRET"])

        return tweepy.API(auth)

    

    def limit_handled(this, cursor, sleep_interval = 15):
        while True:
            try:
                yield cursor.next()

            except StopIteration:
                break

            except tweepy.RateLimitError:
                time.sleep(sleep_interval * 60)

            
    def	get_user_timeline(this, id, tweet_mode="extended", include_rts=True, limit=-1):
        public_tweets_cursor = tweepy.Cursor(this.api.user_timeline, id=id, tweet_mode=tweet_mode, include_rts=include_rts)
        tweets = []
        count = 1
        for tweet in this.limit_handled(public_tweets_cursor.items()):

                status = tweet.text if tweet_mode == "compact" else tweet.full_text
                if include_rts or (not include_rts and not tweet.retweeted):
                    tweets += status,
                    count += 1
                    if count == limit:
                        break
        return tweets