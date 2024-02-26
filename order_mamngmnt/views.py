from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from home .models import CustomUser,UserAddress,Cart,CartItem,Address
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from category.models import Products,ProductImage,ProductVar,Category,Subcategory,Color,Size
from django.db.models import Min
from django.db.models import F, Sum
from django.views.decorators.csrf import csrf_protect
from .models import Order,OrderAddress,OrderProduct
from django.db import transaction
from django.core.serializers.json import DjangoJSONEncoder
from coupons .models import Coupon
# Create your views here.
@login_required
def cart_to_order(request,cart_id):
    
    cart=Cart.objects.get(id=cart_id)
    cart_items=CartItem.objects.filter(cart=cart)
    us=request.user
    user=CustomUser.objects.get(id=us.id)
    address=Address.objects.get(user=us,is_default=True)
    cust_detail=UserAddress.objects.get(user=us)
    if cart.coupon_cart_total:
        coupon=Coupon.objects.get(id=cart.applied_coupon.id)
        coupon.usage_count +=1
        coupon.user_count +=1
        coupon.save()
    context={
        'cart':cart,
        'cart_items':cart_items,
        'address':address,
        'user':user,
        'cust_detail':cust_detail,
        'coupon':coupon
    }
    return render (request,'checkout.html',{'context':context})
def order_display(request):
    
    user=request.user
    cart=Cart.objects.get(user=user.id)
    items=CartItem.objects.filter(cart=cart)
    cart_user=CustomUser.objects.get(id=user.id)
    address=Address.objects.get(user=user,is_default=True)
    cust_detail=UserAddress.objects.get(user=user)
    order_address=OrderAddress.objects.create(
        user=user,
        house_name=address.house_name,
        street=address.street,
        city=address.city,
        district=address.district,
        landmark=address.landmark,
        state=address.state,
        postal_code=address.postal_code,
        country = address.country
    
    )
    

    order=Order.objects.create(user=user,address=order_address,order_total=cart.cart_total,total_qnty=cart.total_qnty)
    if cart.coupon_cart_total:
        coupon=Coupon.objects.get(id=cart.applied_coupon.id)
        order.discount_total=cart.coupon_price
        order.discount_grand_total=cart.coupon_cart_total
        order.applied_coupon=coupon.id
        order.save()
    
    for item in items:
        ox=OrderProduct.objects.create(
                    order=order,
                    product_variant=item.product_variant,
                    quantity=item.quantity,
                    price=item.product_variant.price,
                    
                )
        print(ox.item_total_price,"this is the total price of the vaariant")
        
        # ox.item_total_price=ox.quantity* ox.price


    od_items=OrderProduct.objects.filter(order=order)
    cart.delete()
    items.delete()
    if cart is None:
        print("order placed successfully")
    return render (request,'orderdisplay.html',{
        'order':order,
        'order_items':od_items,
        'address':order_address,
        'user':cart_user,
        'user_detail':cust_detail

    })
    # except:
    #     return HttpResponse("Error placing Order")
      
        # except:
        #     return render(request,'nohistory.html')

def order_item_display(request,order_id):
    order_items=OrderProduct.objects.filter(order=order_id)
    order_details = []
    for product in order_items:
        img=ProductImage.objects.get(img_id=product.product_variant.prod_id).first()
        order_details.append({
            'productImage': img,
            'productName': product.product_variant.prod_id.pr_name,
            'quantity': product.quantity,
            'individualPrice': product.product_variant.price,
            'totalPrice': product.item_total_price,
            'size': product.product_variant.size,
            'color': product.product_variant.color,
        })
        print(product.item_total_price,"checking the value being fetdched")
    
    return JsonResponse(order_details, safe=False)
def order_history(request):
    user = request.user
    
    orders = Order.objects.filter(user=user).order_by('created_at')  
    if not orders.exists():
        return render(request,'nohistory.html')
    else:
        addresses = []
        order_data=[]
        for order in orders:
            order_items=OrderProduct.objects.filter(order=order)
            order_details = []
            print(order.id,"this are my ordersssss")
            
        
            for product in order_items:
                img=ProductImage.objects.filter(img_id=product.product_variant.prod_id).first()
                order_details.append({
                    'image': img,
                    'pr_name': product.product_variant.prod_id.pr_name,
                    'quantity': product.quantity,
                    'price': product.product_variant.price,
                    'totalPrice': product.item_total_price,
                    'size': product.product_variant.size,
                    'color': product.product_variant.color,
                })
                print(product.item_total_price,"history total price checking")
            order_data.append({
                'order':order,
                'items':order_details,
            })
        
            address = OrderAddress.objects.get(id=order.address.id)
            addresses.append(address)

        return render(request, 'order_history.html', {
            'order_data':order_data,
            'addresses':addresses
        })
  
def admin_orderlist(request):
    order_data=Order.objects.select_related('user','address').prefetch_related('orderproduct__product_variant','user__useraddress').all()
    
    for order in order_data:
    
        print(order.user.email,"useremail")
        
        for pr in order.orderproduct.all():
            print(pr.product_variant.prod_id.pr_name)
            print(pr.product_variant.price,"unit price")
            print(pr.item_total_price)
        for us in order.user.useraddress.all():
            print(us.user_name) 
    return render (request,'orderlist.html',{'orders':order_data,'status_choices': Order.STATUS})
@require_POST   
def update_status(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS):
        order.status = new_status
        order.save()
    return redirect('admin_orderlist')

def get_order_products(request,order_id):
    print("get_order_products called")
    orders=Order.objects.get(pk=order_id)
    user=orders.user
    customer=CustomUser.objects.get(id=user.id)
    customer_detail=UserAddress.objects.get(user=user.id)
    print(customer.email)
    order_products = OrderProduct.objects.filter(order=order_id)
    # Construct a list of dictionaries containing order product data
    order_product_data = []
    for order_product in order_products:
        imgs=ProductImage.objects.filter(img_id=order_product.product_variant.prod_id).first()
        img=imgs.image.url
        order_product_data.append({
            'product_name': order_product.product_variant.prod_id.pr_name,
            'quantity': order_product.quantity,
            'total_price': order_product.item_total_price,
            'individual_price': order_product.price,
            'image_url': img,  # Assuming 'image' is a field in your ProductVariant model
            'color': order_product.product_variant.color.color,
            'size': order_product.product_variant.size.size,
            
            # Add more fields as needed
        })

        print(order_product.price)
    return render (request, 'order_iem_detail.html',{'order_products': order_product_data,'orders':orders,'customer':customer,'customer_detail':customer_detail})

    

