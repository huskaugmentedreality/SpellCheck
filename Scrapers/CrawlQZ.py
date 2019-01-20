from bs4 import BeautifulSoup
import sys, requests
import os
import pickle, os
import json

def getIDs():
    return {"qz":"573918122"}

def getArticle(destination, url):
    title = ''
    print ("got request for: " + url)
    page = requests.get(url)
    myArticle = BeautifulSoup(page.text, 'html.parser')
    
    url = ""
    try:
        urlStuff = myArticle.find("meta", {"property":"og:url"})
        print(urlStuff["content"])
        url = urlStuff["content"]
        if url.startswith("https://twitter.com"):
            print ("It's a Tweet")
            return {}


    except:
        print ("can't find url")
        pass


    title = myArticle.find("title")
    if title:
        title = title.text
    else:
        return


    siteText = ""
    for p in myArticle.find_all("p"):
        if p.text.startswith("Additional reporting"):
            continue
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

#getArticle("./test", "https://qz.com/africa/1528663/zimbabwe-intnerent-shutdown-leads-to-vpn-use/")
