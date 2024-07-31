from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from .filters import ProductModelFilterSet
from .models import Product, Category
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from .serializers import ProductModelSerializer, CategoryModelSerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    # filterset_fields = 'name', 'price', 'owner', 'description'
    filterset_class = ProductModelFilterSet

    def filter_queryset(self, queryset):
        description = self.request.query_params.get('description')
        name = self.request.query_params.get('name')
        price = self.request.query_params.get('price')
        owner = self.request.query_params.get('owner')

        if name:
            queryset = queryset.filter(name=name)
        if description:
            queryset = queryset.filter(description__contains=description)
        if price:
            queryset = queryset.filter(price=price)
        if owner:
            user = get_user_model()
            queryset = user.objects.filter(username=owner)

        return queryset
