from flask import Flask, render_template, request, jsonify, redirect, url_for
from app.models.models import GroceryItem
import requests

app = Flask(__name__)

API_BASE_URL = "https://api.freecurrencyapi.com/v1"
API_KEY = "fca_live_WOZ0cR5GFEW96tQkLhG7l3acbynPfWRlWVar8DlZ&currencies=MXN%2CUSD"

def get_exchange_rate():
    url = f"{API_BASE_URL}/latest?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    exchange_rates = data.get("data", {})
    return exchange_rates

@app.route('/', methods=['GET'])
def view_items():
    items = list(GroceryItem.select())
    return render_template('items.html', items=items)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        data = request.form.to_dict()
        item = GroceryItem.create(**data)
        return redirect(url_for('view_items'))
    return render_template('add_item.html')

@app.route('/items/delete/<string:sku>', methods=['GET', 'POST'])
def delete_item(sku):
    if request.method == 'POST':
        try:
            item = GroceryItem.get(GroceryItem.SKU == sku)
            item.delete_instance()
            return redirect(url_for('view_items'))
        except GroceryItem.DoesNotExist:
            return 'Elemento no encontrado', 404
    return render_template('delete_item.html', sku=sku)

@app.route('/items_currency', methods=['GET'])
def items_currency():
    exchange_rates = get_exchange_rate()
    mxn_to_usd_rate = exchange_rates.get("MXN", 1)
    items = list(GroceryItem.select())
    
    for item in items:
        item.Price *= mxn_to_usd_rate
    
    return render_template('items_currency.html', items=items)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    app.add_url_rule('/', 'root', lambda: redirect(url_for('view_items')))