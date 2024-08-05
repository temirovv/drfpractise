from .filters import ProductModelFilterSet, CategoryModelFilterSet
from .models import Product, Category
from rest_framework.generics import ListAPIView
from .serializers import ProductModelSerializer, CategoryModelSerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filterset_class = ProductModelFilterSet


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    filterset_class = CategoryModelFilterSet
