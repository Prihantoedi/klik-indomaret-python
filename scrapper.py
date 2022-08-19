# import requests
import bs4 as bs
import json

from flask import jsonify

import urllib.request




def fetchProductInfo(mySoup, myTag, className, myData, productNum, baseUrl):
    key = "product_"

    for div in mySoup.find_all(myTag, {"class" : className}):
        childContent = div.contents[1] 
        title = childContent.find("div", {"class" : "title"})
        price = childContent.find("span", {"class" : "normal price-value"})
        image = childContent.find("img", {"class": "lazy"})
        
    
        # get title, price, image, and product link
        if title:
            myData[key + str(productNum)] = {"title" : title.text.replace("\n", ""), "price" : price.text, "img" : image["data-src"], "link" : baseUrl + div.a["href"]}
            productNum+=1

    return myData, productNum


def fetchProducts(keyword):
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
        data, prodNum = fetchProductInfo(soup, "div", "item", data, prodNum, base_url)

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


def productDetail(urlTarget):

    # target = "https://www.klikindomaret.com/product/doremi-hairandbody-wash-moisturizing"
    src = urllib.request.urlopen(urlTarget)
    sp = bs.BeautifulSoup(src, "lxml")

    description = []
    for div_desc in sp.find_all("span", {"class" : "spec_label"}):
        temp_desc = {}
        temp_desc["spec_label"] = div_desc.text
        nextSibling = div_desc.find_next("span")
        temp_desc["spec_desc"] = nextSibling.text
        description.append(temp_desc)


    promotion = []

    for div_prom in sp.find_all("div", {"id" : "information"}):
        promInfo = div_prom.find_all("span")
        temp = {}
        if len(promInfo) > 1:
            disc = promInfo[0].find("b")
            temp["head"] = disc.text
            temp["explain"] = promInfo[1].text
        else:
            temp["head"] = promInfo[0].text
            temp["explain"] = ""
        
        promotion.append(temp)


    return jsonify({"description": description, "promotion" : promotion})