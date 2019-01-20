# -*- coding: utf-8 -*-

import os, datetime, sys
import tweepy
import pickle
import json


#This gets today's date and sets some variables
today = datetime.datetime.now().strftime("%Y%m%d")

history = {}

#this first bit of code goes and checks the Scraper directory for the files to scrape
#articles from different publishers

scraperDir = "Scrapers"
destDir = "Articles"
artDir = today +"_Articles"


def setupDirs():

    #this is where it'll dump article directories for today. It'll be within /Articles/
    artDir = today +"_Articles"

    #this is the first level directory it'll look for or make to dump, can change
    destDir = "Articles"

    #this is where the actual scraper python files are located
    scraperDir = "Scrapers"
    loaded_sites = 0

    #appending the path to the scrapers will allow me to import them to use their <crawl> method
    sys.path.append("./" + scraperDir)
    sys.path.append(".")

    #check if we have scrapers (it doesn't return, it'll get an error later though if you don't)
    if scraperDir in os.listdir():
        print ("Found Scrapers")

    #check if the place to dump articles is here
    if destDir in os.listdir():
        print ("Found Article Folder")

    #if the place to dump articles isn't here, make it
    else:
        os.mkdir(destDir)
        print ("Created Articles Folder")

    #check if the place to dump article directories is in the articles folder
    if artDir in os.listdir(destDir):
        print ("Found Today's Folder")

    #if the place to dump article directories isn't there, make it
    else:
        os.mkdir("./" + destDir + "/" + artDir)

setupDirs()

# Query terms


def loadScrapers():
    name_dict = {}
    scrapers = {}

    #this is going to loop through all the scrapers, import them, and use them
    for k in os.listdir(scraperDir):
        #check if it's a python folder, if it is, it should be a scraper
        if k.endswith(".py"):
            scraper = __import__(k[:len(k)-3])
            test = scraper.getIDs()
            name_dict.update(test)
            scrapers[list(test.keys())[0]] = scraper
            os.makedirs(destDir + "/" + artDir + "/" + list(test.keys())[0], exist_ok=True)
    return name_dict, scrapers

name_dict, scrapers = loadScrapers()
#see what I loaded
print (str(name_dict))

#target is the array of publisher names
#pubs is the array of twitter IDs for each publisher twitter handle
#these were all imported along with the code to scrape articles from each publishers site
target = []
pubs = []
for key in name_dict:
    pubs.append(key)
    target.append(name_dict[key])

#The Twitter API keys are stored in a file called "keys.json". They're in a dict format.
with open('keys.json', 'r') as infile:
    keys = json.load(infile)

CONSUMER_KEY = keys["CONSUMER_KEY"]
CONSUMER_SECRET = keys["CONSUMER_SECRET"]
ACCESS_TOKEN = keys["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = keys["ACCESS_TOKEN_SECRET"]

#connects to tweepy which handles the tweeting
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

#load in the spellchecker
#it should be called SpellCheck.py
SpellCheck = __import__("SpellCheck")
spellcheck = SpellCheck.symspellpy()
spellcheck.init()

completed_urls = []

try:
    completed_urls = pickle.load(open("history.p", "rb"))
    print ("Loaded " + str(len(completed_urls)) + " completed urls!")
except:
    print ("Could not find history")
    pass


##Requests the actual HTML of an article linked to by a tweet
##Takes the following:
#publisher: the twitter handle of the news org
#tweet_path: where the tweet's gonna get saved
#tweet_id: identifier of the tweet for the publisher
#(the tweet itself can be found at twitter.com/publisher/status/tweet_id)
def getArticle(publisher, tweet_path, tweet_id):
    
    #this loads the tweet from where it's saved
    tweet = pickle.load( open(tweet_path, "rb" ))
    
    #This goes and pulls the url of the linked article from the saved tweet
    #I don't really get which of the things it is so I try b oth
    try:
        myURL = tweet.extended_tweet["entities"]["urls"][0]["url"]
    except:
        try:
            myURL = tweet.entities["urls"][0]["url"]
        except:
            print ("Couldn't Read Tweet")
            return
    
    print (myURL)

    #K, so the scrapers were all loaded into this scrapers dictionary by publisher so use
    #the right scraper to parse the HTML
    article = scrapers[publisher].getArticle(destDir + "/" + artDir + "/" + publisher, myURL)
    
    #The return should be a dict {"text", "url", "title"}
    #If there's no returning text that means it's bad
    try:
        text = article["text"]
    except:
        print ("\nNo Text Found\n\n")
        return
    try:
        url = article["url"]
        if url in completed_urls:
            print ("url previously scraped")
            return
        completed_urls.append(url)
    except:
        print ("URL not found in returned article dict")
        return

    #goes and saves the URL to history so I don't go and spam people
    pickle.dump(completed_urls, open("history.p", "wb"))

    #finally I go ahead and spellcheck it! It returns a dict of the bad words:sentences
    return spellcheck.findSuspiciousWords(text)

def prepTweet(tweetID, bad_words, good_words):
    print ("TweetID: " + tweetID)
    for i in len(bad_words):
        print (bad_words[i] + " may be a typo; did you mean " + good_words[i])

#this is the actual thing that does the tweet listening
class CustomStreamListener(tweepy.StreamListener):
    #when a tweet is found, print the info for the tweet
    def on_status(self, status):
        try:
            #there doesn't seem to be a better way to filter out replies; I'm checking if the tweeter is the account tweeted at
            if status.author.screen_name in pubs:
                print ("%s\t%s\t%s\t%s\n" % (status.text,
                                          status.author.screen_name,
                                          status.created_at,
                                          status.source,))
                tweet_path = status.author.screen_name + "_" + str(status.created_at) +".p"
                tweet_path = tweet_path.replace('/', '')
                tweet_path = "tweets/" + tweet_path
                pickle.dump(status, open(tweet_path, "wb" ))
                
                #This returns the typos; I'm not doing anything with them though!
                results = getArticle(status.author.screen_name, tweet_path, status.id)
    
            
            
        except:
            print ('Encountered Exception:')
            pass

    def on_error(self, status_code):
        print ('Encountered error with status code:', status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print ('Timeout...')
        return True # Don't kill the stream


def start():
    print ("starting")
    #feeds the class above to tweepy
    streaming_api = tweepy.streaming.Stream(auth, CustomStreamListener(), timeout=60)
    #prints out what it's pulling
    print ('Checking Twitter IDs "%s"\n\n\n' % target)
    #actually starts the twitter feed
    streaming_api.filter(follow=target)

start()
