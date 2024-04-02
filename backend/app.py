from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = Flask(__name__)
CORS(app)

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

app.config['JWT_SECRET_KEY'] = os.urandom(24)
jwt = JWTManager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db'"
db.init_app(app)

class User(db.Model):
    # id: Mapped[int] = mapped_column(primary_key=True)
    # username: Mapped[str] = mapped_column(unique=True)
    # email: Mapped[str] = mapped_column(unique=True)
    # phone: Mapped[int] = mapped_column(unique=True)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(80))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))

    def __repr__(self):
        return '<User %r>' % self.username


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    price = db.Column(db.Integer())

    def __repr__(self):
        return '<Product %r>' % self.name


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

    username = user.get('username')
    user_exists = db.get_or_404(User, username)
    # user.get('email')
    if user_exists:
        return jsonify({"success": False, 'msg': "User already exists with same username/email"})

    user = User(**user)
    db.session.add(user)
    db.session.commit()

    return jsonify({'success': True, 'msg': "user created"})


@app.route("/product/add/", methods=["POST"])
def add_product():
    product = request.json.get('product')
    if not product:
        return jsonify({"success": False, 'msg': "Please enter all details"})

    Product(**product)
    return jsonify({'success': True, 'msg': "product created"})

@app.route("/products/", methods=["GET"])
def get_all_products():
    Product.query.filter_by()

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

    product = Product.query.filter_by(id=id).first()
    if not product:
        return jsonify({"success": False, 'msg': "Product not found"})

    return jsonify({'success': True, 'msg': "product!", 'product': product})


if __name__ == '__main__':
    app.run(debug=True, port=8000)
