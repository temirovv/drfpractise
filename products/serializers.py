from pprint import pprint

from .models import Product, Category, ProductImage
from rest_framework.serializers import ModelSerializer, ListSerializer, SerializerMethodField
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = 'image', 'product'


class CategoryModelSerializer(ModelSerializer):
    child = SerializerMethodField()

    # name = SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'parent', 'child')

    def get_child(self, category):
        child = category.get_children()
        return CategoryModelSerializer(child, many=True).data


class ProductModelSerializer(ModelSerializer):
    category = SerializerMethodField()
    owner = SerializerMethodField()
    image = ListSerializer(child=ProductImageSerializer(), source='images')

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'owner', 'image', 'category', 'created_at')

    def get_category(self, product):  # noqa
        return product.category.name

    def get_owner(self, product):  # noqa
        return product.owner.username


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
