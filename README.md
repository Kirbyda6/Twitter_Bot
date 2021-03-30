# Babel Bot
https://twitter.com/hackORproject
https://youtu.be/gVMVFJgX6yU

![Capture](https://user-images.githubusercontent.com/54118319/112742794-8d497a00-8f5f-11eb-88f7-04858e5e0523.PNG)

## Inspiration
The inspiration to build Babel Bot comes from one of Babel Bot's creators who had heard of a similar concept in which poems were passed into a translation platform repeatedly, with different languages each iteration, before being returned to the original language. Reading how those various iterations of languages modified the original poem sparked the idea to create a Twitter bot that would automatically run these translations and reply with the (often humorous) result to any user who tweeted at it.

## What it does
Public twitter accounts can tweet at Babel Bot (@hackorproject) any phrase of a uniform language. Babel bot then translates this phrase repeatedly, in real-time, to 10 different languages. Finally, Babel bot converts the phrase back into the native language of the original tweet and replies to the user.

## How we built it
Babel bot was built with Python 3.9 and the frameworks Tweepy and deep_translator. Tweepy allows Python to directly interact with Twitter API and allows Babel Bot to monitor mentions real-time through streams, get twitter user data, and post replies/status updates. The module deep_translator allows Babel Bot to identify the language of the incoming user tweet data and also translate it to one of the 107 available languages in the Google Translate API.

## Challenges we ran into
One of the core issues with building Babel Bot was implementation of the translation functionality with various API's. Most Python module based translation API's set limits on the number of translations executed per hour. In the development phase we found this to be a challenge and ultimately identified deep_translator as a our go-to module as it has unlimited translations.

Another challenge we ran into was learning to work together over Github. None of us had collaborated with other coders until this project. We had to learn and apply how to create new branches, merge branches, review each other's code, and keep our local code up-to-date with the remote main. We had one big moment of confusion when we realized some of the master branch's code had been accidentally overwritten, but we were able to sort it out and keep going.

## Accomplishments that we're proud of
We are proud of a few things coming out of this project. First, as a team, being able to work in a collaborative manner to break down problems, trouble-shoot code and communicate ideas was a big accomplishment for all of us since this is our first collaborative coding experience. Second, being able to break down an API and understand the underlying mechanics so that we could use them for our own purposes was a pretty big accomplishment. Third, coming out of this experience with our idea working as imagined is a huge win!

## What we learned
We learned how to collaborate via GitHub and use the Python frameworks Tweepy and deep_translator.

## What's next for Babel Bot
Some of the ideas going forward with Babel Bot include: identifying how to run the program continuously on some server environment and adding additional functionality such as self generation of own status (i.e. poems translated, etc.).

## Built With
#### python: https://www.python.org/
#### deep-translator: https://github.com/nidhaloff/deep-translator  
#### tweepy: https://github.com/tweepy/tweepy
