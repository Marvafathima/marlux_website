from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from .models import Category,Subcategory,ProductVar, Color, Size,ProductImage
from .forms import SubcategoryForm,ProductsForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
# Create your views here.
@login_required(login_url="adminapp:admin")
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
@login_required(login_url="adminapp:admin")
def category_list(request):
    context={'category_list':Category.objects.all()}
    return render(request,'cat_list.html',context)
@login_required(login_url="adminapp:admin")
def del_category(request,id):
    cat=Category.objects.get(id=id)
    cat.delete()
    return redirect('adminapp:category_list')
@login_required(login_url="adminapp:admin")
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
@login_required(login_url="adminapp:admin")
def add_subcategory(request):
    if request.method == "POST":
        form = SubcategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subcategory added successfully.')  # Add a success message
            return redirect('adminapp:category_list')
        else:
            messages.error(request, 'Form validation failed. Please check the entered data.')
            # You might want to handle form validation errors here
    else:
        form = SubcategoryForm()

    return render(request, 'addsubcat.html', {'forms': form})
# def delete_subcategory(request, subcategory_id):
#     subcategory = get_object_or_404(Subcategory, pk=subcategory_id)

#     if request.method == "POST":
#         subcategory.delete()
#         messages.success(request, 'Subcategory deleted successfully.')
#         return redirect('adminapp:category_list')

    return render(request, 'delete_subcategory.html', {'subcategory': subcategory})
@transaction.atomic
def add_product(request):
    if request.method == 'POST':
        product_form = ProductsForm(request.POST)
        variant_count = int(request.POST.get('variant_count', 0))
        img1=request.FILES.get('image1')
        if 'image2' in request.FILES:
            img2=request.FILES.get('image2')
        else:
            img2=None
        if 'image3'in request.FILES:
            img3=request.FILES.get('image3')
        else:
            img3=None
        print(variant_count)
        if product_form.is_valid():
            product_instance = product_form.save()
            image=ProductImage.objects.create(img_id=product_instance,image=img1)
            if img2:
                ProductImage.objects.create(img_id=product_instance,image=img2)
            if img3:
                ProductImage.objects.create(img_id=product_instance,image=img3)
            for i in range(1, variant_count + 1):
                color = request.POST.get(f'color_{i}')
                size = request.POST.get(f'size_{i}')
                stock = request.POST.get(f'stock_{i}')
                price = request.POST.get(f'price_{i}')
                discount=request.POST.get(f'discount_{i}')

                print(color,size,stock,price,discount)

                color_instance, _ = Color.objects.get_or_create(color=color)
                size_instance, _ = Size.objects.get_or_create(size=size)

                ProductVar.objects.create(
                    prod_id=product_instance,
                    color=color_instance,
                    size=size_instance,
                    stock=stock,
                    price=price,
                    discount=discount
                )
            
            return redirect('adminapp:category_list')
        else:
           messages.error(request,"invalid form")
           return render(request,"add_product.html")
    else:
        product_form = ProductsForm()

    return render(request, 'add_product.html', {'product_form': product_form})
    

    


    