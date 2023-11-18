from peewee import SqliteDatabase, Model, CharField, FloatField, IntegerField, DateField

db = SqliteDatabase('grocery.db') 

class GroceryItem(Model):
    SKU = CharField(primary_key=True)
    Name = CharField()
    Description = CharField()
    Price = FloatField()
    Quantity = IntegerField()
    Expiration_Date = DateField(null=True)

    class Meta:
        database = db

db.connect()
db.create_tables([GroceryItem])
