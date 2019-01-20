from bs4 import BeautifulSoup
import sys, requests
import os
import pickle, os
import json

def getIDs():
    return {"bostonglobe":"95431448"}

def getArticle(destination, url):
    title = ''
    print ("got request for: " + url)
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

    title = myArticle.find("title")
    if title:
        title = title.text
    else:
        return


    siteText = ""
    for p in myArticle.find_all("p"):
        siteText += p.text
        siteText += '\n'

    print ("got here")

    title = title.replace('/', '_')

    article = {}
    article["title"] = title
    article["text"] = siteText
    article["url"] = url


    with open(destination + "/" + title + ".json", "w") as outfile:
        json.dump(article, outfile)
    return article

