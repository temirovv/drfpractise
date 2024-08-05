from django.contrib.auth import get_user_model
from django_filters import FilterSet, BooleanFilter, DateFilter, NumberFilter, ChoiceFilter, CharFilter
from .models import Product, Category
from django.utils.timezone import datetime, timedelta, now
from users.models import CustomUser
from django.db.models import F, TextChoices


class SortingChoices(TextChoices):
    EXPENSIVE = 'expensive', 'Expensive'
    CHEAP = 'cheap', 'Cheap'
    OLD = 'old', 'Old'
    NEW = 'new', 'New'


class CategoryModelFilterSet(FilterSet):
    class Meta:
        model = Category
        fields = 'name',


class ProductModelFilterSet(FilterSet):
    is_active = BooleanFilter(field_name='owner__is_active', lookup_expr='exact')
    in_day = NumberFilter(field_name='created_at', lookup_expr='iexact', method='is_in_day')
    made_date = ChoiceFilter(field_name='created_at',
                             choices=(
                                 (3, 3), (7,  7), (15, 15), (30, 30)
                             ),
                             method='days_since_made')
    owner_type = ChoiceFilter(field_name='owner__type', choices=CustomUser.Type.choices)
    n = NumberFilter(field_name='price' ,method='gt_n_multiple_price')

    category = CharFilter(method='get_category')
    only_with_picture = BooleanFilter(method='has_pic')
    sorting = ChoiceFilter(choices=SortingChoices.choices, method='sorting_')

    class Meta:
        model = Product
        fields = 'name', 'description', 'price', 'owner', 'category'

    def sorting_(self, queryset, name, value):
        sorts = {'cheap': 'price', 'expensive': '-price', 'new': '-created_at', 'old': 'created_at'}
        field = sorts.get(value, 'created_at')
        return queryset.order_by(field)

    def has_pic(self, queryset, name, value):
        qs = queryset.objects.filter(images__isnull=not value)
        return qs

    def get_category(self, queryset, name, value):
        category = Category.objects.get(name__iexact=value)
        categories = category.get_descendants(include_self=True)
        return queryset.filter(category__in=categories)

    def is_in_day(self, queryset, name, value):
        return queryset.filter(created_at__day=str(value))

    def days_since_made(self, queryset, name, value):
        target_date = now().date() - timedelta(days=int(value))
        # return queryset.filter(created_at__date=target_date)
        # return queryset.filter(created_at__contains=target_date)
        return queryset.filter(created_at__startswith=target_date)

    def gt_n_multiple_price(self, queryset, name, value):
        return queryset.filter(owner__balance__gt=F('price')*value)
