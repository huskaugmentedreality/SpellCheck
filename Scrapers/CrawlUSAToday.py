from bs4 import BeautifulSoup
import sys, requests
import os, pickle, json

def getIDs():
    return {"USATODAY":"15754281"}

def getArticle(destination, url):
    page = requests.get(url)
    myArticle = BeautifulSoup(page.text, 'html.parser')
    #open('./Original/' + url.split('/')[-1], 'w').write(str(myArticle))

    url = ""
    try:
        urlStuff = myArticle.find("link", {"rel":"canonical"})
        print (urlStuff["href"])
        url = urlStuff["href"]
        if url.startswith("https://twitter.com"):
            print ("It's a Tweet")
            return {}

    except:
        print ("couldn't find url")
        pass

    title = myArticle.find("title")
    if title:
        title = title.text

    siteText = ""

    paragraphs = myArticle.find_all("p")

    if paragraphs:
        for p in paragraphs:
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
