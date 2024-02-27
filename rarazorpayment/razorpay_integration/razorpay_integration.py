import razorpay
from django.conf import settings

client=razorpay.Client(auth=(settings.RAZORPAY_ID,settings.RAZORPAY_SECRET))
def initiate_payment(notes,order_reciept,amount,currency='INR'):
    data={
        'amount':amount*100,
        'currency':currency,
        'payment_capture':'1',
        'notes':notes,
        'reciept':order_reciept
    }
    response=client.order.create(data=data)
    return response['id']