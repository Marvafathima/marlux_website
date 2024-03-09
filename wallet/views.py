from django.shortcuts import render
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
from django.db import transaction
from django.core.serializers.json import DjangoJSONEncoder
from coupons .models import Coupon
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView
from order_mamngmnt .models import Order,OrderProduct,OrderAddress
from .models import Wallet,Transaction
from django.core.paginator import Paginator
# Create your views here.

def view_wallet(request):
    user=request.user
    try:
        wallet=Wallet.objects.get(user=user)
        print(wallet.balance)
        transaction=Transaction.objects.filter(wallet=wallet)

        paginator = Paginator(transaction, 5)
        page_number = request.GET.get('page')
        transactions = paginator.get_page(page_number)

        return render(request,"wallet.html",{'wallet':wallet,'transaction':transactions})
    except:
        return render(request,"wallet.html")
