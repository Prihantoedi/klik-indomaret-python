from flask import Flask
from flask import request

from flask.globals import request

from scrapper import fetchProductInfo


app = Flask(__name__)

app.config["DEBUG"] = True # do not use this in production level

# keyword = input("input your keyword here:")
# getInfo = scrapPageContent(keyword)


@app.route("/api/v1/search/products", methods=["GET"])
def search_product():
    keyword = request.args.get("product-name")
    
    getProductsInfo = fetchProductInfo(keyword)
    return getProductsInfo, 200



if __name__ == "__main__":
    app.run()