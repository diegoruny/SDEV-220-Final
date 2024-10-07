from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),
    path('remove_item/<int:product_id>/', views.remove_item, name='remove_item'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
]
