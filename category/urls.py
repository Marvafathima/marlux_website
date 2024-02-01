from django.urls import path
from . import views
app_name = 'category'
urlpatterns=[
    path('category/',views.add_category,name='addcategory'),
    path('category/category_list',views.category_list,name='category_list'),
    path('category/update_category/<int:id>',views.update_category,name='update_category'),
    path('category/delete_category/<int:id>',views.del_category,name='delete_category'),
    path('category/add_subcategory',views.add_subcategory,name='add_subcategory'),
]