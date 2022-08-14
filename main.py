# import requests

import bs4 as bs

import urllib.request


base_url = "https://www.klikindomaret.com"
keyword = "sabun"
source = urllib.request.urlopen(base_url + "/search/?key=" + keyword)
soup = bs.BeautifulSoup(source, "lxml")

data = {"title" : [], "price" : [], "link": []}
for div in soup.find_all("div", class_="item"):
    
    childContent = div.contents[1]
    title = childContent.find("div", {"class" : "title"})
    price = childContent.find("span", {"class" : "normal price-value"})
    # print(childContent)
    # link = childContent.find("a", href=True)
    # if link:
    #     print(link["href"])
    # print("=======================")


    if title:
        data["title"].append(title.text.replace("\n", ""))
        data["price"].append(price.text)
        # data["link"].append(link["href"])


# print(data)

