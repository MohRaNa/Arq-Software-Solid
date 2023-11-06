from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    SKU = db.Column(db.String(20), unique=True, nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(200), nullable=True)
    Price = db.Column(db.Float, nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    Expiration_Date = db.Column(db.String(10), nullable=False)

    def serialize(self):
        return {
            'SKU': self.SKU,
            'Name': self.Name,
            'Description': self.Description,
            'Price': self.Price,
            'Quantity': self.Quantity,
            'Expiration Date': self.Expiration_Date
        }

@app.route('/item', methods=['GET'])
def get_items():
    currency = request.args.get('currency')
    if currency == 'USD':
        response = requests.get('https://api.exchangerates.io/latest')
        exchange_rate = response.json()['rates']['USD']
        items = Item.query.all()
        converted_items = []
        for item in items:
            converted_item = {
                'SKU': item.SKU,
                'Name': item.Name,
                'Description': item.Description,
                'Price': item.Price * exchange_rate,
                'Quantity': item.Quantity,
                'Expiration Date': item.Expiration_Date
            }
            converted_items.append(converted_item)
        return {'items': converted_items}
    else:
        items = Item.query.all()
        return {'items': [item.serialize() for item in items]}

@app.route('/item', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = Item(
        SKU=data['SKU'],
        Name=data['Name'],
        Description=data['Description'],
        Price=data['Price'],
        Quantity=data['Quantity'],
        Expiration_Date=data['Expiration Date']
    )
    db.session.add(new_item)
    db.session.commit()
    return {'message': 'Item added successfully'}

@app.route('/item/<string:SKU>', methods=['DELETE'])
def delete_item(SKU):
    item = Item.query.filter_by(SKU=SKU).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item deleted successfully'}
    return {'message': 'Item not found'}, 404

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('templates/index.html', items=items)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item_page():
    if request.method == 'POST':
        data = request.form
        new_item = Item(
            SKU=data['SKU'],
            Name=data['Name'],
            Description=data['Description'],
            Price=float(data['Price']),
            Quantity=int(data['Quantity']),
            Expiration_Date=data['Expiration Date']
        )
        db.session.add(new_item)
        db.session.commit()
        return 'Item added successfully'
    return render_template('templates/add.html')

@app.route('/edit_item/<string:SKU>', methods=['GET', 'POST'])
def edit_item_page(SKU):
    item = Item.query.filter_by(SKU=SKU).first()
    if request.method == 'POST':
        data = request.form
        item.Name = data['Name']
        item.Description = data['Description']
        item.Price = float(data['Price'])
        item.Quantity = int(data['Quantity'])
        item.Expiration_Date = data['Expiration Date']
        db.session.commit()
        return 'Item updated successfully'
    return render_template('templastes/base.html', item=item)

if __name__ == '__main__':
    db.create_all()
    app.run()

