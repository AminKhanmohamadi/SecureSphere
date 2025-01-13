from django.shortcuts import render
from django.views import View

from products.models import Product


# Create your views here.
class ProductListView(View):
    def get(self , request , pk):
        products = Product.objects.filter(category=pk)
        for product in products:
            product.first_image = product.images.first()

        context = {
            'products': products,
        }
        return render(request , 'products/product_list.html' , context)