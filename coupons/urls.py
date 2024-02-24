from django.urls import path
from . import views
urlpatterns=[

path('create_coupon/',views.create_coupon,name="create_coupon"),
path('view_coupon/',views.view_coupon,name="view_coupon"),
path('update_coupon/<int:id>/',views.update_coupon,name='update_coupon'),
path('delete_coupon/<int:id>/',views.delete_coupon,name='delete_coupon'),
path('user_coupons/',views.user_coupons,name='user_coupons'),
path('apply_coupon/',views.apply_coupon,name="apply_coupon"),

]