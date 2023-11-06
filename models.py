from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
