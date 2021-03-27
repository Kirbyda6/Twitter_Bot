import tweepy
import langdetect
import secrets


# Authenticate to Twitter
auth = tweepy.OAuthHandler(secrets.CONSUMER_KEY, secrets.CONSUMER_SECRET)
auth.set_access_token(secrets.ACCESS_KEY, secrets.ACCESS_SECRET)

api = tweepy.API(auth)

if api.verify_credentials() is False:
    print("Error during authentication")


