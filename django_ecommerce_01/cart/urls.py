from django.urls import path
from django_ecommerce_01.cart import views

app_name = "cart"
urlpatterns = [
    path('product-list/', views.ProductListAPIView.as_view(), name='product-list'),
    path('product-details/<slug>/', views.ProductDetailAPIView.as_view(), name='product-details'),
    path('add-to-cart/<slug>/', views.AddToCartAPIView.as_view(), name='add-to-cart'),
]