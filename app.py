from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin

# jsonify é utilizado para retorna json nos métodos
# request é utilizado para captar o json do produto

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecomerce.db'

db = SQLAlchemy(app)
CORS(app)

# Modelagem do usuário
# User (id, username, password)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=True)

@app.route('/login', methods=["POST"])
def login():
    data = request.json
    data.get("username")

    user = User.query.filter_by(username=data.get("username")).first()

    if user:
        if data.get("password") == user.password: 
            return jsonify({"message":"Logged in successfully"})
    return jsonify({"message":"Unauthorized. Invalid credentials"}), 401

# Modelagem do banco de dados
# Produto (id, nome, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# Adição de produtos no e-commerce
# Método HTTP Post
@app.route('/api/products/add', methods=["POST"])
def add_product():
    # obtem JSON com informações do produto.
    data = request.json 
    # Verifica se nome e preço foram colocados no JSON 
    if 'name' in data and 'price' in data:

        # data[] acessa os valores do JSON captado pelo request
        product = Product(name=data["name"], price=data["price"], description=data.get("description", ""))

        # Adiciona o cadastro do produto no banco de dados
        db.session.add(product)
        db.session.commit()
        return jsonify({"message":"Product added sucessfully"})
    return jsonify({"message":"Invalid product data"}), 400

# Deleção de produtos no e-commerce
# Método HTTP Delete
@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    # Recuperar o produto da base de dados
    # Verifica de o produto existe. Se existe, apagar da base de dados. Se não, retorna erro 404 NOT_FOUND
    product = Product.query.get(product_id)
    if product: 
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"Product deleted sucessfully"})
    return jsonify({"message":"Product does not exist"}), 404

# Recuperação de produtos presentes no e-commerce
# Método HTTP GET
@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_datails(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message":"Product not found"}), 404

# Atualizar as informações de um produto
# Método HTTP Put
@app.route('/api/products/uptade/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"message":"Product not found"}), 404
   
    data = request.json
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'description' in data:
        product.description = data['description']

    # Sempre que houver uma alteração é necessário dar commit no BD.    
    db.session.commit()

    return jsonify({"message": "Product updated sucessfully"})

# Lista todos os produtos adicionados
# Método HTTP GET
@app.route('/api/products', methods=["GET"])
def get_products():
    products = Product.query.all()
    product_list = []
    for product in products:
        product_data = {
             "id": product.id,
             "name": product.name,
             "price": product.price,
             "description": product.description
        }
        product_list.append(product_data)
    return jsonify(product_list)


# Definir uma rota raiz (página inicial) e a função que será executada ao requesitar essa rota
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)