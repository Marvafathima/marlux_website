from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='home'),
    path('login/',views.user_login,name='login'),
    path('otp/', views.otpVerify, name='otp'),
    path('signup/',views.user_signup,name='signup'),
    path('logout/',views.user_logout,name='logout'),
    path('shop/',views.shop,name='shop'),
    path('shop/<int:category_id>/',views.categoryproduct,name='catpro'),
    path('product_detail/<int:id>/',views.product_detail,name='product_detail'),
    path('get_sizes/', views.get_sizes, name='get_sizes'),
    path('get_price/', views.get_price, name='get_price'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('update_cart_item/', views.update_cart_item, name='update_cart_item'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('myprofile/',views.user_profile,name='user_profile'),
    path('user_address/',views.user_address,name='user_address'),
    path('cartcount/',views.cart_count,name='cart_count'),
    path('addressdisplay/',views.addressdisplay,name='addressdisplay'),
    path('set_default_address/',views.set_default_address,name='set_default_address'),
    path('delete_address/<int:id>/',views.address_delete,name='delete_address'),
    path('update_address/<int:id>/',views.update_address,name='update_address'),
    path('user_password/',views.user_password,name='user_password'),
    path('product_detail/<int:id>/cart_login_redirect/',views.cart_login_redirect,name='cart_login_redirect')
   
    # path('forgot_password/',views.forgot_password,name='forgot_password'),
    # path('forgot_password/', views.forgot_password, name='forgot_password'),
    # path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),


]