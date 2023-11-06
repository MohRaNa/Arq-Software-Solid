from flask import Flask, request, jsonify
from models import GroceryItem
import requests

app = Flask(__name__)

# Ruta para obtener todos los elementos
@app.route('/item', methods=['GET'])
def get_items():
    items = list(GroceryItem.select())
    return jsonify([item.serialize() for item in items])

# Ruta para agregar un elemento
@app.route('/item', methods=['POST'])
def add_item():
    data = request.get_json()
    item = GroceryItem.create(**data)
    return jsonify(item.serialize()), 201

# Ruta para borrar un elemento por SKU
@app.route('/item/<string:sku>', methods=['DELETE'])
def delete_item(sku):
    try:
        item = GroceryItem.get(GroceryItem.sku == sku)
        item.delete_instance()
        return '', 204
    except GroceryItem.DoesNotExist:
        return 'Elemento no encontrado', 404

# Ruta para obtener elementos por moneda
@app.route('/item', methods=['GET'])
def get_items_by_currency():
    currency = request.args.get('currency', 'USD')
    items = list(GroceryItem.select().where(GroceryItem.currency == currency))
    return jsonify([item.serialize() for item in items])

if __name__ == '__main__':
    app.run(debug=True)
