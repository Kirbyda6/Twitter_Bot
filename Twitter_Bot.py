import tweepy
import langdetect
import secrets
from translate import Translator
from langdetect import detect_langs
import random


# Authenticate to Twitter
auth = tweepy.OAuthHandler(secrets.CONSUMER_KEY, secrets.CONSUMER_SECRET)
auth.set_access_token(secrets.ACCESS_KEY, secrets.ACCESS_SECRET)
api = tweepy.API(auth)

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
        print(origin_lang_code[1:6])
        return origin_lang_code[1:6]
    else:
        print(origin_lang_code[1:3])
        return origin_lang_code[1:3]


def translate():
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

    final_translate = Translator(to_lang=get_language_code())
    return final_translate.translate(translated[-1])


if __name__ == '__main__':
    translate()
