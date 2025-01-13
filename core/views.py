from pydoc import parentname
from unicodedata import category

from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View

from products.models import Category


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'core/main.html'



class CategoryPartials(View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(parent__isnull=True)
        return render(request , 'core/partials/category_partial.html' , {'categories': categories})