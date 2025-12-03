from django.urls import path
from .views import ProductListView, ShopListView, OrderListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('shops/', ShopListView.as_view(), name='shop-list'),
    path('orders/', OrderListView.as_view(), name='order-list'),
]
