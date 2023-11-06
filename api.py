from flask import Flask, request, jsonify
from models import GroceryItem
import requests

app = Flask(__name__)

API_BASE_URL = "https://api.exchangeratesapi.io/v1/"
API_KEY = "300c6eb13a807d4bb3d5230fc36421e7"

# Función para obtener tasas de cambio
def get_exchange_rates():
    url = f"{API_BASE_URL}latest?access_key={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data.get('rates', {})
    else:
        return {}

# Función para convertir moneda
def convert_currency(amount, from_currency, to_currency):
    rates = get_exchange_rates()
    if from_currency in rates and to_currency in rates:
        conversion_rate = rates[to_currency] / rates[from_currency]
        converted_amount = amount * conversion_rate
        return converted_amount
    else:
        return None

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
@app.route('/item/currency', methods=['GET'])
def get_items_by_currency():
    currency = request.args.get('currency', 'USD')
    items = list(GroceryItem.select().where(GroceryItem.currency == currency))
    
    # Realiza conversiones de moneda para los precios
    converted_items = []
    for item in items:
        converted_price = convert_currency(item.price, "USD", currency)
        if converted_price is not None:
            item.price = converted_price
            converted_items.append(item.serialize())

    return jsonify(converted_items)

if __name__ == '__main__':
    app.run(debug=True)
