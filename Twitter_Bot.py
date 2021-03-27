import tweepy
import langdetect
import secrets
from PyDictionary import PyDictionary
from langdetect import detect_langs
import random
import re


# This is the listener that accesses the flow of data from twitter
class MentionListener(tweepy.StreamListener):

    # These two funcs print out data that passes our filter (see MentionStream) to the terminal
    def on_data(self, data):
        self.process_data(data)
        return True

    def process_data(self, data):
        print(data)
        result = re.search('"id":\d+', data)
        tweet_id = result.group()[5:]
        print(tweet_id)

    # Return false to disconnect the stream - something went wrong
    def on_error(self, status_code):
        if status_code == 420:
            return False


# This is our stream that filters out mentions, AKA only pays attention to the data we want
class MentionStream:
    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start(self):
        # Detects when someone replies to it with @HackorProject
        self.stream.filter(track=['HackorProject'])


dictionary = PyDictionary()  # Dictionary object needed for translation

# A list of language codes according to ISO 639-1 codes - use for random translations
LANG_CODES = ['af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'gu',
              'he', 'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no',
              'pa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk',
              'ur', 'vi', 'zh-cn', 'zh-tw']


def get_language_code(user_input):
    """
    Taking the input, extract and return the detected origin language code. The function checks if the
    input is one of the special case codes starting in z and if so returns the 5 char code. Otherwise,
    it returns the 2 char code.
    :return: a two character string origin language code: ex: en = english
    """
    origin_lang_code = str(detect_langs(user_input))
    if origin_lang_code[1] == 'z':
        return origin_lang_code[1:6]
    else:
        return origin_lang_code[1:3]


if __name__ == '__main__':
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(secrets.CONSUMER_KEY, secrets.CONSUMER_SECRET)
    auth.set_access_token(secrets.ACCESS_KEY, secrets.ACCESS_SECRET)
    api = tweepy.API(auth)

    # API Verification
    if api.verify_credentials() is False:
        print("Error during authentication")

    listener = MentionListener()
    stream = MentionStream(auth, listener)
    stream.start()
