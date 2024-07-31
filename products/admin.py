from django.contrib.admin import register, StackedInline, ModelAdmin
from .models import Product, ProductImage, Category


@register(Category)
class CategoryModelAdmin(ModelAdmin):
    list_display = 'name',
    search_fields = 'name',


class ImageStackedInline(StackedInline):
    model = ProductImage
    fields = 'image', 'product'


@register(Product)
class ProductModelAdmin(ModelAdmin):
    list_display = 'name', 'description', 'price', 'owner'
    inlines = [ImageStackedInline]
    search_fields = 'name', 'price', 'category__name'
    autocomplete_fields = 'category',
