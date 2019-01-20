from bs4 import BeautifulSoup
import sys, requests
import os, pickle
import json

def getIDs():
    return {"nytimes":"807095"}

def getArticle(destination, url):
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
        print ("couldn't find url in NYT")
        pass


    title = ""
    for fu in myArticle.find_all('h1'):
        title = fu.text

    siteText = ""
    for fu in myArticle.find_all('p'):
        if fu.text == 'Supported by':
            continue
        if fu.text.startswith("By"):
            if len(fu.text.split()) == 3:
                continue
        if fu.text.startswith("A look from across the New York Times"):
                continue
        if fu.text == "SEE SAMPLE":
            continue
        if fu.text == "Please verify you’re not a robot by clicking the box.":
            continue
        if fu.text == "Invalid email address. Please re-enter.":
            continue
        if fu.text == "You must select a newsletter to subscribe to.":
            continue
        if fu.text == "* Required field":
            continue
        if fu.text == "View all New York Times newsletters.":
            continue
        if fu.text != 'Advertisement':
                if not str(fu).startswith("<p class=\"byline-dateline\">"):
                    siteText += fu.text
                    siteText += '\n'
    title = title.replace('/', '_')
    if len(title) > 40:
        title = title[:40]

    article = {}
    article["title"] = title
    article["text"] = siteText
    article["url"] = url

    with open(destination + "/" + title + ".json", "w") as outfile:
        json.dump(article, outfile)

    return article

