# SpellCheck


Download files. You need to put your own Twitter API keys into keys.json (there's 4)

It'll complain about any missing dependencies (python3); just install them.

To run, run RunTwitterAPI.py. It uses the thingies in Articles to crawl twitter and download news articles. It uses SpellCheck to identify possible typos and save the typos as .json files. You're going to need to install a lot of libraries.

To run the tweets, run tweetPending.py. It goes through the .json files and lets the user verify typos; it then tweets the typos when requested.

Also, delete test.json out of the tweets and pendingTypoTweets folders; github won't allow me to upload empty folders and I'm not going to go have them mkdir like I should.
