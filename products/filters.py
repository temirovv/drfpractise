from django_filters import FilterSet, BooleanFilter
from .models import Product


class ProductModelFilterSet(FilterSet):
    is_active = BooleanFilter(field_name='owner__is_active',lookup_expr='exact')

    class Meta:
        model = Product
        fields = 'name', 'description', 'price', 'owner',

    # def is_active_owner(self, queryset, name, value):
    #     active_owner = queryset.objects.filter(owner__is_active=value)
    #     return active_owner
