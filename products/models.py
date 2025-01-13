import uuid
from decimal import Decimal
from slugify import slugify

from autoslug import AutoSlugField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.

class Category(MPTTModel):
    title = models.CharField(max_length=100, db_index=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, db_index=True,
                            related_name='children')
    description = models.TextField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title , allow_unicode=True)
        super(Category , self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique=True, allow_unicode=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    recommendation = models.ManyToManyField('products.Product', through='ProductRecommendation', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    off_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    offer = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], null=True,
                                        blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.offer and self.offer >= 1:
            discount = (self.offer / Decimal('100')) * self.price
            self.off_price = self.price - discount
        super().save(*args, **kwargs)

    @property
    def get_price(self):
        return self.off_price if self.offer else self.price

    @property
    def main_image(self):
        if self.images.exists():
            return self.images.first()
        else:
            return None


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=True, blank=True)


class ProductRecommendation(models.Model):
    primary = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='primary_recommendations')
    recommendation = models.ForeignKey(Product, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('primary', 'recommendation')
        ordering = ('primary', '-rank')


def product_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return f'images/product/{slugify(instance.product.title)}/{filename}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_upload_path)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('display_order',)
        verbose_name = 'Product Image'
        verbose_name_plural = 'Product Images'

    def delete(self , *args, **kwargs):
        super().delete(*args, **kwargs)
        for index , image in enumerate(self.product.images.all()):
            image.display_order = index
            image.save()