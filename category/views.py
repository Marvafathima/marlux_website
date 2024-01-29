from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from .models import Category,Subcategory,Products,ProductVarient,Brand
# Create your views here.
def add_category(request):
    if request.method=='POST':
        if request.user.is_superuser:
            cat_name=request.POST.get('cat_name')
            cat_des=request.POST.get('description')
            cat_img=request.FILES.get('image')
            is_published=request.POST.get('is_published')=='True'

            category=Category.objects.create(name=cat_name,cat_dsc=cat_des,cat_img=cat_img,published=is_published)
        else:
            messages.error(request,"access denied")
            return render(request,'adminapp/index.html')
    
    return render(request,'add_category.html')