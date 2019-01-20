from bs4 import BeautifulSoup
import sys, requests
import os, pickle, json

def getIDs():
    return {"dcexaminer":"18956073"}

def getArticle(destination, url):

    page = requests.get(url)
    myArticle = BeautifulSoup(page.text, 'html.parser')
    #open('./Original/' + url.split('/')[-1], 'w').write(str(myArticle))

    #try to find URL:
    url = ""
    try:
        urlStuff = myArticle.find("link", {"rel":"canonical"})
        print(urlStuff["href"])
    
    except:
        print ("can't find url")
        pass


    title = myArticle.find("title")

    if title:
        title = title.text
    else:
        return ""

    siteText = ""

    paragraphs = myArticle.find_all("p", class_=False)

    if paragraphs:
        for p in paragraphs:
            siteText += p.text
            siteText += '\n\n'

    print ("got here")

    title = title.replace('/', '_')
    if len(title) > 40:
        title = title[:40]

    article = {}
    article["title"] = title
    article["text"] = siteText

    #print ("currrent title: " + title)

    #print ("writing to destination")

    with open(destination + "/" + title + ".json", "w") as outfile:
        json.dump(article, outfile, indent=4)

    return siteText
