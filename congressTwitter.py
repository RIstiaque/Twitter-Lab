##################
# congressTwitter.py
# Rifatul Istiaque
##################

# Code credit (and thanks) to Dan Nguyen of the Stanford Journalism program!
import json
import os
import requests
import tweepy
import csv

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
     return tweepy.API(auth)

def csvObj():
     """
     This will assign serving congress members' names to their
     twitter handles using a dictionary.
     Arguments:
     None.
     Returns:
     A dictionary with congress memembers' names as keys, and their twitter handles as values.
     """
     CSV_URL = "http://unitedstates.sunlightfoundation.com/legislators/legislators.csv"
     s = requests.get(CSV_URL) # Download the csv using requests.
     reader = csv.DictReader(s.text.splitlines(), lineterminator="\n") # Use the dictreader to make a dictionary with the attribute name paired with the rows value for that attribute.
     name2twitter_id = {}
     for row in reader:
          if (row['in_office'] == "1" and row['twitter_id'] != ""):
               name = row['firstname'] + " " # Construct the name.
               if (row['middlename'] != ""): # Not all names have middle names.
                    name += row['middlename'] + " "
               name += row['lastname']
               name2twitter_id[name] = row['twitter_id'] # Assign the name to their handle.
     del name2twitter_id["Tim Murphy"] # This representative does not have an active twitter handle. 
     name2twitter_id["Gregory W. Meeks"] = "RepGregoryMeeks" # Insert this representatives twitter handle manually.
     return name2twitter_id

def followers(congressDict, twitterAPI):
     """
     This function will find out which congress member has the
     most followers and which has the least.
     Input:
     congressDict: Dictionary of Congress Members paired with their
     twitter handles.
     twitterAPI: A tweepy object.
     Returns:
     A list containing the names for congress members that
     have the most followers, and one that has the least.
     """
     most = twitterAPI.get_user(list(congressDict.items())[0][1]) # Choose an arbitrary starting point from the dictionary and assign it their user details.
     least = most
     for name in congressDict:
        tempAPI = twitterAPI.get_user(congressDict[name]) # Get the user details of each congress members' twitter handle.
        numFollowers = tempAPI._json['followers_count']
        if (numFollowers > most._json['followers_count']): # If the follower count is greater than most, replace the user details with current one.
            most = tempAPI
        elif (numFollowers < least._json['followers_count']): # If the follower count is lower than least, replace the user details with the current one.
            least = tempAPI
     return [most._json["name"], least._json["name"]]

def totFavandRetweets(congressDict, twitterAPI):
     """
     This function will go through the last ten tweets of
     each congress member and report the total number of
     retweets and favorites for all ten.
     Input:
     congressDict: A dictionary consisting of the congress
     members' name and twitter handle.
     twitterAPI: the twitter API object.
     Output:
     FandRDict: A dictionary where the keys are the congress
     members' names, and the values are a list consisting of
     the total # of favorites and # of retweets for their last
     ten tweets.
     """
     FandRDict = {}
     for name in congressDict:
          FandRDict[name] = [0, 0] # Assign a beginning value for each congress member.
          for status in twitterAPI.user_timeline(screen_name=congressDict[name], count = 10): # Parse through each tweet's detais.
               FandRDict[name] = [FandRDict[name][0] + status._json["favorite_count"] # Add the current tweets fav. and rt's to the current value.
                                  ,FandRDict[name][1] + status._json["retweet_count"]]
     return FandRDict

def main():
    fIn = open("congressTwitter.txt", "w", encoding='utf-8')
    tweepyAPI = get_api() # Receive the twitter API.
    congressDict = csvObj() # A dictionary pairing conrgress members to their twitter handles.
    followersList = followers(congressDict, tweepyAPI) # A list containing the names of congress members with the most followers and the least.
    fIn.write("Most followers: " + followersList[0] + "\n") # Writes the name to the text file.
    fIn.write("Least followers: " + followersList[1] + "\n")    
    FandRDict = totFavandRetweets(congressDict, tweepyAPI) # Dictionary that has keys of congress members' names and values of their total # of rts and favorites over their last 10 tweets.
    for name in FandRDict:
         fIn.write(name + "'s last 10 tweets: " + str(FandRDict[name][0]) # Writes this data to the text file.
                   + " favorited, " + str(FandRDict[name][1]) + " retweeted.\n")

main()
