from django.urls import path
from . import views
urlpatterns=[
    path('checkout/<int:cart_id>/',views.cart_to_order,name='checkout'),





]