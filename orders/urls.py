from django.urls import path

from . import views

urlpatterns = [
    path('order_complete/', views.order_complete, name='order_complete'),
    path('place_order/', views.place_order, name='place_order'),
    path('success/<tran_id>/<int:user_id>', views.success_view, name='success_view'),
    



    # path('checkout/', views.checkout, name='checkout'),
    # path('pay/', views.payment, name='payment'),
    path('all_order/', views.all_order, name='all_order'),
    # path('purchase/<tran_id>/<int:user_id>', views.purchase, name='purchase'),
    
]