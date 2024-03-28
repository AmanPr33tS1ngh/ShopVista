from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.urandom(24)
jwt = JWTManager(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shop_vista.db"

db = SQLAlchemy()
db.init_app(app)
    
# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))

    def __repr__(self) -> str:
        return self.usename

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'firstName': self.firstName,
            'lastName': self.lastName,
        }
        
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    price = db.Column(db.Integer)
    image = db.Column(db.String(255))
    discountAmount = db.Column(db.Integer)
    
    def __repr__(self) -> str:
        return f'{self.name} - {self.price}'

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'image': self.image,
            'discountImage': self.discountAmount,
        }


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('product.id'), nullable=False)

    user = db.relationship('User', backref='ratings')
    product = db.relationship('Product', backref='ratings')

    def __repr__(self) -> str:
        return f'{self.name} - {self.price}'

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'value': self.value,
            'user': self.user.serialize(),
            'product': self.product.serialize(),
        }
        


with app.app_context():
    print('with app.app_context():')
    db.create_all()
    
    
# serializer
def serialize(objects) -> list:
    return [obj.serialize() for obj in objects]


# routes
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
    
    user = User.query.filter_by(username=username, password=password).first()
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
    
    user_exists = User.query.filter_by(username=user.get('username')).first()
    if user_exists:
        return jsonify({"success": False, 'msg': "User already exists with same username/email"})
    
    user = User(**user)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'success': True, 'msg': "user created"})


@app.route("/products/", methods=["GET", "POST"])
def get_all_products():
    try:
        print(request.method)
        if request.method == "POST": 
            product = request.json.get('product')
            p = request.json
            if not product:
                return jsonify({"success": False, 'msg': "Please enter all details"})
            print('product', product)
            new_product = Product(**product)
            db.session.add(new_product)
            db.session.commit()
            return jsonify({'success': True, 'msg': "product created"})
        products = serialize(Product.query.filter().all())
        print('prododo', products)
        return jsonify({'success': True, 'msg': "products!", 'products': products})
    except Exception as e:
        print('err', str(e))
        return jsonify({'success': False, 'msg': "no products!", 
                        # 'products': products
                        })

@app.route("/product/<id>", methods=["GET"])
def get_product(id):
    print('id', id)
    if not id:
        return jsonify({'success': False, 'msg': 'Please provide id'})
    
    product = Product.query.filter_by(id=id).first()
    if not product:
        return jsonify({"success": False, 'msg': "Product not found"})
    
    return jsonify({'success': True, 'msg': "product!", 'product': product})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
    