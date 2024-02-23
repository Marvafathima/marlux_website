from django.urls import path
from . import views
urlpatterns=[

path('create_coupon/',views.create_coupon,name="create_coupon"),
path('view_coupon/',views.view_coupon,name="view_coupon"),
path('update_coupon/<int:id>/',views.update_coupon,name='update_coupon')
]