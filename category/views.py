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
            messages.success(request,"category added successfully")
            return redirect('adminapp:category_list')
        else:
            messages.error(request,"access denied")
            return render(request,'adminapp/index.html')
    
    return render(request,'add_category.html')
def category_list(request):
    context={'category_list':Category.objects.all()}
    return render(request,'cat_list.html',context)
def del_category(request,id):
    cat=Category.objects.get(id=id)
    cat.delete()
    return redirect('adminapp:category_list')
def update_category(request,id):
    cat=Category.objects.get(pk=id)
    if request.method=="POST":
        cat_name=request.POST.get('cat_name')
        cat_dsc=request.POST.get('description')
        cat_img=request.FILES.get('image')
        is_published=request.POST.get('is_published')=='True'
        if cat_name:
            cat.name=cat_name
        if cat_dsc:
            cat.cat_dsc=cat_dsc
        if is_published :
            cat.published=is_published
        if cat_img:
            cat.cat_img=cat_img
        cat.save()
        return redirect('adminapp:category_list')
    context={'id':cat.pk,'cat_name':cat.name,'description':cat.cat_dsc,'image':cat.cat_img,'is_published':cat.published}
    return render(request,'cat_update.html',context)


