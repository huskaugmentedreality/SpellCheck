# SpellCheck


Download files. You need to put your own Twitter API keys into keys.json (there's 4)

It'll complain about any missing dependencies (python3); just install them.

To run, run SpellCheck.py. It uses the thingies in Articles to crawl twitter and download news articles. It uses SpellCheck to identify possible typos and save the typos as .json files.

To run the tweets, run tweetPending.py. It goes through the .json files and lets the user verify typos; it then tweets the typos when requested.
