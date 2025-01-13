from django.urls import path
from .views import ProductListView
urlpatterns = [
    path('list/<int:pk>', ProductListView.as_view(), name='product_list' ),
]