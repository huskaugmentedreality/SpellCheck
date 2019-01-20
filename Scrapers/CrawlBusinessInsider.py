from bs4 import BeautifulSoup
import sys, requests
import os, pickle, json

def getIDs():
    return {"businessinsider":"20562637"}

def getArticle(destination, url):

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

    siteText =""

    paragraphs = myArticle.find_all("p")

    if paragraphs:
        for p in paragraphs:
            if p.text.startswith('Business Insider will'):
                continue
            if p.text.startswith('Find out why'):
                continue
            siteText += p.text
            siteText += '\n\n'

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
