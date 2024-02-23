from django.shortcuts import render,redirect,get_object_or_404
from .models import Coupon
from category .models import Products,Category,Subcategory,ProductVar,Brand, Color, Size,ProductImage
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
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
        
        minimum_order_amount=request.POST.get('min_amount')
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
                description=description

            )
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
    coupon=Coupon.objects.get(id=id)
    if request.method=="POST":
        if 'code' in request.POST:
            code = request.POST.get('code')
        if 'discount_amount' in request.POST:    
            discount_amount = request.POST.get('discount_amount')
        if 'discount_percentage' in request.POST:    
            discount_percentage=request.POST.get('discount_percentage')
        if 'expiration_date' in request.POST:  
            expiration_date = request.POST.get('expiration_date')
        if 'usage_limit' in request.POST:    
            usage_limit = request.POST.get('usage_limit')
        if 'user_limit' in request.POST:    
            user_limit=request.POST.get('user_limit')
        if 'minimum_order_amount' in request.POST:
            minimum_order_amount=request.POST.get('min_amount')
        if 'description' in request.POST:    
            description=request.POST.get('description')
        if 'active' in request.POST:
            active=request.POST.get('active')=='on'
        else:
            active = False
        return render (request,'view_coupon.html')
    else:
        return render(request,'edit_coupon.html',{'coupon':coupon})
        
