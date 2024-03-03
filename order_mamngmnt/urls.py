from django.urls import path
from . import views
urlpatterns=[
    path('checkout/<int:cart_id>/',views.cart_to_order,name='checkout'),
    path('order_display/',views.order_display,name='order_display'),
    path('order_item_display/',views.order_item_display,name='order_item_display'),
    path('order_history/',views.order_history,name='order_history'),
    path('admin_orderlist/',views.admin_orderlist,name='admin_orderlist'),
    path('orderlist/<int:order_id>/',views.update_status,name='update_status'),
    path('get_order_products/<int:order_id>/',views.get_order_products,name='get_order_products'),
    
    path('my_orders/',views.my_orders,name="my_orders"),

]