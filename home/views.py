from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import CustomUser,UserAddress
import random
from .helper import MessageHandler
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from category.models import Products,ProductImage,ProductVar,Category,Subcategory,Color,Size
from django.db.models import Min
@login_required(login_url='login')
def index(request):
    # products = Products.objects.annotate(
    #     lowest_price=Min('product_varient__price'),
    #     prod_image=Min('product_image__image')).values('pr_name','lowest_price','prod_image')
    # for product in products:
    #     print(product['prod_image']) 
    products=Products.objects.all()
    category=Category.objects.all()
    return render(request,'userside/index.html',{'products':products,'categories':category})
def categoryproduct(request,category_id):
    cat=get_object_or_404(Category, pk=category_id)
    subcat=Subcategory.objects.filter(cat_id=category_id)
    prod=Products.objects.filter(cat_id=category_id)
    return render(request, 'shop.html', {'cat': cat, 'prod': prod,'subcat':subcat})

def product_detail(request,id):
    products=Products.objects.get(pk=id)
    images=ProductImage.objects.filter(img_id=id)
    varients=ProductVar.objects.filter(prod_id=products)
    colors=ProductVar.objects.filter(prod_id=products).values('color__id','color__color').distinct()
    print(colors)
    sizes =ProductVar.objects.filter(prod_id=products).values('size__id','size__size').distinct()
    print(images)
    return render(request,'userside/detail.html',{'products':products,' images':images,'varients':varients,'colors':colors,'sizes':sizes})
def get_price(request):
    if request.method == 'GET':
        size_id = request.GET.get('size')
        color_id = request.GET.get('color')

        try:
            product_variant = ProductVar.objects.get(size=size_id, color=color_id)
            price = product_variant.price
        except ProductVar.DoesNotExist:
            price = None
        print(price)
        return JsonResponse({'price': price})


def user_login(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['passw']
        print(email,password)
        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            # messages.success(request,'Successfully loged in')
            return redirect('home')
        elif user is not None and not user.is_active:
            messages.error(request, "Your account is not active. Please contact support.")
            print("hellooo")
            return redirect('login')
        else:
            messages.error(request,"invalid user name or password")
            return redirect('login')
    return render(request,'userside/user_login.html')

def user_signup(request):
    if request.method=='POST':
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        user_name=request.POST.get('user_name')
        phone_number=request.POST.get('phone_number')

        if not email or not pass1 or not pass2:
            messages.error(request,'Please fill this fields.')
            return render(request,'userside/user_signup.html')
        if len(pass1)<6 or not any(char.isupper() for char in pass1)or not any(char.isdigit() for char in pass1):
            messages.error(request,'password must have atleast 6 characters with atleast one uppercase and numbers.')
            return render(request,'userside/user_signup.html')
        if pass1!=pass2:
            messages.error(request, "Your password and confirm Password are not the same")
            return redirect('signup')
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered")
            return redirect('signup')
       
        otp=str(random.randint(10000,99999))
        print(otp)

        subject = 'OTP Verification'
        message = f'Your OTP for registration is: {otp}'
        sender = 'marvafathima62@gmail.com'  # Replace with your email
        recipient = [email]

        try:
            send_mail(subject, message, sender, recipient, fail_silently=False)
        except Exception as e:
            return HttpResponse(f"Error sending email: {e}")

        # Store OTP in session
        request.session['otp'] = otp
        request.session['password'] = pass1
        # Redirect to the OTP verification page
        return render(request, 'userside/otpVerify.html', {'email': email,'user_name':user_name,'phone_number':phone_number})
       
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

def otpVerify(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        email = request.POST.get('email')
        phone_number=request.POST.get('phone_number')
        user_name=request.POST.get('user_name')
        stored_otp = request.session.get('otp')
        print(entered_otp)
        print(stored_otp)

        if entered_otp == stored_otp:
            # OTP is correct, create the user
            user = CustomUser.objects.create_user(email=email, password=request.session.get('password'),is_active=True)
            user_details=UserAddress.objects.create(user=user,user_name=user_name,phone_number=phone_number)
            messages.success(request, "User created successfully")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, 'userside/otpVerify.html', {'email': email,'user_name':user_name,'phone_number':phone_number})

    return render(request, 'userside/otpVerify.html')





def user_logout(request):
    logout(request)
    return redirect('login')


def shop(request):
    products=Products.objects.all()
    return render (request,'shop.html',{'products': products})

