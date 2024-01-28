from django.urls import path
from . import views
app_name = 'category'
urlpatterns=[
    path('category/',views.add_category,name='addcategory')

    # path('adminlogout/',views.admin_logout,name='alogout'),
    # path('custadmin/',views.custom_admin,name='admin'),
    # path('dashboard/',views.admin_dashboard,name='dashboard'),
    # path('dashboard/userlist/',views.admin_userlist,name='userlist'),
    # path('dashboard/userlist/unblock/<int:user_id>/',views.user_unblock,name='unblock_user'),
    # path('dashboard/userlist/block/<int:user_id>/',views.user_block,name='block_user'),
]