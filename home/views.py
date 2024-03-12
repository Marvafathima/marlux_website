from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import CustomUser,UserAddress,Cart,CartItem,Address
import random
from .helper import MessageHandler
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
from wishlist .models import Wishlist
def index(request):
   
    products=Products.objects.all()
    category=Category.objects.all()
    user=request.user
    return render(request,'userside/index.html',{'products':products,'categories':category,'cart_count':6})
    
   
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
    if 'product_id' in request.session:
        del request.session['product_id']
    request.session['product_id']=products.id
    iddd=request.session.get('product_id')
    print(iddd,"this is the product id*******************")
    try:
        user=request.user
        user_detail=CustomUser.objects.get(id=user.id)
        return render(request, 'userside/detail.html', {'products': products, 'images': images, 'varients': varients, 'colors': colors, 'sizes': sizes,'user_detail':user_detail})
    except:
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
    product_id=request.session.get('product_id')
    product=Products.objects.filter(pk=product_id)
    print(type(product_id),product_id)
    for p in product:
        print(p.pr_name)
        print("*************************************")
    try:
        product_var = ProductVar.objects.get(prod_id=product_id,color_id=color_id, size_id=size_id)
        price = product_var.price
        print(product_var.id)
        return JsonResponse({'price': price})
    except ProductVar.DoesNotExist:
        return JsonResponse({'price': None}) 
    
@login_required(login_url='login')
def add_to_cart(request):

    color_id = request.GET.get('color_id')
    size_id = request.GET.get('size_id')
    quantity = request.GET.get('quantity')
    product_id=request.session.get('product_id')
    try:
        product_var = ProductVar.objects.get(prod_id=product_id,color_id=color_id, size_id=size_id)
        stocks=product_var.stock
    except ProductVar.DoesNotExist:
        return JsonResponse({'error': 'Product unavailable'}, status=400)
    user = request.user
    if not user.is_authenticated:
        messages.info(request,"Login to add items to the cart")
        return redirect('login')
    
    cart, created = Cart.objects.get_or_create(user=user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product_variant=product_var)
    cart_item.price=product_var.price
    cart_item.save()
    try:
        wishlist=Wishlist.objects.filter(user=user)
        for wish in wishlist:
            if wish.product.id==cart_item.product_variant.prod_id.id:
                wish.delete()
                update_wishlist_count_in_session(request)
    except:
        print("no wishlist")

    print(cart_item.price,"this is cart item price")
    if not created:
        # If the cart item already exists, update the quantity
        cart_item.quantity += int(quantity)
        cart_item.save()
    else:
        # If the cart item is newly created, set its quantity
        cart_item.quantity = int(quantity)
        cart_item.save()
    # cart.total_qnty = CartItem.objects.filter(cart=cart).aggregate(total_quantity=Sum('quantity'))['total_quantity']
    cart.total_qnty = CartItem.objects.filter(cart=cart).count()
    print(cart.total_qnty)
    if cart.total_qnty >0:
        cart.total_price = CartItem.objects.filter(cart=cart).aggregate(total_price=Sum('item_total_price'))['total_price']
        cart.cart_total=cart.shipping+cart.total_price
        cart.save()
    else:
        cart.total_price = 0.00
        cart.cart_total=cart.shipping+cart.total_price
        cart.save()
    return JsonResponse({'message': 'Product added to cart successfully.'})
def update_wishlist_count_in_session(request):
    user = request.user
    wishlist_count = Wishlist.objects.filter(user=user).count()
    if not wishlist_count:
        request.session['wishlist_count'] = "0"
    request.session['wishlist_count'] = wishlist_count    
def cart_login_redirect(request,id):
    messages.error(request,"you need to login first to add items to the cart!")
    return redirect('login')
def cart(request):
    print('cart selected')
    user=request.user
    
    try:
        
        address=Address.objects.get(user=user,is_default=True)
    except:
        address=None
    try:
        carts=Cart.objects.get(user=user.id)
        cart_items=CartItem.objects.filter(cart__user=user.id)
        for cart_item in cart_items:
            product_name=cart_item.product_variant.prod_id.pr_name
        if carts.total_qnty==0:
            carts.total_price=0
            carts.cart_total=carts.total_price + carts.shipping
        
        
        return render(request,'cart.html',{'cart_items':cart_items,'carts':carts,'address':address})
    except:
        return render(request,'emptycart.html')
@require_POST
def update_cart_item(request):
    item_id = request.POST.get('item_id')
    quantity = request.POST.get('quantity')
    cart_id=request.POST.get('cart_id')
    print(request, "called update cart")
    try:
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.quantity = int(quantity)
        cart_item.save()
        
        price = float(cart_item.product_variant.price)
        cart_item_total_price = price * cart_item.quantity
        cart_item.item_total_price = cart_item_total_price
        cart_item.save()
        # Update total price and total quantity for the cart
       
        cart = Cart.objects.get(id=cart_id)
        cart.total_qnty = CartItem.objects.filter(cart=cart).count()
        if cart.total_qnty==0:
            cart.delete()
            return render(request,'emptycart.html')
        else:
            old_price=cart.total_price
            cart.total_price = CartItem.objects.filter(cart=cart).aggregate(total_price=Sum('item_total_price'))['total_price']
            new_price=cart.total_price
        cart.save()
        if cart.coupon_price:
            price_diff=new_price-old_price
            cart.coupon_price+=price_diff
            cart.coupon_cart_total+=price_diff
            cart.save()
            return JsonResponse({
            'success': True,
            'quantity': cart_item.quantity,
            'total_price': cart_item.item_total_price,
            'subtotal':cart.total_price,
            'cart_total':cart.cart_total,
            'tax':cart.tax,
            'coupon_price':cart.coupon_price,
            'coupon_cart_total':cart.coupon_cart_total                                                                                                                                          
        })
            
        return JsonResponse({
            'success': True,
            'quantity': cart_item.quantity,
            'total_price': cart_item.item_total_price,
            'subtotal':cart.total_price,
            'cart_total':cart.cart_total,
            'tax':cart.tax                                                                                                                                              
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Cart item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



def remove_from_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        cart_id= request.POST.get('cart_id')
        user=request.user
        print('remove function called')
        try:
            cart_item = CartItem.objects.get(id=item_id)
            cart=Cart.objects.get(id=cart_id)
            cart.total_price-=cart_item.item_total_price
            cart_item.delete()
           
            qnty=cart_item.quantity 
            cart.total_qnty = CartItem.objects.filter(cart=cart).count()
            # cart.total_qnty=cart.total_qnty-1
            new_qnty= cart.total_qnty

            # cart_item.delete()
            if(cart.total_qnty)==0:
                # cart.total_price=0.00
                # if cart.coupon_price:
                #     cart.coupon_price==0
                #     cart.coupon_cart_total==0
                cart.delete()
                return render(request,'emptycart.html')
            
            # cart.total_qnty = CartItem.objects.filter(cart=cart).count()
            cart.save()
            print(cart.total_price,"NEW UPDATED PRICE AFTER REMOVAL")
    
            return JsonResponse({'message': 'Product removed from the cart',
                                'total_qnty':new_qnty,
                                'subtotal':cart.total_price,
                                'cart_total':cart.cart_total,
                                'tax':cart.tax
                                
                                }, )
           
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Cart item not found'},)
    else:
        return JsonResponse({'error': 'Method not allowed'},)
def cart_count(request):
    user=request.user
    if user is not None:
        try:
            cart=Cart.objects.get(user=user)
            count=cart.total_qnty
            return JsonResponse({'count':count})
        except:
            return JsonResponse({'count':0})
    else:
        return JsonResponse({'count':0})
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
    category=Category.objects.prefetch_related('subcat').all()
    colors=Color.objects.distinct()
    size_order = {
    'XXL': 1,
    'XL': 2,
    'L': 3,
    'M': 4,
    'S': 5,
    'SM': 6
}
    sizes=Size.objects.distinct()
    sorted_sizes = sorted(sizes, key=lambda x: size_order.get(x.size, float('inf')))
    for size in sorted_sizes:
        print(size)
    for c in colors:
        print(c.color)
    brands=Brand.objects.all()
    return render (request,'mainshop.html',{'products': products,'categories':category,'colors':colors,'sizes':sorted_sizes,'brands':brands})


def subcategory_page(request,cat_id,subcat_id,):
    product=Products.objects.filter(Q(subcat_id=subcat_id) & Q(cat_id=cat_id))
    return render (request,'shop.html',{'prod':product})

@require_POST
def search(request):
    print("search called")
    if request.method=="POST":
        print("post request called")
        keyword=request.POST.get("keyword")
        if keyword:
            products=Products.objects.all()
            product=Products.objects.filter(Q(pr_name__icontains=keyword)|
                                            Q(cat_id__name__icontains=keyword)|
                                            Q(brand_id__br_name__icontains=keyword)|
                                            Q(subcat_id__sub_name__icontains=keyword)
                                            )
            if product:
                return render(request,'shop.html',{'prod':product})
            else:
                messages.error(request,"No matching items found!")
                return redirect('home')
            
def price_filter(request):
    if request.method == 'POST' and request.is_ajax():
        selected_ranges = request.POST.getlist('selected_ranges[]')
        # Process selected_ranges and fetch products from the database
        # Replace this with your actual logic to fetch products based on price ranges
        products=Products.objects.prefetch_related('product_variant').filter(
        product_variant__price__gte=min,
        product_variant__price__lte=max)
        
        product_list = [{'name': product.pr_name, 'price': product.product_varient__price,} for product in products]
        return JsonResponse({'products': product_list})
    else:
        # Handle non-ajax requests or other methods
        return JsonResponse({'error': 'Invalid request'})
def filter_data(request):
    colors=request.GET.getlist('color[]')
    brands=request.GET.getlist('brand[]')
    sizes=request.GET.getlist('size[]')
    allproducts=Products.objects.all()
    #one variant checking
    if len(colors)>0 and len(brands)==0 and len(sizes)==0:
        allproducts=Products.objects.prefetch_related('product_varient').filter(
            product_varient__color__id__in=colors
        ).distinct()
        print("color only")
        t=render_to_string('product-list.html',{'products': allproducts})
    
    elif len(brands)>0 and len(colors)==0 and len(sizes)==0:
        allproducts=Products.objects.filter(
            brand_id__in=brands).distinct() 
        print("brand only")
        t=render_to_string('product-list.html',{'products': allproducts})
    elif len(sizes)>0 and len(colors)==0 and len(brands)==0:
        allproducts=Products.objects.prefetch_related('product_varient').filter(
            product_varient__size__id__in=sizes
        ).distinct() 
        print("size only")
        t=render_to_string('product-list.html',{'products': allproducts})

#two variants checking
    elif len(colors)>0 and len(brands)>0 and len(sizes)==0:
        products=Products.objects.prefetch_related('product_varient').filter(
            product_varient__color__id__in=colors).distinct()
        allproducts=products.filter(brand_id__in=brands).distinct()
        
        print("size not")
        t=render_to_string('product-list.html',{'products': allproducts})
    
    elif len(brands)==0 and len(colors)>0 and len(sizes)>0:
        products=Products.objects.prefetch_related('product_varient').filter(
            product_varient__color__id__in=colors).distinct()
        allproducts=products.product_varient__size__id__in=sizes.distinct()
        print("brand not")
        t=render_to_string('product-list.html',{'products': allproducts})
    elif len(sizes)>0 and len(colors)==0 and len(brands)>0:
        products=Products.objects.prefetch_related('product_varient').filter(
            product_varient__size__id__in=sizes).distinct()
        allproducts= products.brand_id__in=brands.distinct()
        print("color not")
        t=render_to_string('product-list.html',{'products': allproducts})   
    
    #three variants checking
    elif len(colors)>0 and len(brands)>0 and len(sizes)>0:
        products1=Products.objects.prefetch_related('product_varient').filter(
           product_varient__color__id__in=colors).distinct()
        products2=products1.brand_id__in=brands.distinct()

        allproducts=products2.product_varient__size__id__in=sizes.distinct()
        print("all3")
        t=render_to_string('product-list.html',{'products': allproducts})


    return JsonResponse({'products':t})
  





def user_profile(request):
    user=request.user
    profile=CustomUser.objects.get(id=user.id)
    print(profile.email)
    if request.method=='GET':
        try:
            useraddress = UserAddress.objects.get(user=user)
            profile=CustomUser.objects.get(id=user.id)
            useraddress = UserAddress.objects.get(user=user)
            us_detail={
                'id':profile.id,
                'name':useraddress.user_name,
                'email':profile.email,
                'password':profile.password,
            'phone_number':useraddress.phone_number
            }
            return render (request,'userprofile.html',{'us':us_detail})
        except:
            return render (request,'userprofile.html')
    else:
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone_number=request.POST.get('number')
        profile.email=email
        profile.save()
       
        useraddress = UserAddress.objects.get(user=user)
        useraddress.user_name=name
        useraddress.phone_number=phone_number
       
        useraddress.save()
        us_detail={
            'id':profile.id,
            'name':useraddress.user_name,
            'email':profile.email,
            'password':profile.password,
           'phone_number':useraddress.phone_number
        }
        return render (request,'userprofile.html',{'us':us_detail})
    
def user_address(request):
    if request.method =='POST':
        print("adress add calleddd")
        house_name=request.POST.get('house_name')
        place=request.POST.get('place')
        city=request.POST.get('city')
        district=request.POST.get('district') 
        pincode=request.POST.get('pin_code') 
        state=request.POST.get('state') 
        country=request.POST.get('country') 
        landmark=request.POST.get('landmark','') 
        print(house_name)
        Address.objects.create(
        user=request.user,
        house_name=house_name,
        street=place,
        city=city,
        district=district,
        postal_code=pincode,
        state=state,
        country=country,
        landmark=landmark
    )
        return redirect('addressdisplay')
        # return render (request,'useraddress.html')
    else:
        print("address get method called ")
        return render (request,'useraddress.html')
        # return redirect('addressdisplay')

def addressdisplay(request):
    user=request.user
    useraddress = Address.objects.filter(user=user)
    if useraddress is not None:
        return render (request,'addressdisplay.html',{'addresses':useraddress})
    else:
        return render (request,'addressdisplay.html')
@csrf_protect
def set_default_address(request):
    print("called set defualt")
    if request.method == 'POST':
        user=request.user
        adrs=Address.objects.filter(user=user)
        for ad in adrs:
            ad.is_default='False'
            ad.save()

        print("loop worked")
        address_id = request.POST.get('address_id')
        address = Address.objects.get(pk=address_id)
        address.is_default = True
        address.save()
        return JsonResponse({'status':"Default address added succesfully "})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
def address_delete(request,id):
    address=Address.objects.get(pk=id)
    address.delete()
    return redirect('addressdisplay')
def update_address(request,id):
    address=get_object_or_404(Address,pk=id)
    print("update address called",id)
    if request.method=="POST":
        house_name=request.POST.get('house_name')
        place=request.POST.get('place')
        city=request.POST.get('city')
        district=request.POST.get('district') 
        pincode=request.POST.get('pin_code') 
        state=request.POST.get('state') 
        country=request.POST.get('country') 
        landmark=request.POST.get('landmark','') 
        print(house_name,country,state)
        address=Address.objects.get(pk=id)
        # Update the attributes of the address instance
        if house_name:
            address.house_name = house_name
        if place:
            address.street = place
        if city:
            address.city = city
        if district:
            address.district = district
        if pincode:
            address.postal_code = pincode
        if state:
            address.state = state
        if country:
            address.country = country
        if landmark:
            address.landmark = landmark

        # Save the updated address instance
        address.save()

        return redirect('addressdisplay')
    else:
        return render (request,'updateaddress.html',{'address':address})
  
def user_password(request):
    user=request.user
    if user.is_authenticated: 
        user=CustomUser.objects.get(id=user.id)
        print(user)
        if request.method=='POST':
            old_password=request.POST.get('old_password')
            pass1=request.POST.get('pass1')
            pass2=request.POST.get('pass2')
            if not user.check_password(old_password):
                messages.error(request,"Entered Old password is wrong!")
                return render (request,'userpassword.html')
            if pass1 != pass2:
                messages.error(request,"new password and confirm password not matching!")
                return render (request,'userpassword.html')
            user.set_password(pass1)
            user.save()
            messages.success(request,"Password changed succesfully!")
            return render (request,'userpassword.html')
        else:
            return render (request,'userpassword.html')
    else:
        return redirect('login')
            




# def forgot_password(request):
#      if request.method == 'POST':
#         email = request.POST['email']
#         user = CustomUser.objects.filter(email=email).first()
#         if user:
#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             send_reset_email(email, uid, token)
#             return render(request, 'password_reset_email_sent.html')
#      return render(request, 'forget_password.html')

# def reset_password(request, uidb64, token):
#     user_id = force_str(urlsafe_base64_decode(uidb64))
#     user = User.objects.filter(pk=user_id).first()
#     if user and default_token_generator.check_token(user, token):
#         if request.method == 'POST':
#             password = request.POST['password']
#             user.set_password(password)
#             user.save()
#             return render(request, 'password_reset_done.html')
#         return render(request, 'reset_password.html')
#     return render(request, 'password_reset_invalid.html')


# def send_reset_email(email, uid, token):
#     domain = get_current_site(request).domain
#     reset_link = f"http://{domain}{reverse('reset_password', kwargs={'uidb64': uid, 'token': token})}"
#     message = render_to_string('password_reset_email.html', {'reset_link': reset_link})
#     send_mail(
#         'Password Reset',
#         message,
#         'marvafathima62@gmail.com',
#         [email],
#         fail_silently=False,
#     )

