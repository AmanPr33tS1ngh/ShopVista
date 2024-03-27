from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/ShopVista"
app.config['JWT_SECRET_KEY'] = os.urandom(24)
jwt = JWTManager(app)

mongo = PyMongo(app).db


@app.route("/check/", methods=["POST"])
@jwt_required()
def index():
    current_user = get_jwt_identity()
    return jsonify({'success': True, 'user': current_user})


@app.route("/sign_in/", methods=["POST"])
def sign_in():
    user = request.json.get("user")
    if not user:
        return jsonify({'success': False, 'msg': "Please provide both username and password"})
    
    username = user.get('username')
    password = user.get('password')
    
    user = mongo.users.find_one({"username": username, "password": password})
    print(user)
    if not user:
        return jsonify({'success': True, 'msg': "User not found!"})
    
    access_token = create_access_token(identity=username)

    return jsonify({'success': True, 'msg': "sign in successful", 'access_token': access_token})


@app.route("/sign_up/", methods=["POST"])
def sign_up():
    user = request.json.get('user')
    if not user:
        return jsonify({"success": False, 'msg': "Please enter all details"})
    
    user_exists = mongo.users.find_one({"$or": [{"username": user.get('username')}, {"email": user.get('email')}]})
    if user_exists:
        return jsonify({"success": False, 'msg': "User already exists with same username/email"})
    
    mongo.users.insert_one(user)
    return jsonify({'success': True, 'msg': "user created"})

@app.route("/product/add/", methods=["POST"])
def add_product():
    product = request.json.get('product')
    if not product:
        return jsonify({"success": False, 'msg': "Please enter all details"})
    
    mongo.products.insert_one(product)
    return jsonify({'success': True, 'msg': "product created"})

@app.route("/products/", methods=["GET"])
def get_all_products():
    products = mongo.products.find({})
    
    print(products)
    if not products:
        return jsonify({"success": False, 'msg': "Products not found!"})
    return jsonify({'success': True, 'msg': "products!", 
                    'products': products
                    })


@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    print('id', id)
    if not id:
        return jsonify({'success': False, 'msg': 'Please provide id'})
    product = dict(mongo.products.find_one({'_id': id})) # get all
    if not product:
        return jsonify({"success": False, 'msg': "Product not found"})
    
    return jsonify({'success': True, 'msg': "product!", 'product': product})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
    