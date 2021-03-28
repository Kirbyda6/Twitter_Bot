import tweepy
import secrets
import random
import re
from deep_translator import GoogleTranslator, single_detection


class MentionListener(tweepy.StreamListener):
    """Represents the listener that accesses the flow of data from twitter"""

    def on_data(self, data):
        """Receives mentions, storing the tweet ID, text, and username in order to write and send a reply to the user."""
        tweet_id = self.get_tweet_id(data)
        tweet_text = self.get_tweet_text(data)

        # Sends a reply to the user
        user_beg = re.search('"screen_name":"', data).end()
        user_end = re.search('"location"', data).start() - 2
        user = data[user_beg:user_end]
        
        api.update_status('@' + user + ' ' + translate(tweet_text), tweet_id)
        print("Reply tweet sent.")
        return True

    def get_tweet_id(self, data):
        """Returns the tweet ID as a string"""
        result = re.search('"id":\d+', data)
        return result.group()[5:]

    def get_tweet_text(self, data):
        """Returns the text content of the tweet as a string"""
        text_beg = re.search('"text":', data).start() + 8
        text_end = re.search('"source":', data).start() - 2
        tweet_text = data[text_beg:text_end].lower()

        # Dict containing the tag, newline, and double spaces that need to be replaced
        str_to_replace = {'@hackorproject': '', r'\n': ' ', '  ': ' '}

        for key, value in str_to_replace.items():
            # Replace key string with value string in the text
            tweet_text = tweet_text.replace(key, value)

        print("Tweet received. Running through translator...")
        
        return tweet_text

    def on_error(self, status_code):
        """If an error code is received, returns false to disconnect the stream."""
        if status_code == 420:
            print("Error code: 420 - something went wrong. Disconnecting from stream.")
            return False


class MentionStream:
    """Filters out mentions, i.e. only pays attention to the data we want"""
    
    def __init__(self, auth, listener):
        """creates a MentionStream object using auth code and the MentionListener object"""
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start(self):
        """starts the stream and detects when someone mentions @hackORproject on twitter"""
        self.stream.filter(track=['@hackORproject'])


# A list of language codes according to ISO 639-1 codes - use for random translations
lang_dict = GoogleTranslator.get_supported_languages(as_dict=True)
lang_codes = list(lang_dict.values())

def translate(text):
    """
    Takes a string of text as a parameter and translates it through 10 random languages and back to the original 
    detected language, returning the final translation.
    """
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
