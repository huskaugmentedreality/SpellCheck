from bs4 import BeautifulSoup
import sys, requests, time, os, pickle, json

def getIDs():
    return {"HuffPost":"14511951"}


def getArticle(destination, url):

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    myArticle = soup.find("div", {"id":"main"})
    
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
        return {}

    title = ""
    for fu in myArticle.find_all('h1'):
        title = fu.text

    siteText = ""

    for fu in myArticle.find_all('p'):
        siteText += fu.text
        siteText += '\n'

    title = title.replace('/', '_')

    article = {}
    article["title"] = title
    article["text"] = siteText
    article["url"] = url


    with open(destination + "/" + title + ".json", "w") as outfile:
        json.dump(article, outfile)
    return article

