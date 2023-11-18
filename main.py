import csv
from app.models.models import db, GroceryItem
from app.app import app

def load_data_from_csv(filename):
    with open(filename, 'r') as f:
        csv_data = f.read().replace("Expiration Date", "Expiration_Date")
        reader = csv.DictReader(csv_data.splitlines())
        items = list(reader)
    with db.atomic():
        for item in items:
            sku = item['SKU'].upper() 
            existing_item, created = GroceryItem.get_or_create(SKU=sku, defaults=item)
            if not created:
                # Actualiza los campos del elemento existente si es necesario
                for key, value in item.items():
                    setattr(existing_item, key, value)
                existing_item.save()

if __name__ == '__main__':
    if not db.is_closed():
        db.close()
    db.connect()
    db.create_tables([GroceryItem], safe=True) 
    load_data_from_csv('sample_grocery.csv')

    # Ejecuta la aplicación Flask
    app.run(debug=True)