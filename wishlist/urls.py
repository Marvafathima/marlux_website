from django.urls import path
from . import views
urlpatterns=[

    path("wishlist/<int:id>/",views.add_to_wishlist,name="wishlist"),
    path("view_wishlist/",views.view_wishlist,name="view_wishlist"),
 path("remove_wishlist/<int:id>/",views.remove_wishlist,name="remove_wishlist"),

    
]