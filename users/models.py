from django.db.models import TextChoices, CharField, FloatField
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Type(TextChoices):
        USER = 'user', 'User'
        MANAGER = 'manager', 'Manager'
        OPERATOR = 'operator', 'Operator'
        MODERATOR = 'moderator', 'Moderator'

    type = CharField(max_length=25, choices=Type.choices, default=Type.USER)
    balance = FloatField(null=True, blank=True)
