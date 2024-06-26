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
from django.urls import reverse
from wallet .models import Wallet,Transaction
from decimal import Decimal
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
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
    
    orders = Order.objects.filter(Q(payment_status="cod")| Q(payment_status="successful") | Q(payment_status="refunded")| Q(payment_status="wallet") ,user=user).order_by('created_at') 
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
    order=Order.objects.filter(Q(payment_status="failed") & Q(user=user)).exclude(status="Cancelled")
   
    if order:   
        return render (request,'failed_order.html',{'order_data':order})
    else:
        return render (request,'empty_failed_order_history.html')


@staff_member_required 
def admin_orderlist(request):
    order_data=Order.objects.select_related('user','address').prefetch_related('orderproduct__product_variant','user__useraddress').order_by('-created_at').all()
   
   
    status = list(Order.STATUS)  # Get the original status choices
    
    delivered_status_choices = []
    shipped_status_choices = []
    confirm_status_choices = []
    pending_status_choices = []
    return_status_choices = []
    cancel_status_choices = []
    

    # Modify status choices based on the current status
    for order in order_data:
        
        if order.status == 'Delivered':
            delivered_status_choices = [choice for choice in status if choice[0] == 'Delivered' or choice[0] == 'Return']
           
        
        elif order.status == 'Shipped':
            shipped_status_choices = [choice for choice in status if choice[0] in ['Shipped', 'Delivered', 'Cancelled', 'Return']]
            
        elif order.status == 'Confirmed':
            confirm_status_choices = [choice for choice in status if choice[0] not in ['Pending']]
           
        elif order.status == 'Pending':
            pending_status_choices = [choice for choice in status ]
           
        elif order.status == 'Return':
            return_status_choices = [choice for choice in status if choice[0] == 'Return']
           
        elif order.status == 'Cancelled':
            cancel_status_choices = [choice for choice in status if choice[0] == 'Cancelled']
            
   
    return render (request,'orderlist.html',{'orders':order_data,
                                             'delivered_status_choices':delivered_status_choices,
                                              'shipped_status_choices':shipped_status_choices,
                                               'confirm_status_choices':confirm_status_choices,
                                               'pending_status_choices':pending_status_choices,
                                               'return_status_choices':return_status_choices,
                                               'cancel_status_choices':cancel_status_choices,
                            
                                              })









@require_POST  
@staff_member_required 
def update_status(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS):
        order.status = new_status
        order.save()
        if order.status=="Delivered":
            
            if order.payment_status=="cod":
               
                payment="successful"
                if payment in dict(Order.PAYMENT_STATUS_CHOICES):
                    order.payment_status=payment
                    
                    order.save() 
        if order.status=="Cancelled":
            if order.payment_status=="successful" or order.payment_status=="wallet":
           
                us=order.user.id
                user=CustomUser.objects.get(id=us)
            
                wallet,created=Wallet.objects.get_or_create(user=user)
                
                if order.applied_coupon:
                    wallet.balance +=Decimal(order.discount_grand_total)
                    wallet.save()
                    amount=order.discount_grand_total
                    transaction=Transaction.objects.create(wallet=wallet,amount=order.discount_grand_total,transaction_type="Refund")
                    print(transaction.id)
                else:
                    grand_total=Decimal(order.grand_total)
                    wallet.balance += grand_total
                    wallet.save()
                    amount=order.grand_total
                    transaction=Transaction.objects.create(wallet=wallet,amount=amount,transaction_type="Refund")
                    print(transaction.id)
                order.payment_status="refunded"
                order.save()
    return redirect('admin_orderlist')


def get_order_products(request,order_id):
    
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
    elif orders.status=="Cancelled":
        cancelled=orders.status
        return render(request,'orderdisplay.html',{'order':orders,'order_items':order_items,'cancelled':cancelled})
    elif orders.status=="Return":
        returned=orders.status
        return render(request,'orderdisplay.html',{'order':orders,'order_items':order_items,'return':returned})
    
    return render(request,'orderdisplay.html',{'order':orders,'order_items':order_items})



from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
import os
from InvoiceGenerator.api import Invoice,Item,Client,Provider,Creator
from InvoiceGenerator.pdf import SimpleInvoice
from django.http import FileResponse
from decimal import Decimal
def invoice_generator(request,id):
   
    os.environ["INVOICE_LANG"] ="en"

    order=Order.objects.get(id=id)
    user=CustomUser.objects.get(id=request.user.id)
    user_detail=UserAddress.objects.get(user=request.user)  
    products=OrderProduct.objects.filter(order=order)
    email=user.email
    address=OrderAddress.objects.get(id=order.address.id)
    address_string = f"{address.house_name}, {address.street}, {address.city}, {address.postal_code}, {address.district}, {address.state}, {address.country}"
    client = Client(user_detail.user_name, address_string)
    provider=Provider('Marlux',bank_account="64567-89078",bank_code='2021')
    creator=Creator('Marlux online fashion store')
    
    invoice = Invoice(client, provider, creator)
    for product in products:
        invoice.add_item(Item(product.quantity,product.price, description=product.product_variant.prod_id.pr_name))
    invoice.add_item(Item(1,order.tax,description="Tax"))
    invoice.add_item(Item(1,50,description="Delivery Charge"))
    discount=order.discount_amount * -1.00
    invoice.add_item(Item(1,discount,description="Discount"))

    invoice.currency = "Rs."
    if order.payment_mode=="razorpay":
        invoice.number = order.tracking_number
    else:
        invoice.number =order.payment_mode

    docu = SimpleInvoice(invoice)
    invoice_file_path = "invoice2.pdf"
    docu.gen(invoice_file_path, generate_qr_code=False) #you can put QR code by setting the #qr_code parameter to ‘True’
    # Open and serve the generated invoice file as a response
    with open(invoice_file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        return response
    #docu.gen("invoice.xml") ## We can also generate an XML file of this invoice

    




def cancel_order(request,order_id):
    order=Order.objects.get(id=order_id)
    status="Cancelled"
    if status in dict(Order.STATUS):
        order.status=status
        order.save()
        
        amount=0
    if order.payment_status=="successful":
        wallet,created=Wallet.objects.get_or_create(user=request.user)
         
        if order.applied_coupon:
            wallet.balance += order.discount_grand_total
            wallet.save()
            amount=order.discount_grand_total
            transaction=Transaction.objects.create(wallet=wallet,amount=order.discount_grand_total,transaction_type="Refund")
       
        else:
            wallet.balance += Decimal(order.grand_total)
            wallet.save()
            amount=order.grand_total
        transaction=Transaction.objects.create(wallet=wallet,amount=amount,transaction_type="Refund")
    
        
        tracking_num=order.tracking_number
        order.payment_status="refunded"
        order.save()

        # stock management for cancelled order

        order_items=OrderProduct.objects.filter(order=order)
        for items in order_items:
            product_var=items.product_variant
            print(product_var.stock,"stock before cancel")
            product_var.stock += items.quantity
            product_var.save()
            print(product_var.stock,"stock after cancel")

        messages.success(request,f"Your order {order.tracking_number} has been cancelled successfully!Your Wallet Credited with {transaction.amount}")

        return redirect('view_wallet')
    else:
        messages.success(request,f"Your order {order.tracking_number} has been cancelled successfully")

        return redirect(reverse('my_orders',args=[order.id]))
    


def return_order(request,order_id):
    order=Order.objects.get(id=order_id)
    status="Return"
    if status in dict(Order.STATUS):
        order.status=status
        order.save()
        amount=0
        if order.payment_status=="successful":
            wallet,created=Wallet.objects.get_or_create(user=request.user)
            
            if order.applied_coupon:
                wallet.balance +=order.discount_grand_total
                wallet.save()
                amount=order.discount_grand_total
                
        
            else:
                wallet.balance += Decimal(order.grand_total)
                wallet.save()
                amount=order.grand_total
            transaction=Transaction.objects.create(wallet=wallet,amount=amount,transaction_type="Refund")
        
            print(wallet.balance,transaction.amount,"this is your wallet balance")
            print(order.status)
        
        order.payment_status="refunded"
        order.save()

        # stock management for cancelled order

        order_items=OrderProduct.objects.filter(order=order)
        for items in order_items:
            product_var=items.product_variant
            print(product_var.stock,"stock before return")
            product_var.stock += items.quantity
            product_var.save()
            print(product_var.stock,"stock after return")
        print(order.status)
        messages.success(request,f"Return request succesfull! Our team will come to collect the order {order.tracking_number} soon!")
        return redirect('view_wallet')
    else:
        messages.success(request,f"Return request succesfull! Our team will come to collect the order {order.tracking_number} soon!")
        return redirect('order_history')
   
    # return redirect(reverse('my_orders', args=[order.id]))
