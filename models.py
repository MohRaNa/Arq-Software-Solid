from peewee import SqliteDatabase, Model, CharField, FloatField, IntegerField, DateField

db = SqliteDatabase('grocery.db')  # Crea o conecta a la base de datos SQLite

class GroceryItem(Model):
    SKU = CharField(primary_key=True)
    Name = CharField()
    Description = CharField()
    Price = FloatField()
    Quantity = IntegerField()
    #Arreglar Expiration_Date
    Expiration_date = DateField(null=True, default='9999-12-31')

    class Meta:
        database = db

db.connect()
db.create_tables([GroceryItem])
