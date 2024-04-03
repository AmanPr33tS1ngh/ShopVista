from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_pymongo import PyMongo
import pandas as pd
from bson import ObjectId
import razorpay
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key' #os.urandom(24)
jwt = JWTManager(app)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/ShopVista'
mongo = PyMongo(app)

RZP_KEY = os.environ.get('RZP_TEST')
RZP_SECRET_KEY = os.environ.get('RZP_SECRET_KEY')

client = razorpay.Client(auth=(RZP_KEY, RZP_SECRET_KEY))

# serializer
def serializer(documents, many=False):
    if many:
        df = pd.DataFrame(list(documents))
        if '_id' in df.columns:
            df['_id'] = df['_id'].astype(str)
        serialized_documents = df.to_dict(orient='records')
        return serialized_documents
    serialized_document = dict(documents)
    serialized_document['_id'] = str(serialized_document['_id'])
    return serialized_document


# Routes
@app.route("/check/", methods=["POST"])
@jwt_required()
def index():
    current_user = get_jwt_identity()
    return jsonify({'success': True, 'user': current_user})


@app.route("/sign_in/", methods=["POST"])
def sign_in():
    users = mongo.db.users
    user_data = request.json.get("user")
    if not user_data:
        return jsonify({'success': False, 'msg': "Please provide both username and password"})

    username = user_data.get('username')
    password = user_data.get('password')

    user = users.find_one({'username': username, 'password': password})
    if not user:
        return jsonify({'success': False, 'msg': "User not found!"})

    access_token = create_access_token(identity=username)

    return jsonify({'success': True, 'msg': "sign in successful", 'access_token': access_token})


@app.route("/sign_up/", methods=["POST"])
def sign_up():
    users = mongo.db.users
    user_data = request.json.get('user')
    if not user_data:
        return jsonify({"success": False, 'msg': "Please enter all details"})
    user_exists = users.find_one({'username': user_data.get('username')})
    if user_exists:
        return jsonify({"success": False, 'msg': "User already exists with same username"})

    users.insert_one(user_data)
    return jsonify({'success': True, 'msg': "user created"})


@app.route("/update_profile/", methods=["POST"])
def update_profile():
    users = mongo.db.users
    user_data = request.json.get('user')
    if not user_data:
        return jsonify({"success": False, "msg": "Please provide user"})

    username = user_data.get('username')
    if not username:
        return jsonify({"success": False, "msg": "Please provide username"})

    user = users.update_one({"_id": ObjectId(user_data.get('_id'))}, {"$set": user_data})
    if not user.modified_count > 0:
        return jsonify({"success": False, 'msg': "Please enter all details"})
    return jsonify({'success': True, 'msg': "Data updated successfully"})


@app.route("/profile/", methods=["POST"])
def get_profile():
    users = mongo.db.users
    username = request.json.get('username')
    user_id = request.json.get('user_id')

    if not username:
        return jsonify({"success": False, "msg": "Please provide username"})

    user = users.find_one({"username": username})
    if not user:
        return jsonify({"success": False, 'msg': "User not found"})

    orders = mongo.db.orders
    user_orders = orders.find_one({"user_id": user_id}) or list()

    return jsonify({'success': True, 'msg': "User", 'user': serializer(user),
                    'orders': serializer(user_orders, many=True)})


@app.route("/products/", methods=["GET", "POST"])
def get_products():
    products = mongo.db.products
    user_id = request.json.get('user_id')
    if request.method == "POST":
        users = mongo.db.users
        admin = users.find_one({'user_id': user_id, 'is_admin': True})
        if not admin:
            return jsonify({"success": False, "msg": "You are not authorised to add products"})

        product_data = request.json.get('product')
        if not product_data:
            return jsonify({"success": False, 'msg': "Please enter all details"})

        products.insert_one(product_data)
        return jsonify({'success': True, 'msg': "product created"})

    result = products.find({})
    df = pd.DataFrame(list(result))
    if '_id' in df.columns:
        df['_id'] = df['_id'].astype(str)
    serialized_documents = df.to_dict(orient='records')
    # return serialized_documents
    print('resu', serialized_documents)
    return jsonify({'success': True, 'msg': "products!", 'products': serialized_documents
        # serializer(result, many=True)
        })

@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    if not id:
        return jsonify({'success': False, 'msg': 'Please provide id'})

    products = mongo.db.products
    product = products.find_one({'_id': ObjectId(id)})
    if not product:
        return jsonify({"success": False, 'msg': "Product not found"})

    return jsonify({'success': True, 'msg': "product!", 'product': serializer(product)})

@app.route("/cart/", methods=["GET", "POST"])
def get_cart():
    user_id = request.json.get("user_id")

    if not user_id:
        return jsonify({'success': False, 'msg': 'Please login'})

    users = mongo.db.users
    user = users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({"success": False, 'msg': "User not found"})

    carts = mongo.db.carts
    user_cart = carts.find_one({"user": user_id})
    if not user_cart:
        print('inserting...')
        user_cart = carts.insert_one({
            "user": user_id,
            "cart_items": [],
        })

    cart_items = user_cart.get("cart_items", [])
    df = pd.DataFrame(cart_items, columns=['_id'])
    cart_items_series = df['_id'].apply(lambda x: get_cart_items({'_id': ObjectId(x)})).tolist()
    cart_items = add_count_and_drop_duplicates(cart_items_series)
    print('cart_items', cart_items)
    return jsonify({'success': True, 'msg': "product!", 'cart_items': cart_items})


def add_count_and_drop_duplicates(cart_items_series):
    df = pd.DataFrame(cart_items_series)
    df['count'] = df.groupby('_id')['_id'].transform('size')
    df.drop_duplicates(subset='_id', keep='first', inplace=True)
    result = df.to_dict('records')
    return result

@app.route("/add_to_cart/", methods=["POST"])
def add_to_cart():
    print(request.json)
    user_id = request.json.get("user_id")
    product_id = request.json.get("product_id")
    if not user_id:
        return jsonify({'success': False, 'msg': 'Please login'})

    if not product_id:
        return jsonify({'success': False, 'msg': 'Please provide product_id'})

    users = mongo.db.users
    user = users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({"success": False, 'msg': "User not found"})

    carts = mongo.db.carts
    existing_user_cart = carts.find_one({"user": user_id})
    if existing_user_cart:
        carts.update_one(
            {"user": user_id},
            {"$push": {"cart_items": product_id}}
        )
    else:
        carts.insert_one({
            "user": user_id,
            "cart_items": [product_id],
        })

    return jsonify({'success': True, 'msg': "Product added to cart!"})


@app.route("/change_cart/", methods=["POST"])
def change_cart():
    user_id = request.json.get("user_id")
    product_id = request.json.get("product_id")
    change_type = request.json.get("change_type")

    if not user_id:
        return jsonify({'success': False, 'msg': 'Please login'})

    if not product_id:
        return jsonify({'success': False, 'msg': 'Please provide product_id'})

    users = mongo.db.users
    user = users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({"success": False, 'msg': "User not found"})

    carts = mongo.db.carts
    existing_user_cart = carts.find_one({"user": user_id})
    if not existing_user_cart:
        return jsonify({"success": False, 'msg': "Cart not found"})

    if change_type == 'increase':
        carts.update_one(
            {"user": user_id},
            {"$push": {"cart_items": product_id}}
        )
    elif change_type == 'decrease':
        carts.update_one(
            {"user": user_id},
            {"$pull": {"cart_items": {"$elemMatch": {"$eq": product_id}}}}
        )
    elif change_type == 'remove':
        carts.update_one(
            {"user": user_id},
            {"$pull": {"cart_items":  product_id}}
        )
    else:
        return jsonify({'success': False, 'msg': "Wrong change type!"})
    return jsonify({'success': True, 'msg': "Product added to cart!"})

@app.route("/get_razorpay_offer/", methods=['POST'])
def get_razorpay_offer():
    amount=request.json.get("amount")
    data = { "amount": amount, "currency": "INR", "receipt": "order_rcptid_" + str(os.urandom(4)) }
    payment = client.order.create(data=data)
    order_id = payment.get("id")
    return jsonify({"success": True, "msg": "Got order id", 'order_id': order_id, 'amount': amount, 'RAZORPAY_KEY': RZP_KEY})
    
    
def get_cart_items(query):
    return serializer(mongo.db.products.find_one(query))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
