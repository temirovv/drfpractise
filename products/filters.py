from django.contrib.auth import get_user_model
from django_filters import FilterSet, BooleanFilter, DateFilter, NumberFilter, ChoiceFilter
from .models import Product
from django.utils.timezone import datetime, timedelta
from users.models import CustomUser
from django.db.models import F


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

    class Meta:
        model = Product
        fields = 'name', 'description', 'price', 'owner',

    # def is_active_owner(self, queryset, name, value):
    #     active_owner = queryset.objects.filter(owner__is_active=value)
    #     return active_owner

    def is_in_day(self, queryset, name, value):
        return queryset.filter(created_at__day=str(value))

    def days_since_made(self, queryset, name, value):
        today = datetime.now().date()
        target_date = today - timedelta(days=int(value))
        # return queryset.filter(created_at__date=target_date)
        # return queryset.filter(created_at__contains=target_date)
        return queryset.filter(created_at__startswith=target_date)

    def gt_n_multiple_price(self, queryset, name, value):
        return queryset.filter(owner__balance__gt=F('price')*value)
