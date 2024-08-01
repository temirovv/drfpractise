from django.contrib.auth import get_user_model
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from .filters import ProductModelFilterSet
from .models import Product, Category
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from .serializers import ProductModelSerializer, CategoryModelSerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    # filterset_fields = 'category', 'name'
    filterset_class = ProductModelFilterSet
