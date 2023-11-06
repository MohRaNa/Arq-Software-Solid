import csv
from models import GroceryItem

def load_data_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        items = list(reader)
    for item in items:
        GroceryItem.create(**item)

if __name__ == '__main__':
    from api import app  # Importa la aplicación Flask
    from models import db, GroceryItem

    # Carga los datos del archivo CSV en la base de datos
    db.connect()
    db.create_tables([GroceryItem])
    load_data_from_csv('sample_grocery.csv')

    # Ejecuta la aplicación Flask
    app.run(debug=True)
