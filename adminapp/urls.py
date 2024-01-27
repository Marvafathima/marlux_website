from django.urls import path
from . import views
app_name = 'adminapp'
urlpatterns=[
    # path('home/',views.index,name='home'),
    # path('login/',views.user_login,name='login'),
    # path('otp/<str:uid>/', views.otpVerify, name='otp'),
    # path('',views.user_signup,name='signup'),
    path('adminlogout/',views.admin_logout,name='alogout'),
    path('custadmin/',views.custom_admin,name='admin'),
    path('dashboard/',views.admin_dashboard,name='dashboard'),
    path('dashboard/userlist/',views.admin_userlist,name='userlist'),
    path('dashboard/userlist/unblock/<int:user_id>/',views.user_unblock,name='unblock_user'),
    path('dashboard/userlist/block/<int:user_id>/',views.user_block,name='block_user'),
]