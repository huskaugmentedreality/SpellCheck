from bs4 import BeautifulSoup
import sys, requests
import os, pickle
import json

def getIDs():
    return {"washingtonpost":"2467791"}

def getArticle(destination, url):
    try:
        article = {}
        title = ''
        page = requests.get(url)
        myArticle = BeautifulSoup(page.text, 'html.parser')
        
        url = ""
        try:
            urlStuff = myArticle.find("meta", {"property":"og:url"})
            print (urlStuff["content"])
            url = urlStuff["content"]
            if url.startswith("https://twitter.com"):
                print ("It's a Tweet")
                return {}

        except:
            print ("couldn't find url in BG")
            pass
        
        for fu in myArticle.find_all('h1'):
            title = fu.text

        siteText = ""
        for fu in myArticle.find_all('p'):
            siteText += fu.text
            siteText += '\n'

        title = title.replace('/', '_')

        article["title"] = title
        article["text"] = siteText
        article["url"] = url

        with open(destination + "/" + title + ".json", "w") as outfile:
            json.dump(article, outfile)
        return article

    except:
        print ('error with ' + url)
        pass
