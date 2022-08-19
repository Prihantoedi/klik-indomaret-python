from flask import Flask
from flask import request

from flask.globals import request

from scrapper import fetchProducts, productDetail


app = Flask(__name__)

app.config["DEBUG"] = True # do not use this in production level

# use the route like this: /api/v1/search/products?product-name=yourproductname
@app.route("/api/v1/search/products", methods=["GET"])
def search_product():
    keyword = request.args.get("product-name")    
    getProductsInfo = fetchProducts(keyword)

    return getProductsInfo, 200

@app.route("/api/v1/product/detail", methods=["GET"])
def product_detail():
    target = request.args.get("target-link")
    getProductDetail = productDetail(target)
    
    return getProductDetail, 200

if __name__ == "__main__":
    app.run()