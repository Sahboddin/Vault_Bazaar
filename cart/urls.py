from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.cart, name='cart'),
    path('<int:product_id>/', views.add_to_cart, name='add_cart'),
    path('remove/<int:product_id>/<int:cart_item_id>/', views.decrease_cart_item, name='decrease_cart_item'),
    path('delete/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
]