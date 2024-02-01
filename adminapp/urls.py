from django.urls import path
from . import views as admin_views
from category import views as category_views
app_name = 'adminapp'
urlpatterns=[
    # path('home/',views.index,name='home'),
    # path('login/',views.user_login,name='login'),
    # path('otp/<str:uid>/', views.otpVerify, name='otp'),
    # path('',views.user_signup,name='signup'),
    path('adminlogout/',admin_views.admin_logout,name='alogout'),
    path('custadmin/',admin_views.custom_admin,name='admin'),
    path('dashboard/',admin_views.admin_dashboard,name='dashboard'),
    path('dashboard/userlist/',admin_views.admin_userlist,name='userlist'),
    path('dashboard/userlist/unblock/<int:user_id>/',admin_views.user_unblock,name='unblock_user'),
    path('dashboard/userlist/block/<int:user_id>/',admin_views.user_block,name='block_user'),
    path('dashboard/category',category_views.add_category,name='addcategory'),
    path('dashboard/category/category_list',category_views.category_list,name='category_list'),
    path('dashboard/category/update_category/<int:id>',category_views.update_category,name='update_category'),
    path('dashboard/category/delete_category/<int:id>',category_views.del_category,name='delete_category'),
    path('dashboard/category/add_subcategory',category_views.add_subcategory,name='add_subcategory'),
]