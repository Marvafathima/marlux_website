from django.urls import path
from . import views
app_name = 'category'
urlpatterns=[
    path('category/',views.add_category,name='addcategory'),
    path('category/category_list',views.category_list,name='category_list'),
    path('category/update_category/<int:id>',views.update_category,name='update_category'),
    path('category/delete_category/<int:id>',views.del_category,name='delete_category'),
    path('category/add_subcategory',views.add_subcategory,name='add_subcategory'),
    path('dashboard/products/product_list',views.list_product,name='list_product'),
    path('product_variant_list/<int:id>',views.product_variant_list,name='product_variant_list'),
]