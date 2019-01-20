import os, sys, json

# raw_input returns the empty string for "enter"
yes = {'yes','y', 'ye'}
no = {'no','n'}

import tweepy
import json

with open('keys.json', 'r') as outfile:
    keys = json.load(outfile)

CONSUMER_KEY = keys["CONSUMER_KEY"]
CONSUMER_SECRET = keys["CONSUMER_SECRET"]
ACCESS_TOKEN = keys["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = keys["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)


def qaqctweet(file_name, myDict):

    typos = list(myDict.keys())
    contexts = list(myDict.values())
    
    target_username = file_name.split("_")[0]
    target_id = file_name.split("_")[1][:-5]

    print (target_id)

    ready = False
    answers = []
    tweetText = ""

    while(not ready):
        answers = []
        for typo in myDict:
            print("Answers so far " + str(answers))
            while (True):
                print ("is " + typo + " misspelled in the context of " + myDict[typo] + "?")
                choice = input().lower()
                if choice in yes:
                    answers.append(1)
                    break
                elif choice in no:
                    answers.append(0)
                    break
                else:
                    print("Please respond with 'yes' or 'no'")

        
        if sum(answers) > 0:
            print ("Replying to " + target_username + " that:")
            if sum(answers) > 1:
                tweetText = "@" + target_username + " You may have some typos in the article; are these words? "
                for i in range(len(answers)):
                    if answers[i]:
                        tweetText += "\"" + typos[i] + "\" "
            else:
                tweetText = "@" + target_username + " You may have a typo in the article; is this the word you wanted? "
                for i in range(len(answers)):
                    if answers[i]:
                        tweetText += "\"" + typos[i] + "\" "

            print (tweetText)
            print ("Is that accurate?")
            choice = input().lower()
            if choice in yes:
                ready = True
                api.update_status(status=tweetText, in_reply_to_status_id=target_id)
                os.remove("pendingTypoTweets/" + file_name)

                break
            elif choice in no:
                ready = False
            else:
                print("Please respond with 'yes' or 'no'")
                
        else:
            print ("Delete without tweeting?")

        choice = input().lower()
        if choice in yes:
            ready = True
            os.remove("pendingTypoTweets/" + file_name)
            break
        elif choice in no:
            ready = False
        else:
            print("Please respond with 'yes' or 'no'")


    if sum(answers) > 0:
        print (tweetText)


pending = "pendingTypoTweets"
targetfiles = os.listdir(pending)
for tar in targetfiles:
    full_path = pending + "/" + tar
    print(tar)
    with open(full_path, "r") as infile:
        newDict = json.load(infile)
    qaqctweet(tar, newDict)

