from django.shortcuts import render,redirect,get_object_or_404
from .models import Coupon
from category .models import Products,Category,Subcategory,ProductVar,Brand, Color, Size,ProductImage
from home .models import Cart,CartItem,CustomUser,Address
from order_mamngmnt .models import Order,OrderProduct
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from decimal import Decimal
from django.template.defaultfilters import date
from django.utils import timezone
# Create your views here.
def create_coupon(request):
    if request.method == 'POST':
        print("reached here")
        code = request.POST.get('code')
        discount_amount = request.POST.get('discount_amount')
        discount_percentage=request.POST.get('discount_percentage')
        expiration_date = request.POST.get('expiration_date')
        usage_limit = request.POST.get('usage_limit')
        user_limit=request.POST.get('user_limit')
        if 'purchase_count' in request.POST:
            purchase_count=request.POST.get('purchase_count')
        minimum_order_amount=request.POST.get('minimum_order_amount')
        description=request.POST.get('description')
        if 'active' in request.POST:
            active=request.POST.get('active')=='on'
        else:
            active = False

        try:
            coupon = Coupon.objects.create(
                code=code,
                expiration_date=expiration_date,
                usage_limit=usage_limit,
                user_limit=user_limit,
                active=active,
                minimum_order_amount=minimum_order_amount,
                description=description,
               

            )
            if purchase_count:
                 coupon.purchase_count=purchase_count

            
            if discount_amount:
                coupon.discount_amount=discount_amount
            if discount_percentage:
                coupon.discount_percentage=discount_percentage
            coupon.save()
            messages.success(request, "Coupon created successfully.")
            return redirect('view_coupon')
        except:
            print("Error creating coupon.")
            messages.error(request, "Error creating coupon.")
            return render(request, 'add_coupon.html')
    else:
        return render(request, 'add_coupon.html')
def view_coupon(request):
    try:
        coupons=Coupon.objects.all()
        return render (request,'view_coupon.html',{'coupons':coupons})
    except:
        return render (request,'view_coupon.html')
def update_coupon(request,id):
    print("update called")
    coupon=Coupon.objects.get(id=id)
    # coupon.expiration_date = date(coupon.expiration_date, 'd/m/Y') 
    print(coupon.expiration_date)
    if request.method=="POST":
        if 'code' in request.POST:
            code = request.POST.get('code')
            coupon.code=code
        try:     
            discount_amount = request.POST.get('discount_amount')
            coupon.discount_amount=Decimal(discount_amount)
        except:   
            discount_percentage=request.POST.get('discount_percentage')
            coupon.discount_percentage=Decimal(discount_percentage)
        if 'expiration_date' in request.POST:  
            expiration_date = request.POST.get('expiration_date')
            coupon.expiration_date=expiration_date
            
        if 'usage_limit' in request.POST:    
            usage_limit = request.POST.get('usage_limit')
            coupon.usage_limit=usage_limit
        if 'user_limit' in request.POST:    
            user_limit=request.POST.get('user_limit')
            coupon.user_limit=user_limit
        if 'minimum_order_amount' in request.POST:
            minimum_order_amount=request.POST.get('minimum_order_amount')
            coupon.minimum_order_amount=minimum_order_amount
       
        if 'purchase_count' in request.POST:
            purchase_count=request.POST.get('purchase_count')
            if purchase_count.strip():
  
                try:
                    purchase_count=int(purchase_count)
                    coupon.purchase_count=purchase_count
                except:
                    
                    print("no purchase count")
            else:
                coupon.purchase_count=None
        if 'description' in request.POST:    
            description=request.POST.get('description')
            coupon.description=description
        if 'active' in request.POST:
            active=request.POST.get('active')=='on'
        else:
            active = False
        coupon.active=active
        coupon.save()
        return redirect('view_coupon')
    else:
        return render(request,'edit_coupon.html',{'coupon':coupon})
def delete_coupon(request,id):
    coupon=Coupon.objects.get(pk=id)
    coupon.delete()
    return redirect('view_coupon')
        
def user_coupons(request):
    coupon=Coupon.objects.all()
    return render(request,'coupons.html',{'coupons':coupon})
def apply_coupon(request):
    user=request.user
    code=request.POST.get('code') 
    print(code,'this is the code')
    try:
        coupon=Coupon.objects.get(code=code)
        if coupon.discount_amount:
            print(coupon.discount_amount)
        else:
            print(coupon.discount_percentage)
        if coupon.is_valid():
            cart=Cart.objects.get(user=user.id)
            cart_items=CartItem.objects.filter(cart__user=user.id)
            try:
            
                address=Address.objects.get(user=user,is_default=True)
            except:
                address=None
            grand_total=cart.total_price
            user_limit=cart.coupon_count
            print(cart.total_price,cart.coupon_count,"coupon valid")
            try:
                order_count=Order.objects.filter(user=user).count()
            
            except:
                order_count=0
        
            if coupon.minimum_order_amount==None:
                coupon.minimum_order_amount=0
            if float(grand_total)< float(coupon.minimum_order_amount):
                messages.error(request,"oops.total purchase amount is low to apply this coupon.add more to cart.")
                return render(request,'cart.html',{'carts':cart,'cart_items':cart_items,'address':address})
            if user_limit>40:
                messages.error(request,"It seems like you have Already applied a coupon")
                return render(request,'cart.html',{'carts':cart,'cart_items':cart_items,'address':address})
            if coupon.purchase_count is not None:
                if order_count != coupon.purchase_count:
                    messages.error(request,"you are not eligible for this coupon.either you need to be either  new to the website or a regular customer")
                    return render(request,'cart.html',{'carts':cart,'cart_items':cart_items,'address':address})
            else:
                order_count=None
            
            if float(grand_total)>= float(coupon.minimum_order_amount) and user_limit<=40 and order_count==coupon.purchase_count:
                if coupon.discount_amount:
                    cart.discount_amount=coupon.discount_amount
                    cart.coupon_price=cart.total_price-coupon.discount_amount
                    cart.coupon_cart_total=cart.coupon_price+cart.tax+cart.shipping
                    # cart.total_price-=coupon.discount_amount
                    print(cart.discount_amount,"added discount amount")
                    cart.save()
                else:
                    grand_total=(coupon.discount_percentage * grand_total)/100
                    cart.discount_amount=grand_total
                    cart.coupon_price=cart.total_price-grand_total
                    cart.coupon_cart_total=cart.coupon_price+cart.tax+cart.shipping
                    # cart.total_price-=grand_total
                    print(cart.discount_amount,"discount percentage in amount")
                    cart.save()
                cart.applied_coupon=coupon
                
                cart.save()
                print(cart.coupon_price,"this is the new total")
                messages.success(request,"coupon applied successfully!")
                return render(request,'cart.html',{'carts':cart,'cart_items':cart_items,'address':address,'coupon':coupon})
            
            else:
                coupon.active==False
                coupon.save()
                print("exceeded the limit")
                messages.error(request,"coupon limit exceeded")
            
            return render(request,'cart.html',{'carts':cart,'cart_items':cart_items,'address':address})
        else:
            messages.error(request,"Coupon is not valid")
            return redirect('cart')

    except:
        messages.error(request,"No matching coupon found!!Apply valid code")
        
    return redirect('cart')
       

    

   
        

