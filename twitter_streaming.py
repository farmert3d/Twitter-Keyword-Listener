#twitter_streaming.py
#Taylor Farmer
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import smtplib
import email.utils
from email.mime.text import MIMEText
import json
import csv
#Variables that contains the user credentials to access Twitter API
access_token = "REDACTED"
access_token_secret = "REDACTED"
consumer_key = "REDACTED"
consumer_secret = "REDACTED"
# Reading the tweet, followed by making a word list, checking for matches, then sending email if there is a match.
class StdOutListener(StreamListener):
    # tweet listener
    def on_data(self, data):
        wordList = []
        try:
            # JSON from tweet
            info = json.loads(data)
            tweet = info['text'].encode("utf-8")
        except:
            print("-----An error occured while reading a tweet-----")
        # Creating the word list array based on words in Applications.txt
        wordList = [line.rstrip() for line in open('Applications.txt')]
        # Checking if tweet was a retweet
        if "RT @CVEnew" not in tweet:
            # Creating a loop that goes over every word in wordlist
            for word in wordList:
                # a lop checking if each word, which comes from wordlist, is in the tweet.
                if word in tweet:
                    print tweet
                    print "word: " + word
                    # Create the message.
                    msg = MIMEText(tweet)
                    msg['To'] = email.utils.formataddr(('REDACTED_NAME', 'REDACTED_TO@REDACTED.com'))
                    msg['From'] = email.utils.formataddr(('REDACTED_FROM_NAME', 'REDACTED_FROM@REDACTED.com'))
                    msg['Subject'] = 'REDACTED_SUBJECT'
                    # SMTP() is used with normal, unencrypted (non-SSL) email.
                    server = smtplib.SMTP()
                    # specify which mail server we wish to connect to.
                    server.connect ('REDACTED.org', 25)
                    # the first email is our envelope address and specifies the return path for bounced emails.
                    try:
                        server.sendmail('REDACTED_FROM@REDACTED.com', ['REDACTED_TO@REDACTED.com'], msg.as_string())
                    finally:
                        server.quit()
                    # Return for if statment
                    return True
    print "running..."
    # error handling for tweet listener
    def on_error(self, status):
        print status
#This handles Twitter authetification and the connection to Twitter Streaming API
if __name__ == '__main__':
    try:
        l = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, l)
        # user ID for CVENew 821806287461740544
        # user ID for my test account REDACTED
        stream.filter(follow = ['821806287461740544'])
    except:
        print ("-----An error occured while following the stream-----")
        try:
            l = StdOutListener()
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            stream = Stream(auth, l)
            # user ID for CVENew 821806287461740544
            # user ID for my test account REDACTED
            stream.filter(follow = ['821806287461740544'])
        except:
            print "-----A second error occured while following the stream-----"
