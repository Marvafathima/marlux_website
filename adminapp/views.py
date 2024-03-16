from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.http import JsonResponse,FileResponse,HttpResponse
import random
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from home.models import UserAddress ,CustomUser,Address
from order_mamngmnt .models import Order,OrderProduct
from datetime import datetime, timedelta
from django.db.models import Sum,Avg,F,Count
from coupons .models import Coupon
from decimal import Decimal
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table,TableStyle,SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from .utils  import months, colorPrimary, colorSuccess, colorDanger, generate_color_palette, get_year_dict
from django.contrib.admin.views.decorators import staff_member_required
from reportlab.lib.units import inch
from reportlab.lib import colors
from django.http import FileResponse
import io
from django.db.models.functions import ExtractYear, ExtractMonth
# Create your views here.
@ensure_csrf_cookie
def custom_admin(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        
        # Authenticate using email and password
        user = authenticate(request, email=email, password=password)

        if user is not None and user.is_superuser:
            # Log the user in
            login(request, user)
            return redirect('adminapp:dashboard')
        else:
            messages.info(request, "Invalid admin credentials")
            return redirect('adminapp:admin')

    return render(request, "adminside/index.html")
@login_required(login_url='adminapp:admin')         
def admin_dashboard(request):
    return render(request,"adminside/dashboard.html")
def admin_logout(request):
    
    logout(request)
    return redirect('adminapp:admin')
# # Create your views here.
def admin_userlist(request):
    user_data = CustomUser.objects.select_related('useraddress').values('id', 'email','is_active','useraddress__user_name','useraddress__phone_number')
    context = {'userlist':user_data}
    return render(request, "adminside/userlist.html", context)

def user_unblock(request,user_id):
    us=CustomUser.objects.filter(id=user_id).first()
    us.is_active=True
    us.save()
    return redirect('adminapp:userlist')
def user_block(request,user_id):
    us=CustomUser.objects.filter(id=user_id).first()
    print(us)
    us.is_active=False
    us.save()
    return redirect('adminapp:userlist')
def sales(request):
    if request.method=="POST":
        start_date=request.POST.get("start_date")
        end_date=request.POST.get("end_date")
        day=request.POST.get("day")
        print(type(end_date),"this is the date type")
        print(day)
        if day =="month" or day=="week" or day=="day":
            formatted_start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            formatted_end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            orders=Order.objects.filter(created_at__range=[formatted_start_date,formatted_end_date]).exclude(Q(status="Return")| Q(status="Cancelled")|Q(status="Pending") )
            total_orders=orders.count()
            if total_orders !=0:
                
                no_discount_sale=Order.objects.filter(created_at__range=[formatted_start_date,formatted_end_date],applied_coupon__isnull=True).exclude(Q(status="Return")| Q(status="Cancelled")|Q(status="Pending")).aggregate(nondiscount_sale=Sum('grand_total'))
                discount_sale=Order.objects.filter(created_at__range=[formatted_start_date,formatted_end_date],applied_coupon__isnull=False).exclude(Q(status="Return")| Q(status="Cancelled")|Q(status="Pending")).aggregate(discount_sale=Sum('discount_grand_total'))
                actual_sale_price=Order.objects.filter(created_at__range=[formatted_start_date,formatted_end_date],applied_coupon__isnull=False).exclude(Q(status="Return")| Q(status="Cancelled")|Q(status="Pending")).aggregate(sale=Sum('grand_total'))
                print(actual_sale_price,"this is actual sale price+++++++++++")
                try:
                    total_discount=Decimal(actual_sale_price['sale'])-discount_sale['discount_sale']
                    no_discount_grand_total=Decimal(actual_sale_price['sale'])+Decimal(no_discount_sale['nondiscount_sale'])
                    sales_grand_total=discount_sale['discount_sale'] + Decimal(no_discount_sale['nondiscount_sale'])
                except:
                    actual_sale_price=0
                    total_discount=0
                    no_discount_grand_total=Decimal(no_discount_sale['nondiscount_sale'])
                    sales_grand_total=no_discount_sale['nondiscount_sale']
                total_quantity=Order.objects.filter(created_at__range=[formatted_start_date,formatted_end_date]).aggregate(total_quantity=Sum('total_qnty'))
                print(no_discount_grand_total,"this is the grand total without discount+++++++++++")
                
                
                request.session['orders'] =str(list(orders.values()) ) # Convert QuerySet to list of dictionaries
                request.session['total_discount'] = str( total_discount) 
                request.session['total_orders']= str(total_orders) 
                request.session['no_discount_grand_total'] =  str(no_discount_grand_total) 
                request.session['sales_grand_total'] =  str(sales_grand_total) 
                request.session['total_quantity'] = str( total_quantity['total_quantity']) 
                request.session['start_date']=str(formatted_start_date)
                request.session['end_date']=str(formatted_end_date)
                request.session['day']=day
                print(request.session['no_discount_grand_total'],"this is the grand total without discount+++++++++++")
                
            
                
                return render (request,"salesview.html",{
                'orders':orders,
                'total_orders':total_orders,
                'total_items':total_quantity['total_quantity'],
                'grand_total':no_discount_grand_total,
                'coupon_total': total_discount,
                'discount_grand_total':sales_grand_total,
                'day':day,
                'start_date':start_date,
                'end_date':end_date  
                        })
            else:
                print(total_orders)
                total_orders=0
                total_quantity=0
                no_discount_grand_total=0.00
                total_discount=0.00
                sales_grand_total=0.00
                request.session['orders'] =str(list(orders.values()))  # Convert QuerySet to list of dictionaries
                request.session['total_discount'] = str(total_discount)
                request.session['total_orders']=str(total_orders)
                request.session['no_discount_grand_total'] = str(no_discount_grand_total)
                request.session['sales_grand_total'] = str(sales_grand_total)
                request.session['total_quantity'] = str(total_quantity)
                request.session['start_date']=str(formatted_start_date)
                request.session['end_date']=str(formatted_end_date)
                request.session['day']=day
                return render (request,"salesview.html",{
                    
                    'total_orders':total_orders,
                    'total_items':total_quantity,
                    'grand_total':no_discount_grand_total,
                    'coupon_total': total_discount,
                    'discount_grand_total':sales_grand_total,
                    'day':day,
                    'start_date':start_date,
                    'end_date':end_date   
                            })
        else:
              
            end_date = datetime.strptime(end_date, "%m/%d/%Y") if isinstance(end_date, str) else end_date
            start_date = datetime.strptime(start_date, "%m/%d/%Y") if isinstance(start_date, str) else start_date

            formatted_start_date = datetime.strptime(start_date, "%Y/%m/%d").date() if isinstance(start_date, str) else start_date

            

          
            formatted_end_date = datetime.strptime(end_date, "%Y/%m/%d").date() if isinstance(end_date, str) else end_date

            print(type(formatted_end_date),"this is the date type")
            print(type(formatted_start_date),"this is the date type")
            orders=Order.objects.filter(created_at__range=[formatted_start_date,formatted_end_date]).exclude(Q(status="Return")| Q(status="Cancelled")|Q(status="Pending") )
            total_orders=orders.count()
            if total_orders !=0:
                
                no_discount_sale=Order.objects.filter(created_at__range=[formatted_start_date,formatted_end_date],applied_coupon__isnull=True).exclude(Q(status="Return")| Q(status="Cancelled")|Q(status="Pending")).aggregate(nondiscount_sale=Sum('grand_total'))
                discount_sale=Order.objects.filter(created_at__range=[formatted_start_date,formatted_end_date],applied_coupon__isnull=False).exclude(Q(status="Return")| Q(status="Cancelled")|Q(status="Pending")).aggregate(discount_sale=Sum('discount_grand_total'))
                actual_sale_price=Order.objects.filter(created_at__range=[formatted_start_date,formatted_end_date],applied_coupon__isnull=False).exclude(Q(status="Return")| Q(status="Cancelled")|Q(status="Pending")).aggregate(sale=Sum('grand_total'))
                total_discount=Decimal(actual_sale_price['sale'])-discount_sale['discount_sale']
                no_discount_grand_total=Decimal(actual_sale_price['sale'])+Decimal(no_discount_sale['nondiscount_sale'])
                sales_grand_total=discount_sale['discount_sale']+ Decimal(no_discount_sale['nondiscount_sale'])
                total_quantity=Order.objects.filter(created_at__range=[start_date,end_date]).aggregate(total_quantity=Sum('total_qnty'))
                print(total_orders,no_discount_sale,"refund return included")
                no=Order.objects.filter(created_at__range=[formatted_start_date,formatted_end_date],applied_coupon__isnull=True).aggregate(nondiscount_sale=Sum('grand_total'))
                ord=Order.objects.filter(created_at__range=[formatted_start_date,formatted_end_date])
                total=ord.count()
                print(total,no,"refund return excluded")
                request.session['orders'] =str(list(orders.values())) # Convert QuerySet to list of dictionaries
                request.session['total_discount'] = str(total_discount)
                request.session['total_orders']=str(total_orders)
                request.session['no_discount_grand_total'] =str( no_discount_grand_total)
                request.session['sales_grand_total'] = str(sales_grand_total)
                request.session['total_quantity'] = str(total_quantity['total_quantity'])
                request.session['day']=day
                request.session['start_date']=str(formatted_start_date)
                request.session['end_date']=str(formatted_end_date)
                return render (request,"salesview.html",{
                    'orders':orders,
                'total_orders':total_orders,
                'total_items':total_quantity['total_quantity'],
                'grand_total':no_discount_grand_total,
                'coupon_total': total_discount,
                'discount_grand_total':sales_grand_total,
                'day':day,
                'start_date':start_date,
                'end_date':end_date  
                        })
            else:
                print(total_orders)
                total_orders=0
                total_quantity=0
                no_discount_grand_total=0.00
                total_discount=0.00
                sales_grand_total=0.00
                request.session['orders'] = str(list(orders.values()))  # Convert QuerySet to list of dictionaries
                request.session['total_discount'] = str(total_discount)
                request.session['no_discount_grand_total'] = str(no_discount_grand_total)
                request.session['sales_grand_total'] = str(sales_grand_total)
                request.session['total_orders']=str(total_orders )
                request.session['total_quantity'] = str(total_quantity)
                request.session['start_date']=str(formatted_start_date)
                request.session['end_date']=str(formatted_end_date)
                request.session['day']=day
                return render (request,"salesview.html",{
                    'total_orders':total_orders,
                    'total_items':total_quantity,
                    'grand_total':no_discount_grand_total,
                    'coupon_total': total_discount,
                    'discount_grand_total':sales_grand_total,
                    'day':day,
                    'start_date':start_date,
                    'end_date':end_date   
                            })
    else:

    
        start_date_month=datetime.now()-timedelta(days=30)
        start_date_week=datetime.now()-timedelta(days=7)
        end_date=datetime.now()
        orders=Order.objects.filter(created_at__range=[end_date,end_date]).exclude(Q(status="Return")| Q(status="Cancelled")|Q(status="Pending") )
        print(orders.count())
        
       
        print(start_date_month,"one month before")
        print(start_date_week,"one year before")
        end_date = datetime.now()
        print(end_date.strftime("%Y-%m-%d"),"todays date")
        
        return render(request,'sales.html',{
            'start_date_week':start_date_week.strftime("%Y-%m-%d"),
            'start_date_month':start_date_month.strftime("%Y-%m-%d"),
            'end_date':end_date.strftime("%Y-%m-%d")
        })
from reportlab.platypus import Paragraph
def download_pdf(request):
    buf=io.BytesIO()
    total_orders = request.session.get('total_orders','')
    total_discount=request.session.get('total_discount','')
    no_discount_grand_total =request.session.get('no_discount_grand_total','')
    sales_grand_total = request.session.get('sales_grand_total','')
    total_quantity= request.session.get('total_quantity','')  
    start_date=request.session.get('start_date')
    end_date=request.session.get('end_date')
    day=request.session.get('day')
    if day!="custom":
        date_format="%Y-%m-%d"
        start_date=datetime.strptime(start_date,date_format)
        end_date=datetime.strptime(end_date,date_format)
    else:
        start_date=datetime.strptime(start_date,"%Y-%m-%d %H:%M:%S")
        end_date=datetime.strptime(end_date,"%Y-%m-%d %H:%M:%S")
        start_date.strftime("%Y-%m-%d")
        end_date.strftime("%Y-%m-%d")
        print(end_date,start_date,type(end_date),type(start_date),"this is the date type")

    orders=Order.objects.filter(created_at__range=[start_date,end_date]).exclude(Q(status="Return")| Q(status="Cancelled")|Q(status="Pending"))
    print(orders.count(),"this is order set count")
   
    
   

    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    # Create heading with styling
    heading = "SALES REPORT"
    heading=Paragraph(heading,styles['Heading1'])
    elements.append(heading)
    
    # elements.append(Paragraph(heading,styles['Heading1']))  # Use pre-defined style for heading

    # Formatted date range string
    date_range = f"Start Date: {start_date.strftime('%Y-%m-%d')} - End Date: {end_date.strftime('%Y-%m-%d')}"
    elements.append(Paragraph(date_range, styles['Normal']))  # Use a normal style

    # Add horizontal line
   # Create a line object with spacing and thickness
  
    # Upper part of the PDF with statistics
    upper_part = [
        ["Total Orders:", total_orders],
        ["Total Quantity:", total_quantity],
        ["Total Discount:", total_discount],
        ["No Discount Grand Total:",no_discount_grand_total],
        ["Sales Grand Total:", sales_grand_total],

    ]

    # Create table for upper part

    upper_table = Table(upper_part,spaceBefore=4,spaceAfter=50)
    upper_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                     ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    elements.append(upper_table)

    # Table part with orders
    
    order_data = [["Order Id","Total units","Order Date", "Total Price", "Discount", "Grand Total"]]
    for order in orders:
        # order_data.append([order['tracking_number'],order['grand_total'], order['status'], order['user.email']])
        if order.applied_coupon:
            if order.applied_coupon.discount_amount:
                order_data.append([order.tracking_number,order.total_qnty,order.created_at,order.grand_total,"₹"+ str(order.applied_coupon.discount_amount),order.discount_grand_total])
            elif order.applied_coupon.discount_percentage:
                order_data.append([order.tracking_number,order.total_qnty,order.created_at,order.grand_total,str(order.applied_coupon.discount_percentage)+"%",order.discount_grand_total])
        else:
            order_data.append([order.tracking_number,order.total_qnty,order.created_at,order.grand_total,"-",order.grand_total])
       
    
    
    
    # Create table for order data
    order_table = Table(order_data)
    order_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                     ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                     ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                      ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                     ]))

    elements.append(order_table)

    # Build PDF
    doc.build(elements)
    buf.seek(0)
    
        
    del request.session['orders']
    del request.session['total_orders']
    del request.session['total_quantity']
    del request.session['total_discount']
    del request.session['no_discount_grand_total']
    del request.session['sales_grand_total']
    del request.session['start_date']
    del request.session['end_date']

    
    # Return the response
    return FileResponse(buf, as_attachment=True, filename='sales.pdf')

        
@staff_member_required
def get_filter_options(request):
    grouped_purchases = Order.objects.annotate(year=ExtractYear("created_at")).values("year").order_by("-year").distinct()
    options = [purchase["year"] for purchase in grouped_purchases]

    return JsonResponse({
        "options": options,
    })


@staff_member_required
def get_sales_chart(request, year):
    purchases = Order.objects.filter(created_at__year=year)
    grouped_purchases = purchases.annotate(price=F("grand_total")).annotate(month=ExtractMonth("created_at"))\
        .values("month").annotate(average=Sum("grand_total")).values("month", "average").order_by("month")

    sales_dict = get_year_dict()

    for group in grouped_purchases:
        sales_dict[months[group["month"]-1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"Sales in {year}",
        "data": {
            "labels": list(sales_dict.keys()),
            "datasets": [{
                "label": "Amount ($)",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(sales_dict.values()),
            }]
        },
    })


@staff_member_required
def spend_per_customer_chart(request, year):
    purchases = Order.objects.filter(created_at__year=year)
    grouped_purchases = purchases.annotate(price=F("grand_total")).annotate(month=ExtractMonth("created_at"))\
        .values("month").annotate(average=Avg("grand_total")).values("month", "average").order_by("month")

    spend_per_customer_dict = get_year_dict()

    for group in grouped_purchases:
        spend_per_customer_dict[months[group["month"]-1]] = round(group["average"], 2)

    return JsonResponse({
        "title": f"Spend per customer in {year}",
        "data": {
            "labels": list(spend_per_customer_dict.keys()),
            "datasets": [{
                "label": "Amount ($)",
                "backgroundColor": colorPrimary,
                "borderColor": colorPrimary,
                "data": list(spend_per_customer_dict.values()),
            }]
        },
    })
   
@staff_member_required
def sale_statistics(request):
    return render(request,'sale_chart.html')


 