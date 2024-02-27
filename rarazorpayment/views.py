from django.shortcuts import render
from http.client import HTTPResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from order_mamngmnt .models import Order,OrderAddress,OrderProduct
from django.utils import timezone
from django.conf import settings
from home .models import CustomUser,UserAddress,Cart,CartItem,Address
import razorpay
from django.conf import settings
# Create your views here.


def payment_view(request):
    if request.method=="POST":
        amount=request.POST.get('amount')
        orderid=request.POST.get('orderid')
        username=request.POST.get('user_name')
        phone_number=request.POST.get('phone_number')
        currency='INR'
        data={
        'amount':amount*100,
        'currency':currency,
        'payment_capture':'1',
        'reciept':orderid
    }
        client=razorpay.Client(auth=('rzp_test_ZCCSyrCe5ZqrEH','0jXHYc59iwAKVWDMphgnXlh'))
        response_payment=client.order.create(data=data)
        print(response_payment)
        return render(request,'paysample.html')
    else:
        cart=Cart.objects.get(user=request.user,is_ordered=False)
        user_detail=UserAddress.objects.get(user=request.user)
        address=Address.objects.get(user=request.user,is_default=True)
        user_name=user_detail.user_name
        phone_number=user_detail.phone_number
        order_amount=cart.coupon_cart_total
        notes={
        'house_name':address.house_name,
        'street:order':address.street,
        'city:order':address.city,
        ' district':address.district,
        'landmark':address.landmark,
        'state':address.state,
        'postal_code':address.postal_code,
        'country ':address.country
        }
        # currency='INR'
        # data={
        #     'amount':order_amount*100,
        #     'currency':currency,
        #     'payment_capture':'1',
        #     'notes':notes,
        #     'reciept':cart.id
        # }
        # order_receipt =cart.id
        # client=razorpay.Client(auth=('rzp_test_ZCCSyrCe5ZqrEH','0jXHYc59iwAKVWDMphgnXlh'))
        # response_payment=client.order.create(data=data)
        # print(response_payment)
        context={
            'amount':order_amount,
            'order':cart,
            'orderId':cart.id,
            'user_name':user_name,
            'phone_number':phone_number
        }
        return render(request,'paysample.html',context)




#     order_id=initiate_payment(notes,order_receipt,order_amount)
#     cart.razorpay_order_id =order_id["id"]
#     cart.save()
#     context={
#         'order_id':order_id,
#         'amount':order_amount,
#         'order':cart,
#         'orderId':cart.id,
#         'user_name':user_name,
#         'phone_number':phone_number
#     }
#     return render(request,'checkout.html',context)
# client=razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_SECRET))
# def initiate_payment(notes,order_receipt,amount,currency='INR'):
#     data={
#         'amount':amount*100,
#         'currency':currency,
#         'payment_capture':'1',
#         'notes':notes,
#         'reciept':order_receipt
#     }
#     response=client.order.create(data=data)
#     return response['id']
# def payment_success_view(request):
#    order_id = request.POST.get('order_id')
#    payment_id = request.POST.get('razorpay_payment_id')
#    signature = request.POST.get('razorpay_signature')
#    params_dict = {
    #    'razorpay_order_id': order_id,
    #    'razorpay_payment_id': payment_id,
    #    'razorpay_signature': signature
#    }
  # try:
       #client.utility.verify_payment_signature(params_dict)
       # Payment signature verification successful
       # Perform any required actions (e.g., update the order status)
       #return render(request, 'payment_success.html')
  # except razorpay.errors.SignatureVerificationError as e:
       # Payment signature verification failed
       # Handle the error accordingly
       #return render(request, 'payment_failure.html')

    # except Order.DoesNotExist:
    #         print("Order not found")
    #         return HTTPResponse("404 Error")

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_success_view(request):
    if request.method=="POST":
        amount=request.POST.get('amount')
        orderid=request.POST.get('orderid')
        username=request.POST.get('user_name')
        phone_number=request.POST.get('phone_number')
        currency='INR'
        data={
        'amount':amount*100,
        'currency':currency,
        'payment_capture':'1',
        'reciept':orderid
    }
        client=razorpay.Client(auth=('rzp_test_ZCCSyrCe5ZqrEH','0jXHYc59iwAKVWDMphgnXlh'))
        response_payment=client.order.create(data=data)
        print(response_payment)
        # return render(request,'paysample.html')

    cart=Cart.objects.get(user=request.user,is_ordered=False)
    user_detail=UserAddress.objects.get(user=request.user)
    address=Address.objects.get(user=request.user,is_default=True)
    user_name=user_detail.user_name
    phone_number=user_detail.phone_number
    order_amount=cart.coupon_cart_total
    notes={
    'house_name':address.house_name,
    'street:order':address.street,
    'city:order':address.city,
    ' district':address.district,
    'landmark':address.landmark,
    'state':address.state,
    'postal_code':address.postal_code,
    'country ':address.country
    }
        # currency='INR'
        # data={
        #     'amount':order_amount*100,
        #     'currency':currency,
        #     'payment_capture':'1',
        #     'notes':notes,
        #     'reciept':cart.id
        # }
        # order_receipt =cart.id
        # client=razorpay.Client(auth=('rzp_test_ZCCSyrCe5ZqrEH','0jXHYc59iwAKVWDMphgnXlh'))
        # response_payment=client.order.create(data=data)
        # print(response_payment)
    context={
        'amount':order_amount,
        'order':cart,
        'orderId':cart.id,
        'user_name':user_name,
        'phone_number':phone_number
    }
    return render(request,'paysample.html',context)
   
#    order_id = request.POST.get('order_id')
#    payment_id = request.POST.get('razorpay_payment_id')
#    signature = request.POST.get('razorpay_signature')
#    params_dict = {
#        'razorpay_order_id': order_id,
#        'razorpay_payment_id': payment_id,
#        'razorpay_signature': signature
#    }
#    try:
#        client.utility.verify_payment_signature(params_dict)
       # Payment signature verification successful
       # Perform any required actions (e.g., update the order status)
#        return render(request, 'payment_success.html')
#    except razorpay.errors.SignatureVerificationError as e:
       # Payment signature verification failed
       # Handle the error accordingly
    #    return render(request, 'payment_failure.html')



# def payment(request):
#     try:
#         order = Order.objects.get(user=request.user, ordered=False)
#         address = CheckoutAddress.objects.get(user=request.user)
#         order_amount = order.get_total_price()
#         order_currency = "INR"
#         order_receipt = order.order_id
#         notes = {
#             "street_address" : address.street_address,
#             "apartment_address" : address.apartment_address,
#             "country" : address.country.name,
#             "zip" : address.zip_code,
#             }
#         razorpay_order = razorpay_client.order.create(dict(
#              amount=order_amount *100,
#              currency=order_currency,
#              receipt=order_receipt,
#              notes=notes,
#              payment_capture="0"
#         ))

#         print(razorpay_order["id"])
#         order.razorpay_order_id = razorpay_order["id"]
#         order.save()
        
#         print("It should render the summary page")
#         return render(request, "core/paymentsummaryrazorpay.html",
#             {
#                 "order" : order,
#                 "order_id" : razorpay_order["id"],
#                 "orderId" : order.order_id,
#                 "final_price" : order_amount,
#                 "razorpay_merchant_id" : settings.RAZORPAY_ID,
#             },
#         )
#     except Order.DoesNotExist:
#             print("Order not found")
#             return HTTPResponse("404 Error")

# #Adding payment gateway
# import razorpay
# from django.conf import settings
# # authorize razorpay client with API Keys.
# razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_ID, settings.RAZORPAY_SECRET))
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def handlerequest(request):
#     # this handle request only for taking data from the razorpay dashboard.
#     if request.method == "POST":
#         try:
#             order_id = request.POST.get("razorpay_order_id", "")
#             payment_id = request.POST.get("razorpay_payment_id", "")
#             signature = request.POST.get("razorpay_signature", "")
#             print(payment_id, order_id, signature)
#             params_dict = {
#                 "razorpay_order_id" : order_id,
#                 "razorpay_payment_id" : payment_id,
#                 "razorpay_signature" : signature,
#             }
            
#             try:
#                 order_db = Order.objects.get(razorpay_order_id=order_id)
#                 print("Order found")
#             except:
#                 print("Order not found")
#                 return HTTPResponse("505 Not found")
                
#             order_db.razorpay_payment_id = payment_id
#             order_db.razorpay_signature = signature
#             order_db.save()
#             print("Working.........")
#             result = razorpay_client.utility.verify_payment_signature(params_dict)
#             if result != None:
#                 print("Working final fine...........")
#                 amount = order_db.get_total_price()
#                 amount = amount * 100 #we have to pass in paise.
#                 payment_status = razorpay_client.payment.capture(payment_id, amount)
#                 if payment_status is not None:
#                     print(payment_status)
#                     order_db.ordered = True
#                     order_db.save()
#                     print("Payment success")
#                     request.session[
#                         "order_complete"
#                     ]= "Your order is successfully placed, you will receive your order within 5 working days"
#                     return render(request, "core/invo/invoice.html")
#                 else:
#                     print("Payment failed")
#                     order_db.ordered = False
#                     order_db.save()
#                     request.session[
#                         "order_failed"
#                     ]= "Unfortunately your order could not be placed, try again!"
#                     return redirect("/")
#             else:
#                 order_db.ordered = False
#                 order_db.save()
#                 return render(request, "core/paymentfailed.html")
#         except:
#             return HTTPResponse("Error occured")