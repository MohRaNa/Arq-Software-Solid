from peewee import SqliteDatabase, Model, CharField, FloatField, IntegerField, DateField

db = SqliteDatabase('grocery.db')  # Crea o conecta a la base de datos SQLite

class GroceryItem(Model):
    sku = CharField(primary_key=True)
    name = CharField()
    description = CharField()
    price = FloatField()
    quantity = IntegerField()
    expiration_date = DateField()

    class Meta:
        database = db

db.connect()
db.create_tables([GroceryItem])
