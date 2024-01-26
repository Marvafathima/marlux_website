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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
          
def admin_dashboard(request):
    return render(request,"adminside/dashboard.html")
def admin_logout(request):
    logout(request)
    return redirect('adminapp:admin')
# # Create your views here.
# def admin_userlist(request):

#     user_list=User.objects.values('email','user_name','phone_number','is_active','date_joined')
#     items_per_page = 15
#     paginator = Paginator(user_list, items_per_page)
#     page = request.GET.get('page', 1)
#     try:
#         users = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         users = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g., 9999), deliver last page of results.
#         users = paginator.page(paginator.num_pages)
#     context = {'userlist': users}
#     return render(request, "adminside/userlist.html", context)