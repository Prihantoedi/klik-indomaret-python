# import requests
import bs4 as bs
import json

from flask import jsonify

import urllib.request



def fetchTitlePrice(mySoup, myTag, className, myData, productNum, baseUrl):
    key = "product_"

    for div in mySoup.find_all(myTag, {"class" : className}):
        childContent = div.contents[1] 
        title = childContent.find("div", {"class" : "title"})
        price = childContent.find("span", {"class" : "normal price-value"})
    
        # get title, price and product link
        if title:
            myData[key + str(productNum)] = {"title" : title.text.replace("\n", ""), "price" : price.text, "link" : baseUrl + div.a["href"]}
            productNum+=1

    return myData, productNum


def fetchProductInfo(keyword):
    base_url = "https://www.klikindomaret.com"

    if " " in keyword:
        keyword = keyword.replace(" ", "'\'")

    url_with_keyword = base_url + "/search/?key=" + keyword

    # try:
    #     source = urllib.request.urlopen(url_with_keyword)
    #     soup = bs.BeautifulSoup(source, "lxml")
    # except:
    #     return {"error" : "Page not found"}, 404

    source = urllib.request.urlopen(url_with_keyword)
    soup = bs.BeautifulSoup(source, "lxml")
    data = {}
    prodNum = 1

    nextPage = True

    newSource = ""
    while nextPage:
        data, prodNum = fetchTitlePrice(soup, "div", "item", data, prodNum, base_url)

        for a in soup.find_all("a"):
            

            # fetch all product info in page
            
            if a.has_key("href"):

                getContent = a.contents
                findSpan = getContent[0] # get child
                toStr = str(findSpan)
                if "<" in toStr and ">" in toStr:
                    if findSpan.has_key("class") and findSpan["class"] == ["next"]:
                        newSource = urllib.request.urlopen(a["href"])
                        break 
        
        if newSource == source or newSource == "":
            nextPage = False

        if nextPage:
            source = newSource
            soup = bs.BeautifulSoup(source, "lxml")
    
    if data == {}:
        return {"error" : "product not found"}
    else:
        return jsonify(data)