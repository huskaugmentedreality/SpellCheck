from bs4 import BeautifulSoup
import sys, requests
import os, pickle, json

def getIDs():
    return {"thehill":"1917731"}


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
        print ("couldn't find url in BG")
        pass


    title = myArticle.find("title")
    if title:
        title = title.text

    siteText = ""

    paragraphs = myArticle.find_all("p", class_=False)

    if paragraphs:
        for p in paragraphs:
            siteText += p.text
            siteText += '\n'

    title = title.replace('/', '_')

    article = {}
    article["title"] = title
    article["text"] = siteText
    article["url"] = url


    with open(destination + "/" + title + ".json", "w") as outfile:
        json.dump(article, outfile)
    return article

