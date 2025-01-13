from django.contrib import admin
from .models import Category, Product, ProductAttribute, ProductRecommendation, ProductImage
from mptt.admin import MPTTModelAdmin

# Register your models here.
@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('title', 'parent', 'tree_id', 'lft', 'rght', 'level' , 'slug')
    list_filter = ('parent',)
    search_fields = ('title',)


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
