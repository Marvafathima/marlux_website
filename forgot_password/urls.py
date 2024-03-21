from django.urls import path
from . import views
urlpatterns=[
 path('forgot_password',views.forgot_password,name='forgot_password'),  
 path('reset_password_otp_verification/',views.reset_password_otp_verification,name="reset_password_otp_verification"),
 path('reset_password/',views.reset_password,name="reset_password"),
]