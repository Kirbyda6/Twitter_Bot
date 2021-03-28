import tweepy
import secrets
import random
import re
from deep_translator import GoogleTranslator, single_detection



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

        # This block runs the translate method 10 times and mutates rep with the final translation
        rep = []
        starter_lang = single_detection(f'{tweet_text}', api_key=f'{secrets.DTL}')
        num = 10
        translate(tweet_text, starter_lang, num, rep)

        # Sends a reply to the user
        user_beg = re.search('"screen_name":"', data).end()
        user_end = re.search('"location"', data).start() - 2
        user = data[user_beg:user_end]
        api.update_status('@' + user + ' ' + translate(tweet_text), tweet_id)


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
lang_dict = GoogleTranslator.get_supported_languages(as_dict=True)
lang_codes = list(lang_dict.values())


def translate(text):
    origin_lang = single_detection(text, api_key=secrets.DTL)
    languages = random.sample(lang_codes, 10)
    for lang in languages:
        text = GoogleTranslator(source='auto', target=lang).translate(text)
    return GoogleTranslator(source='auto', target=origin_lang).translate(text)



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
