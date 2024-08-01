from django.contrib.admin import ModelAdmin, register
from django.contrib.auth import get_user_model


User = get_user_model()


@register(User)
class UserModelAdmin(ModelAdmin):
    pass
