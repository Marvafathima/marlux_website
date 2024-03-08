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
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
# from django.template.loader import render_to_string
# # from weasyprint.html import HTML
# @method_decorator(never_cache, name='dispatch')
# class CheckoutView(TemplateView):
#     template_name = 'checkout.html'

# Create your views here.
@login_required
def cart_to_order(request,cart_id):
    try:
        cart=Cart.objects.get(id=cart_id)
        cart_items=CartItem.objects.filter(cart=cart)
    except:
        return redirect('home')
    us=request.user
    user=CustomUser.objects.get(id=us.id)
    try:
        address=Address.objects.get(user=us,is_default=True)
        cust_detail=UserAddress.objects.get(user=us)
    except:
        messages.error(request,"please add address and other details before checking out!")
        return redirect('cart')
    if cart.applied_coupon:
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
    else:
        context={
            'cart':cart,
            'cart_items':cart_items,
            'address':address,
            'user':user,
            'cust_detail':cust_detail,
        }

    return render (request,'checkout.html',{'context':context})


def retry_payment_checkout(request,id):
    user=request.user
    user=CustomUser.objects.get(id=user.id)
    order=Order.objects.get(id=id)
    order_items=OrderProduct.objects.filter(order=order)
    address=OrderAddress.objects.get(id=order.address.id)
    cust_detail=UserAddress.objects.get(user=user)
    print(address)
    if order.applied_coupon:
        coupon=Coupon.objects.get(id=order.applied_coupon.id)
        coupon.usage_count +=1
        coupon.user_count +=1
        coupon.save()
        context={
                'order':order,
                'cart_items':order_items,
                'address':address,
                'user':user,
                'cust_detail':cust_detail,
                'coupon':coupon

        }
        return render(request,"checkout.html",{'context':context})
    else:
        context={
                'order':order,
                'cart_items':order_items,
                'address':address,
                'user':user,
                'cust_detail':cust_detail,

        }

        return render(request,"checkout.html",{'context':context})
def order_history(request):
    user = request.user
    
    orders = Order.objects.filter(Q(payment_status="cod")| Q(payment_status="successful"),user=user).order_by('created_at') 
    if not orders.exists():
        return render(request,'nohistory.html')
    else:
        addresses = []
        order_data=[]
        for order in orders:
            order_items=OrderProduct.objects.filter(order=order)
            order_details = []
            
        
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
                
            order_data.append({
                'order':order,
                'items':order_details,
            })
        
            address = OrderAddress.objects.get(id=order.address.id)
            addresses.append(address)
#  return render(request, 'order_history.html', {
        return render(request, 'notika.html', {
            'order_data':order_data,
            'addresses':addresses
        })
    

def failed_order_history(request):
    user=request.user
    order=Order.objects.filter(Q(payment_status="failed") & Q(user=user))
    for orders in order:
        print(orders.id,orders.tracking_number)
        
    return render (request,'failed_order.html',{'order_data':order})



def admin_orderlist(request):
    order_data=Order.objects.select_related('user','address').prefetch_related('orderproduct__product_variant','user__useraddress').all()    
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

       
    return render (request, 'order_iem_detail.html',{'order_products': order_product_data,'orders':orders,'customer':customer,'customer_detail':customer_detail})

    

@login_required
def my_orders(request,order_id):
    user=request.user
    orders=Order.objects.get(id=order_id)
    print(orders.tracking_number)
    order_items=OrderProduct.objects.filter(order=orders.id)
    if orders.status=="Confirmed":
        confirm=orders.status
        return render(request,'orderdisplay.html',{'order':orders,'order_items':order_items,'confirm':confirm})
    elif orders.status=="Pending":
        pending=orders.status
        return render(request,'orderdisplay.html',{'order':orders,'order_items':order_items,'pending':pending})
    elif orders.status=="Shipped":
        shipped=orders.status
        return render(request,'orderdisplay.html',{'order':orders,'order_items':order_items,'shipped':shipped})
    elif orders.status=="Delivered":
        delivered=orders.status
        return render(request,'orderdisplay.html',{'order':orders,'order_items':order_items,'delivered':delivered})
    print(orders.status)
    
    return render(request,'orderdisplay.html',{'order':orders,'order_items':order_items})