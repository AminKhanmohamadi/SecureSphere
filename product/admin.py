from django.contrib import admin
from .models import Category, Product, ProductAttribute


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['title' , 'is_public']


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ProductAttributeInline]
