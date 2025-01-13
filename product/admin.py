from django.contrib import admin
from .models import Category, Product, ProductAttribute, ProductRecommendation, ProductImage


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['title' , 'is_public']


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

class ProductRecommendationInline(admin.TabularInline):
    model = ProductRecommendation
    extra = 1
    fk_name = 'primary'

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['title' , 'category' , 'is_public']
    inlines = [ProductAttributeInline ,ProductImageInline ,ProductRecommendationInline]
