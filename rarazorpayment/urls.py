from django.urls import path
from . import views
urlpatterns = [
#   path('checkout_page',views.checkout_page,name="checkout_page"),
path('proceed_to_pay/',views.razorpaycheck,name='proceed_to_pay'),
path('place_order',views.place_order,name="place_order"),
]