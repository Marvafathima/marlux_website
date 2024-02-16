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
    user=request.user
    try:
        cart=Cart.objects.get(id=cart_id)
        cartitems=CartItem.objects.filter(cart=cart)
        total_qnty=cart.total_qnty
        total_price=float(cart.total_price)
    # with transaction.atomic():
        order=Order.objects.create(user=user,order_total=total_price,order_name="order")
        for items in cartitems:
            product_variant=items.product_variant
            quantity=items.quantity
            price=items.item_total_price
            OrderProduct.objects.create(
                order=order,
                product_variant=product_variant,
                quantity=quantity,
                price=price,
                item_total_price=items.item_total_price
                )
        cart.is_ordered=True
        cart.save()
        order_items=OrderProduct.objects.filter(order=order)
        print("yesss!!!!!!!!!!!worked")
        return render(request,'checkout.html',{'order_items':order_items,'order':order})
    except Cart.DoesNotExist:
        print("exception has occured babyy")
        messages.error(request, "You don't have any items in your cart.")
        # return render(request,'checkout.html')
        return redirect('cart')
# @login_required
# def confirm_order(request,order_id):
#     user=request.user
#     try:
#         cart=Cart.objects.get(user=user)
#         order=Order.objects.get(id=order_id)
#         order.is_ordered=True
#         order.status='Confirmed'
#         order.save()
#         cart.delete()
#         messages.success(request,"order placed successfully!")
#         return redirect('order_list',order_id=order.id)

#     except Cart.DoesNotExist:
#         messages.error(request, "You don't have any items in your cart.")
#         return redirect('cart')

# def order_list(request,)
    
