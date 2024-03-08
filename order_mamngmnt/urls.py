from django.urls import path
from . import views
urlpatterns=[
    path('checkout/<int:cart_id>/',views.cart_to_order,name='checkout'),
    # path('order_display/',views.order_display,name='order_display'),
    # path('order_item_display/',views.order_item_display,name='order_item_display'),
    path('order_history/',views.order_history,name='order_history'),
     path('failed_order_history',views.failed_order_history,name='failed_order_history'),
    path('admin_orderlist/',views.admin_orderlist,name='admin_orderlist'),
    path('orderlist/<int:order_id>/',views.update_status,name='update_status'),
    path('get_order_products/<int:order_id>/',views.get_order_products,name='get_order_products'),
    path('retry_payment_checkout/<int:id>/',views.retry_payment_checkout,name="retry_payment_checkout"),
    path('my_orders/<int:order_id>/',views.my_orders,name="my_orders"),
    path('cancel_order/<int:order_id>/',views.cancel_order,name="cancel_order"),
     path('return_order/<int:order_id>/',views.return_order,name="return_order"),

]