from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/ShopVista"

mongo = PyMongo(app).db


@app.route("/", methods=["GET"])
def index():
    return jsonify({'success': True})


@app.route("/sign_in/", methods=["POST"])
def sign_in():
    user = request.json.get("user")
    if not user:
        return jsonify({'success': False, 'msg': "Please provide both username and password"})
    
    user = mongo.db.users.find_one({"username": user.get('username'), "password": user.get('password')})
    if not user:
        return jsonify({'success': True, 'msg': "User not found!"})
    
    return jsonify({'success': True, 'msg': "sign in successful"})


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

if __name__ == '__main__':
    app.run(debug=True, port=8000)
    