from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from home .models import CustomUser,UserAddress,Cart,CartItem,Address
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from category.models import Products,ProductImage,ProductVar,Category,Subcategory,Color,Size
from django.db.models import Min
from django.db.models import F, Sum
from django.views.decorators.csrf import csrf_protect
from django.db import transaction
from django.core.serializers.json import DjangoJSONEncoder
from coupons .models import Coupon
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from home.models import CustomUser,UserAddress,Cart,CartItem,Address
from .models import Wishlist
from django.urls import reverse
# Create your views here.
def add_to_wishlist(request,id):
    user=request.user
    product=Products.objects.get(id=id)
    wishlist=Wishlist.objects.create(user=user,product=product)
    messages.success(request,"Product added to wishlist")
    return redirect(request.META.get('HTTP_REFERER', '/'))




def view_wishlist(request):
    user=request.user  
    wishlists=Wishlist.objects.filter(user=user)
    return render (request,'wishlist.html',{'wishlists':wishlists})
def remove_wishlist(request,id):
    wishlist=Wishlist.objects.get(id=id)
    wishlist.delete()
    messages.error(request,"product removed from wishlist succesfully")
    return redirect('view_wishlist')




