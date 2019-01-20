from bs4 import BeautifulSoup
import sys, requests, os, pickle
import json

def getIDs():
    return {"CNN":"759251"}

def test():
    fh = open ("test_output/test.text", "r")
    myText = fh.read()
    fh.close
    print ("zomg I'm alive!w00t")
    return getArticle (".", myText, test_parse=True)

def getArticle(destination, url, test_parse = False):
    #print ("in here")

    if not test_parse:
        if url.startswith("//"):
            url = "http:" + url
        #print ("Current request: " + url)

        title = ''
        page = requests.get(url)
        myArticle = BeautifulSoup(page.text, 'html.parser')
    
    if test_parse:
        myArticle = BeautifulSoup(url, 'html.parser')

    #print ("made it here")

    url = ""
    try:
        urlStuff = myArticle.find("meta", {"itemprop":"url"})
        print(urlStuff["content"])
        url = urlStuff["content"]
        if url.startswith("https://twitter.com"):
            print ("It's a Tweet")
            return {}


    except:
        print ("can't find url")
        pass


    title = ""

    for fu in myArticle.find_all('h1'):
        title = fu.text.strip()

    #print ("made it past title")

    siteText = ""
    body_missing = True
    tryBody = myArticle.find_all(class_="zn-body__paragraph")
    if tryBody:
        for fu in tryBody:
            if not (fu.text == ''):
                body_missing = False
            siteText += fu.text
            siteText += '\n'

    elif myArticle.find_all(class_="Paragraph__component"):
        #print ("in second")
        tryBody = myArticle.find_all(class_="Paragraph__component")
        if tryBody:
            for fu in tryBody:
                if not (fu.text == ''):
                    body_missing = False
                siteText += fu.text
                siteText += '\n'
    #print ("made it past parafgraphs")

    if (body_missing):
        siteText = "Could not read: " + url
        print ("CouLD NOT READ: " + url)
        return

    title = title.replace('/', '')
    if len(title) > 40:
        title = title[:40]

    article = {}
    article["title"] = title
    article["text"] = siteText
    article["url"] = url

    #print ("currrent title: " + title)

    #print ("writing to destination")

    with open(destination + "/" +title + ".json", "w") as outfile:
        json.dump(article, outfile, indent=4)

    return article
