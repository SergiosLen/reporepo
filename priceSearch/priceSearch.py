from flask import Flask,json, Response,jsonify,request

from loadcsvjson import data

app= Flask(__name__)



@app.route('/')
def hello_from_api():
    return 'Returns json file of products use /products for a list of all products, /products/product_id  for the product itself'
@app.route('/products')
def api_products():
    resp= jsonify(data)
    resp.status_code= 200
    return resp
    # js= json.dumps(data)
    # resp= Response(js, status=200, mimetype='application/json')
@app.errorhandler(404)
def not_found(error= None):
    message = {
            'status': 404,
            'message': 'Not found ' + request.url,
    }
    resp= jsonify(message)
    resp.status_code = 404
    return resp

@app.route('/products/<productid>',methods =['GET'])
def api_product(productid):
    if productid in data:
        return jsonify(data[productid])
    else:
        return not_found()