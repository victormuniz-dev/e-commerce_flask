from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecomerce.db'

db = SQLAlchemy(app)

# Modelagem do banco de dados
# Produto (id, nome, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# Adição de produtos no e-comerce
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

@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    # Recuperar o produto da base de dados
    # Verifica de o produto existe. Se existe, apagagar da base de dados. Se não, retorna erro 404 NOT_FOUND
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"Product deleted sucessfully"})
    return jsonify({"message":"Product does not exist"}), 404


# Definir uma rota raiz (página inicial) e a função que será executada ao requesitar essa rota
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)