from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
# from .models import Profiles,User
import random
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from home.models import UserAddress ,CustomUser,Address
from order_mamngmnt .models import Order,OrderProduct
from datetime import datetime, timedelta
from django.db.models import Sum
from coupons .models import Coupon
from decimal import Decimal
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table,TableStyle,SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.units import inch
from reportlab.lib import colors
from django.http import FileResponse
import io
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
                total_discount=Decimal(actual_sale_price['sale'])-discount_sale['discount_sale']
                no_discount_grand_total=Decimal(actual_sale_price['sale'])+Decimal(no_discount_sale['nondiscount_sale'])
                sales_grand_total=discount_sale['discount_sale']+ Decimal(no_discount_sale['nondiscount_sale'])
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

def download_pdf(request):
    buf=io.BytesIO()
    total_orders = request.session.get('total_orders','')
    total_discount=request.session.get('total_discount','')
    no_discount_grand_total =request.session.get('no_discount_grand_total','')
    sales_grand_total = request.session.get('sales_grand_total','')
    total_quantity= request.session.get('total_quantity','')  
    start_date=request.session.get('start_date')
    end_date=request.session.get('end_date')
    print(end_date,start_date,type(end_date),type(start_date),"thsi is the date type")

    date_format="%Y-%m-%d"
    start_date=datetime.strptime(start_date,date_format)
    end_date=datetime.strptime(end_date,date_format)
    print(end_date,start_date,type(end_date),type(start_date),"thsi is the date type")

    orders=Order.objects.filter(created_at__range=[start_date,end_date]).exclude(Q(status="Return")| Q(status="Cancelled")|Q(status="Pending"))
    print(orders.count(),"this is order set count")
   
    
    # orders = list(orders_str)  # Parse the string back to a list of dictionaries
    # except json.JSONDecodeError:
    # Handle the case where the JSON string is not properly formatted
        # orders = []

    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Upper part of the PDF with statistics
    upper_part = [
        ["Total Orders:", total_orders],
        ["Total Quantity:", total_quantity],
        ["Total Discount:", total_discount],
        ["No Discount Grand Total:",no_discount_grand_total],
        ["Sales Grand Total:", sales_grand_total],

    ]

    # Create table for upper part
    upper_table = Table(upper_part)
    upper_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                     ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                     ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                     ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                     ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

    elements.append(upper_table)

    # Table part with orders
    order_data = [["Tracking Number", "Grand Total", "Status", "User Email"]]
    for order in orders:
        # order_data.append([order['tracking_number'],order['grand_total'], order['status'], order['user.email']])
    
        order_data.append([order.tracking_number,order.grand_total,order.status,order.user.email])
    # Create table for order data
    order_table = Table(order_data)
    order_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                     ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

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

        
# def download_pdf(request):
   
#     buf=io.BytesIO()
#     c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
#     textob=c.beginText()
#     textob.setTextOrigin(inch,inch)
#     textob.setFont("Helvetica",14)
  
#     start_date_month=datetime.now()-timedelta(days=30)
#     start_date_week=datetime.now()-timedelta(days=7)
#     end_date=datetime.now()
#     orders=Order.objects.filter(created_at__range=[start_date_month,end_date]).exclude(Q(status="Return")| Q(status="Cancelled")|Q(status="Pending") )
#     print(orders.count())
#     lines=[]
#     for order in orders:
        
#         lines.append(str(order.tracking_number))
#         lines.append(str(order.grand_total))
#         lines.append(str(order.status))
#         lines.append(str(order.user.email))
#         lines.append("")

#     max_lines_per_page = 40
#     current_line = 0
#     for line in lines:
#         textob.textLine(line)
#         current_line += 1
#         if current_line >= max_lines_per_page:
#             c.drawText(textob)
#             c.showPage()
            
#             buf.seek(0)
#             textob = c.beginText()
#             textob.setTextOrigin(inch, inch)
#             textob.setFont("Helvetica", 14)
#             current_line = 0 
#     if current_line > 0:
#         c.drawText(textob)

#     c.showPage()
#     c.save()
#     buf.seek(0)
#     return FileResponse(buf,as_attachment=True,filename='sales.pdf')
   
   


 