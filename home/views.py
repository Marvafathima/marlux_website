from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import Profiles,User
import random
from .helper import MessageHandler
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
@login_required
def index(request):
    if request.COOKIES.get('verified') and request.COOKIES.get('verified')!=None:
        return redirect('home')
    else:
        return HttpResponse("Not verified")
def user_login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['passw']
        print(email,password)
        if User.objects.filter(email__iexact=email).exists():
            us=User.objects.get(email__iexact=email)
            if us.password!=request.POST['passw']:
                messages.info(request,"incorrect password!")
                return redirect('login')
            login(request,us)
            return render(request,'userside/index.html')
          
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request,'userside/user_login.html')

def user_signup(request):
    if request.method=="POST":
        print(request.POST)
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        email=request.POST['email']
        if pass1!=pass2:
            messages.error(request,"password and confirm password are not the same")
            return redirect('signup')
        if User.objects.filter(email__iexact=request.POST['email']).exists():
            messages.error(request, "User already exists")
            return redirect('signup')
        
        user=User.objects.create(email=request.POST['email'],password=request.POST['pass1'],user_name=request.POST['user_name'],phone_number=request.POST['phone_number'])
        otp=random.randint(1000,9999)
        profile=Profiles.objects.create(user=user,phone_number=request.POST['phone_number'],otp=f'{otp}')
        messagehandler=MessageHandler(request.POST['phone_number'],otp).send_otp_via_message()
        red=redirect(f'otp/{profile.uid}/')
        red.set_cookie("can_otp_enter",True,max_age=600)
        return red
    return render(request,'userside/user_signup.html')
def otpVerify(request,uid):
    if request.method=="POST":
        profile=Profiles.objects.get(uid=uid)
        if request.COOKIES.get('can_otp_enter')!=None:
            if(profile.otp==request.POST['otp']):
                red=redirect("home")
                red.set_cookie('verified',True)
                return red
            messages.error(request,"wrong otp")
            return render(request,'otpVerify')
        messages.error(request,"10 minutes passed")   
        return render(request,'otpVerify')
    return render(request,"userside/otpVerify.html",{'id':uid})
    
def user_logout(request):
    pass

def custom_admin(request):
    if request.method=="POST":
        name=request.POST.get('name','')
        password=request.POST.get('password','')
        if name!="admin":
            messages.info(request,"invalid admin name")
            return redirect('admin')
        elif password!="admin":
            messages.info(request,"invalid password")
            return redirect('admin')
        else:
            return redirect('dashboard')
    return render(request,"adminside/index.html")
          
def admin_dashboard(request):
    return render(request,"adminside/dashboard.html")
# Create your views here.
