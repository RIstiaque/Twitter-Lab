##################
# getTwitterData.py
# Rifatul Istiaque
##################

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import os
import json
import time

DEFAULT_TWITTER_CREDS_PATH = '\creds\me.json' # put your file here!
def get_api(credsfile = DEFAULT_TWITTER_CREDS_PATH):
     """
     Takes care of the Twitter OAuth authentication process and
     creates an API-handler to execute commands on Twitter
     Arguments:
     - credsfile (str): the full path of the filename that contains a
     JSON file with credentials for Twitter
     Returns:
     A tweepy.api.API object
     """
     fn = os.getcwd() + credsfile
     c = json.load(open(fn, "r"))
     # Get authentication token
     auth = tweepy.OAuthHandler(consumer_key = c['consumer_key'],
     consumer_secret = c['consumer_secret'])
     auth.set_access_token(c['access_token'], c['access_token_secret'])
     # create an API handler
     return auth

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This listener will record all the tweet's hashtags that have one or more
    of our tracked hashtags into a json file.
    """
    def __init__(self, time_limit=600):
        """
        This initializes the json file to write to as well
        as stopping the stream after 10 minutes have elapsed.
        """
        self.start_time = time.time() # Define the starting time.
        self.limit = time_limit
        self.lstOfLsts = [] # Initialize a list for the tweets' hashtags to be stored to.
        self.fIn = open('trump.json', 'a') # Open .json file to write to.
        
    def on_data(self, data):
        """
        This will continously retrieve tweets from the twitter stream
        that have one or more of the filtered hashtags into it. Then
        it will them all into a list of lists structure and write that
        information into a .json file.
        """
        ## Note - Twitter data being saved to json is ONLY a list of the tweets' hashtags. ## 
        if (time.time() - self.start_time) < self.limit: # Check if 10 minutes has elapsed.
            data = json.loads(data) # Load the data.
            self.lstOfLsts.append(data['entities']['hashtags']) # Put the hashtag information for that tweet into the list.
            return True # Return true so steam continues.
        else:
            self.fIn.write(json.dumps(self.lstOfLsts)) # Converts the list of lists to a json appropriate format and then write it to file.
            self.fIn.write("\n") # Add a newline character or else an error occurs during reading.
            self.fIn.close()
            return False # Ends stream.

    def on_error(self, status): # Check what kind of error occurs.
        print(status)

def main():
    auth = get_api() # Get proper credentials to twitter in order to use Oauth.
    stream = Stream(auth, StdOutListener()) # Initialize a stream.
    stream.filter(track=['#trump','#maga','#resist','#impeachtrump' # Choose which hashtags to filter on.
                         ,'#donaldtrump','#potus','#deplorables'])
    
main()
