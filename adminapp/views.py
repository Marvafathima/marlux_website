from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
# from .models import Profiles,User
import random
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from home.models import UserAddress ,CustomUser,Address
from order_mamngmnt .models import Order,OrderProduct
from datetime import datetime, timedelta
from django.db.models import Sum
# Create your views here.
@ensure_csrf_cookie
def custom_admin(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        
        # Authenticate using email and password
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_superuser:
            # Log the user in
            login(request, user)
            return redirect('adminapp:dashboard')
        else:
            messages.info(request, "Invalid admin credentials")
            return redirect('adminapp:admin')

    return render(request, "adminside/index.html")
@login_required(login_url='adminapp:admin')         
def admin_dashboard(request):
    return render(request,"adminside/dashboard.html")
def admin_logout(request):
    
    logout(request)
    return redirect('adminapp:admin')
# # Create your views here.
def admin_userlist(request):
    user_data = CustomUser.objects.select_related('useraddress').values('id', 'email','is_active','useraddress__user_name','useraddress__phone_number')
    context = {'userlist':user_data}
    return render(request, "adminside/userlist.html", context)

def user_unblock(request,user_id):
    us=CustomUser.objects.filter(id=user_id).first()
    us.is_active=True
    us.save()
    return redirect('adminapp:userlist')
def user_block(request,user_id):
    us=CustomUser.objects.filter(id=user_id).first()
    print(us)
    us.is_active=False
    us.save()
    return redirect('adminapp:userlist')
def sales(request):
    if request.method=="POST":
        start_date=request.POST.get("start_date")
        end_date=request.POST.get("end_date")
        day=request.POST.get("day")
        print(day)
        formatted_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        formatted_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        orders=Order.objects.filter(created_at__range=[formatted_start_date,formatted_end_date])
        total_orders=orders.count()
        total_days=0
        if day=="day":
            total_days=1
        elif day=="week":
            total_days=7
        elif day=="month":
            total_days=30
        avg_order=total_orders/total_days
        total_sale=Order.objects.aggregate(total_sale=Sum('grand_total'))
        return render (request,"salesview.html",)

    else:

    
        start_date_month=datetime.now()-timedelta(days=30)
        start_date_week=datetime.now()-timedelta(days=7)
        print(start_date_month,"one month before")
        print(start_date_week,"one year before")
        end_date = datetime.now()
        print(end_date.strftime("%Y-%m-%d"),"todays date")
        return render(request,'sales.html',{
            'start_date_week':start_date_week.strftime("%Y-%m-%d"),
            'start_date_month':start_date_month.strftime("%Y-%m-%d"),
            'end_date':end_date.strftime("%Y-%m-%d")
        })
    
        
        # 
    return render(request,'sales.html',)




 