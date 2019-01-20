from bs4 import BeautifulSoup
import sys, requests
import pickle, os, json

def getIDs():
    return {"BreitbartNews":"457984599"}

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


    title = ""

    for fu in myArticle.find_all('h1'):
        title = fu.text

    siteText = ""

    for fu in myArticle.find_all('p'):
        siteText += fu.text
        siteText += '\n'
    title = title.replace('/', ' ')

    article = {}
    article["title"] = title
    article["text"] = siteText
    article["url"] = url

    #print ("currrent title: " + title)

    #print ("writing to destination")

    with open(destination + "/" +title + ".json", "w") as outfile:
        json.dump(article, outfile, indent=4)

    return article
