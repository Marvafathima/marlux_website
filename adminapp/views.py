from django.shortcuts import render

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
from home.models import UserAddress ,CustomUser

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
    if us.is_active==True:
        us.is_active=False
        us.save()
    return redirect('adminapp:userlist')
def user_block(request,user_id):
    us=CustomUser.objects.filter(id=user_id).first()
    if us.is_active==False:
        us.is_active=True
        us.save()
    return redirect('adminapp:userlist')




    
#     user_list=CustomUser.objects.all('id','email','is_active','date_joined')
#     user_detail=UserAddress.objects.values('user_name','phone_number')
#     #combining both query set
#     combined_data=[]
#     for user in user_list:
#         user_id = user.get('id')
#         user_address_detail = user_detail.filter(user_id=user_id).first()
#         combined_data.append({**user, **user_address_detail})
#     items_per_page = 15
#     paginator = Paginator(combined_data, items_per_page)
#     page = request.GET.get('page', 1)
    
#     try:
#         users = paginator.page(page)
#     except PageNotAnInteger:
#         users = paginator.page(1)
#     except EmptyPage:
#         users = paginator.page(paginator.num_pages)

#     context = {'userlist': users}
#     return render(request, "adminside/userlist.html", context)