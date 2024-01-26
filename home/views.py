from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import CustomUser
import random
from .helper import MessageHandler
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request):
    return render(request,'userside/index.html')
    # if request.COOKIES.get('verified') and request.COOKIES.get('verified')!=None:
    #     return redirect('home')
    # else:
    #     return HttpResponse("Not verified")
def user_login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['passw']
        print(email,password)
        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Successfully loged in')
            return redirect('home')
        else:
            messages.error(request,"invalid user name or password")
            return redirect('login')
    return render(request,'userside/user_login.html')

def user_signup(request):
    if request.method=='POST':
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if not email or not pass1 or not pass2:
            messages.error(request,'Please fill this fields.')
            return render(request,'userside/user_signup.html')
        if len(pass1)<8 or not any(char.isupper() for char in pass1)or not any(char.isdigit() for char in pass1):
            messages.error(request,'password must have atleast 8 characters with atleast one uppercase and numbers.')
            return render(request,'userside/user_signup.html')
        if pass1!=pass2:
            messages.error(request, "Your password and confirm Password are not the same")
            return redirect('signup')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered")
            return redirect('signup')
        else:
            user=CustomUser.objects.create_user(email=request.POST['email'],password=request.POST['pass1'])
            messages.success(request, "User created successfully")
            return redirect('login')
    return render(request,'userside/user_signup.html')





    # if request.method=="POST":
    #     print(request.POST)
    #     pass1=request.POST['pass1']
    #     pass2=request.POST['pass2']
    #     email=request.POST['email']
    #     if pass1!=pass2:
    #         messages.error(request,"password and confirm password are not the same")
    #         return redirect('signup')
    #     if User.objects.filter(email__iexact=request.POST['email']).exists():
    #         messages.error(request, "User already exists")
    #         return redirect('signup')
        
    #     user=User.objects.create(email=request.POST['email'],password=request.POST['pass1'],user_name=request.POST['user_name'],phone_number=request.POST['phone_number'])
    #     otp=random.randint(1000,9999)
    #     profile=Profiles.objects.create(user=user,phone_number=request.POST['phone_number'],otp=f'{otp}')
    #     messagehandler=MessageHandler(request.POST['phone_number'],otp).send_otp_via_message()
    #     red=redirect(f'otp/{profile.uid}/')
    #     red.set_cookie("can_otp_enter",True,max_age=600)
    #     return red
    # return render(request,'userside/user_signup.html')

def user_logout(request):
    logout(request)
    return redirect('login')


# def otpVerify(request,uid):
#     if request.method=="POST":
#         profile=Profiles.objects.get(uid=uid)
#         if request.COOKIES.get('can_otp_enter')!=None:
#             if(profile.otp==request.POST['otp']):
#                 red=redirect("home")
#                 red.set_cookie('verified',True)
#                 return red
#             messages.error(request,"wrong otp")
#             return render(request,'otpVerify')
#         messages.error(request,"10 minutes passed")   
#         return render(request,'otpVerify')
#     return render(request,"userside/otpVerify.html",{'id':uid})
    
# def user_logout(request):
#     pass


