from django.urls import path
from django_ecommerce_01.cart import views

app_name = "cart"
urlpatterns = [
    path('product-list/', views.ProductListAPIView.as_view(), name='product-list'),
    path('product-details/<slug>/', views.ProductDetailAPIView.as_view(), name='product-details'),
    path('add-to-cart/<slug>/', views.AddToCartAPIView.as_view(), name='add-to-cart'),
    path('cart-view/', views.CartAPIView.as_view(), name='cart-view'),
    path('order-item/<int:id>/delete/', views.OrderItemDeleteAPIView.as_view(), name='delete-order-item'),
    path('update-order-item/<int:id>/', views.UpdateOrderItemAPIView.as_view(), name='update_order_item'),
    path('address/', views.AddressUpdateRetrieveAPIView.as_view(), name='get-set-address'),
]