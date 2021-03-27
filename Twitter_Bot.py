import tweepy
import langdetect
import secrets
from PyDictionary import PyDictionary
from langdetect import detect_langs
import random

dictionary = PyDictionary()  # Dictionary object needed for translation

# Authenticate to Twitter
auth = tweepy.OAuthHandler(secrets.CONSUMER_KEY, secrets.CONSUMER_SECRET)
auth.set_access_token(secrets.ACCESS_KEY, secrets.ACCESS_SECRET)
api = tweepy.API(auth)

mentions = api.mentions_timeline()

for mention in mentions:
    print(str(mention.id) + ' - ' + mention.text)

# API Verification
if api.verify_credentials() is False:
    print("Error during authentication")

user_input = input()  # Temporary :: this will be data passed from the twitter users -> once changed need to refactor
                      # get_language_code function

# A list of language codes according to ISO 639-1 codes - use for random translations
lang_codes = ['af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'gu',
              'he', 'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no',
              'pa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk',
              'ur', 'vi', 'zh-cn', 'zh-tw']


def get_language_code():
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
    get_language_code()