from django.contrib.auth import get_user_model
from django.db.models import Model, CharField, TextField, FloatField, ForeignKey, CASCADE, ImageField,\
    DateTimeField, SlugField
from django.utils.text import slugify
from django.utils.timezone import now

User = get_user_model()


class BaseCreatedModel(Model):
    updated_at = DateTimeField(auto_now_add=True, db_default=now())
    created_at = DateTimeField(auto_now=True, db_default=now())

    class Meta:
        abstract = True


class BaseSlugModel(Model):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True, editable=False)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        count = 0
        self.slug = slugify(self.name)

        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug += f"_{count}"
            count += 1
        
        super().save(force_insert, force_update, using, update_fields)

class Category(BaseSlugModel):

    def __str__(self):
        return self.name


class Product(BaseSlugModel, BaseCreatedModel):
    description = TextField()
    price = FloatField()
    owner = ForeignKey(User, CASCADE, related_name='products')
    category = ForeignKey('products.Category', CASCADE, related_name='products')


class ProductImage(Model):
    image = ImageField()
    product = ForeignKey('products.Product', CASCADE, related_name='images')

    def __str__(self):
        return f"image of {self.product.name}"
