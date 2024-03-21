from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from home.models import CustomUser,UserAddress,Cart,CartItem,Address
import random

from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from category.models import Products,ProductImage,ProductVar,Category,Subcategory,Color,Size,Brand
from django.db.models import Min
from django.db.models import F, Sum
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from django.contrib.auth.hashers import check_password
from wishlist .models import Wishlist
# Create your views here.


def forgot_password(request):
    if request.method =="POST":
        email=request.POST.get('email')
        try:
            user=CustomUser.objects.get(email=email)
            otp=str(random.randint(10000,99999))
            subject = 'OTP For Resetting Your Password'
            message = f'Your OTP for reset password is: {otp}'
            sender = 'marvafathima62@gmail.com'  # Replace with your email
            recipient = [email]

            try:
                send_mail(subject, message, sender, recipient, fail_silently=False)
                print(otp)
            except Exception as e:
                return HttpResponse(f"Error sending email: {e}")

            # Store OTP in session
            if 'reset_password_otp' in request.session:
                del request.session['reset_password_otp']
            if 'reset_password_email' in request.session:
                del request.session['reset_password_email']

            request.session['reset_password_otp'] = otp
            request.session['reset_password_email'] = email
           
            return render(request,"reset_password_otp.html",{'email':email})
        except:
            messages.error(request,"no user exist with this email.")
            return redirect('forgot_password')
        
      
    return render(request,'forgot_password.html')

def reset_password_otp_verification(request):
    if request.method=="POST":
        
        otp=request.POST.get('otp')

        session_email=request.session.get('reset_password_email')
        session_otp=request.session.get('reset_password_otp')
        if otp==session_otp:
            return render(request,'reset_password.html',{'email':session_email})
        elif otp != session_otp:
            del request.session['reset_password_otp']
            del request.session['reset_password_email']
            messages.error(request,"incorrect OTP")
            return redirect("reset_password_otp_verification")
    
    return render (request,"reset_password_otp.html")
def reset_password(request):
    
    if request.method=="POST":
        email=request.POST.get("email")
       
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        user=CustomUser.objects.get(email=email)
        
        if user:
            if password1==password2:
                user.set_password(password1)
                user.save()
                messages.success(request,"password resetted successfully")
                return redirect('login')
            else:
                messages.error(request,"password and confirm password is not same")
                return redirect('reset_password')
        else:
            messages.error("error fetching user")
            return redirect('reset_password',{'email':email})
    else:
        session_email=request.session.get('reset_password_otp')
        session_otp=request.session.get('reset_password_email')
        del request.session['reset_password_otp']
        del request.session['reset_password_email']
        return render(request,"reset_password.html",{'email':session_email})
    
