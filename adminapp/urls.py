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
    path('dashboard/products/add_product',category_views.add_product,name='add_product'),
    path('dashboard/products/delete_product/<int:id>',category_views.delete_product,name='delete_product'),
    path('dashboard/products/update_product/<int:id>',category_views.update_product,name='update_product'),
    path('dashboard/products/product_list',category_views.list_product,name='list_product'),
    path('dashboard/sales',admin_views.sales,name='sales'),
    path('download_pdf/',admin_views.download_pdf,name='download_pdf'),
    path('get_filter_options/',admin_views.get_filter_options,name='get_filter_options'),
    path('get_sales_chart/<int:year>/',admin_views.get_sales_chart,name="get_sales_chart"),
    path('spend_per_customer_chart/<int:year>/',admin_views.spend_per_customer_chart,name="spend_per_customer_chart"),
    path('sale_statistics/',admin_views.sale_statistics,name="sale_statistics"),
    path('top_selling_product/',admin_views.top_selling_product,name="top_selling_product"),
    # path('get_recent_purchases/',admin_views.get_recent_purchases,name="get_recent_purchases"),
    path('top_seller',admin_views.top_seller,name="top_seller"),
    ]