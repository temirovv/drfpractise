from django.contrib.auth import get_user_model
from django.db.models import Model, CharField, TextField, FloatField, ForeignKey, CASCADE, ImageField


User = get_user_model()


class Category(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=255)
    description = TextField()
    price = FloatField()
    owner = ForeignKey(User, CASCADE, related_name='products')
    category = ForeignKey('products.Category', CASCADE, related_name='products')


class ProductImage(Model):
    image = ImageField()
    product = ForeignKey('products.Product', CASCADE, related_name='images')

    def __str__(self):
        return f"image of {self.product.name}"
