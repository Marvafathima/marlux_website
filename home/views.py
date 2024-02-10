from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import CustomUser,UserAddress,Cart,CartItem
import random
from .helper import MessageHandler
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from category.models import Products,ProductImage,ProductVar,Category,Subcategory,Color,Size
from django.db.models import Min
from django.db.models import F, Sum
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

def product_detail(request, id):
    products = Products.objects.get(pk=id)
    images = ProductImage.objects.filter(img_id=id)
    varients = ProductVar.objects.filter(prod_id=products)
    colors = Color.objects.filter(product_color__prod_id=products).distinct()
    sizes = Size.objects.filter(product_size__prod_id=products).distinct()
    print(colors)
    print(sizes)
    return render(request, 'userside/detail.html', {'products': products, 'images': images, 'varients': varients, 'colors': colors, 'sizes': sizes})

def get_sizes(request):
    if request.method == 'GET' and request.is_ajax():
        color_id = request.GET.get('color')
        sizes = ProductVar.objects.filter(color=color_id).values('size__id', 'size__size').distinct()
        sizes_list = list(sizes)
        return JsonResponse({'sizes': sizes_list})
    return JsonResponse({})



def get_price(request):
    color_id = request.GET.get('color_id')
    size_id = request.GET.get('size_id')
    
    try:
        product_var = ProductVar.objects.get(color_id=color_id, size_id=size_id)
        price = product_var.price
        return JsonResponse({'price': price})
    except ProductVar.DoesNotExist:
        return JsonResponse({'price': None}) 
@login_required(login_url='login')
def add_to_cart(request):
    color_id = request.GET.get('color_id')
    size_id = request.GET.get('size_id')
    quantity = request.GET.get('quantity')
    
    try:
        product_var = ProductVar.objects.get(color_id=color_id, size_id=size_id)
    except ProductVar.DoesNotExist:
        return JsonResponse({'error': 'Product unavailable'}, status=400)
    user = request.user
    if not user.is_authenticated:
        # Handle anonymous user (optional)
        # You can create a session-based cart for anonymous users
        # or handle the scenario based on your application's requirements
        return JsonResponse({'message': 'Anonymous users cannot add items to the cart.'}, status=400)
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_variant=product_var)
    if not created:
        # If the cart item already exists, update the quantity
        cart_item.quantity += int(quantity)
        cart_item.save()
    cart.total_qnty = CartItem.objects.filter(cart=cart).aggregate(total_quantity=Sum('quantity'))['total_quantity']
    cart.total_price = CartItem.objects.filter(cart=cart).aggregate(total_price=Sum(F('quantity') * F('product_variant__price')))['total_price']
    cart.save()
    return JsonResponse({'message': 'Product added to cart successfully.'})

def cart(request):
    print('cart selected')
    user=request.user
    carts=Cart.objects.get(user=user.id)
    cart_items=CartItem.objects.filter(cart__user=user.id)
    for cart_item in cart_items:
        product_name=cart_item.product_variant.prod_id.pr_name
        print(product_name)
    
    return render(request,'cart.html',{'cart_items':cart_items,'carts':carts})
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

