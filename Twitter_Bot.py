import tweepy
from PyDictionary import PyDictionary
from langdetect import detect_langs
import random

# Authenticate to Twitter
auth = tweepy.OAuthHandler()
auth.set_access_token()

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")



dictionary = PyDictionary()

user_input = input()  # This will be data passed from the twitter users

# A list of language codes according to ISO 639-1 codes - use for random translations
lang_codes = ['af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'gu',
              'he',
              'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no', 'pa',
              'pl',
              'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'vi',
              'zh-cn', 'zh-tw']


def get_language_code():
    """
    Taking the input, extract and return the detected origin language code. The function checks if the
    input is one of the special case codes starting in z and if so returns the 5 char code. Otherwise,
    it returns the 2 char code.
    :return: a two character string origin language code: ex: en = english
    """
    origin_lang_code_list = detect_langs(user_input)
    origin_lang_code_str = str(origin_lang_code_list)
    if origin_lang_code_str[1] == 'z':
        print(origin_lang_code_str[1:6])
        return origin_lang_code_str[1:6]
    else:
        print(origin_lang_code_str[1:3])
        return origin_lang_code_str[1:3]


if __name__ == '__main__':
    get_language_code()
