import tweepy
import langdetect
import secrets
from translate import Translator
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

        # Finds the tweet text among the data
        text_beg = re.search('"text":', data).start() + 8
        text_end = re.search('"source":', data).start() - 2
        tweet_text = data[text_beg:text_end].lower()

        # Dict containing the tag, newline, and double spaces that need to be replaced
        str_to_replace = {'@hackorproject': '',
                          r'\n': ' ',
                          '  ': ' '}

        for key, value in str_to_replace.items():
            # Replace key character with value character in string
            tweet_text = tweet_text.replace(key, value)

        print(tweet_text)

        # Sends a reply to the user
        user_beg = re.search('"screen_name":"', data).end()
        user_end = re.search('"location"', data).start() - 2
        user = data[user_beg:user_end]
        api.update_status('@' + user + ' Hello', tweet_id)

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
        self.stream.filter(track=['@hackORproject'])


# A list of language codes according to ISO 639-1 codes - use for random translations
lang_codes = ['af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'gu',
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
        print(origin_lang_code[1:6])
        return origin_lang_code[1:6]
    else:
        print(origin_lang_code[1:3])
        return origin_lang_code[1:3]


def translate(user_input):
    """
    :return: Original tweet (in its origin language) after being translated into 10 different random languages
    """
    lang_to_translate_to = random.sample(lang_codes, random.randint(0, 10))
    translated = []
    counter = 0

    for i in lang_to_translate_to:
        counter += 1
        if len(translated) == 0:
            translator = Translator(to_lang=f'{i}')
            translated.append(translator.translate(user_input))
        elif len(translated) < 10:
            translator = Translator(to_lang=f'{i}')
            translated.append(translator.translate(translated[-1]))

    final_translate = Translator(to_lang=get_language_code(user_input))
    return final_translate.translate(translated[-1])


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