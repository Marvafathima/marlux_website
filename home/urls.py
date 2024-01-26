from django.urls import path
from . import views
urlpatterns=[
    path('home/',views.index,name='home'),
    path('login/',views.user_login,name='login'),
    path('otp/', views.otpVerify, name='otp'),
    path('',views.user_signup,name='signup'),
    path('logout/',views.user_logout,name='logout'),
    # path('custadmin/',views.custom_admin,name='admin'),
    # path('dashboard/',views.admin_dashboard,name='dashboard'),
    # path('dashboard/userlist/',views.admin_userlist,name='userlist'),
]