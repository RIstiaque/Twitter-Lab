##################
# trumpTweets.py
# Rifatul Istiaque
##################

import json

def tagDict(fIn, fOut):
    """
    This function make a dictionary that has all the tags paired
    with how long they were used and will find the length of the
    largest tag. This buffer will be used to print in a neat format.
    Input:
        fIn: File to get tag data from.
        fOut: File to print to.
    Output:
        hashtagDict: Dictionary that contains tags paired with the # of times used.
        buffer: Length of the largest tag.
    """
    hashtagDict = {} # Initializing values.
    buffer = 0 
    for lst in range(len(fIn)): # Parses through each tweet.
        for pair in range(len(fIn[lst])): # Parses through each hashtag.
            hashtag = (fIn[lst][pair]["text"]).lower() # Make all hashtags to lower because twitter doesn't differentiate.
            if len(hashtag) > buffer: # Update buffer.
                buffer = len(hashtag)
            if hashtag in hashtagDict: # Increment existing tag 
                hashtagDict[hashtag] += 1
            else: # Create a new key
                hashtagDict[hashtag] = 1
    fOut.write("A total of " + str(len(fIn)) + " tweets were analyzed.\n") # writes how many tweets were analyzed.
    return hashtagDict, buffer

def popularTags(tagsAndBuffer, fOut):
    """
    Finds the 15 most popular tags amongst
    the analyzed tweets and prints out the
    tag and how many times they were called.
    Input:
        tagsAndBuffer: A tuple containing a dictionary(hashtagdict) and an int(buffer)
        fOut: File to write to.
    Output:
        No output.
    """
    hashtagDict = tagsAndBuffer[0] # Initialize variables.
    buffer = tagsAndBuffer[1]
    popularTags = []
    fOut.write("Hashtag" + " "*(buffer-len("Hashtag")) + "Count\n") # Header to serve as a guide for later prints.
    for i in range(15): # Go through dictionary 15 times.
        tag = "" 
        val = 0 # Comparative variable for popularity.
        for key in hashtagDict:
            if (hashtagDict[key] > val and key not in popularTags): # Find keys that are the most popular and not in the list already.
                tag = key # Update variables
                val = hashtagDict[tag]
        popularTags.append(tag) # Add the hashtag to the list.
        keybuff = " "*(buffer-len(tag)) # Create a buffer from the hashtag length.
        fOut.write(tag + keybuff + str(hashtagDict[tag]) + "\n") # Write to output file.

def main():
    fIn = json.load(open("trump.json", "r")) # Open json file
    fOut = open("presStats.txt", "w") # Open output file
    tagsAndBuffer = tagDict(fIn, fOut) 
    popularTags(tagsAndBuffer, fOut)
    fOut.close()
    
main()
