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
from .models import Order,OrderAddress,OrderProduct
from django.db import transaction
# Create your views here.
@login_required
def cart_to_order(request,cart_id):
    
    cart=Cart.objects.get(id=cart_id)
    cart_items=CartItem.objects.filter(cart=cart)
    us=request.user
    user=CustomUser.objects.get(id=us.id)
    address=Address.objects.get(user=us,is_default=True)
    cust_detail=UserAddress.objects.get(user=us)
    context={
        'cart':cart,
        'cart_items':cart_items,
        'address':address,
        'user':user,
        'cust_detail':cust_detail
    }
    return render (request,'checkout.html',{'context':context})
def order_display(request):
    user=request.user
    cart=Cart.objects.get(user=user.id)
    items=CartItem.objects.filter(cart=cart)
    cart_user=CustomUser.objects.get(id=user.id)
    address=Address.objects.get(user=user,is_default=True)
    cust_detail=UserAddress.objects.get(user=user)
    order_address=OrderAddress.objects.create(
        user=user,
        house_name=address.house_name,
        street=address.street,
        city=address.city,
        district=address.district,
        landmark=address.landmark,
        state=address.state,
        postal_code=address.postal_code,
        country = address.country
      
    )
    order=Order.objects.create(user=user,address=order_address,order_total=cart.cart_total,total_qnty=cart.total_qnty)
    for item in items:
         OrderProduct.objects.create(
                    order=order,
                    product_variant=item.product_variant,
                    quantity=item.quantity,
                    item_total_price=item.item_total_price
                )
   
   
    od_items=OrderProduct.objects.filter(order=order)
   
    return render (request,'orderdisplay.html',{
        'order':order,
        'order_items':od_items,
        'address':order_address,
        'user':cart_user,
        'user_detail':cust_detail

    })

def order_item_display(request):
    pass