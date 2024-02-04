from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from .models import Category,Subcategory,Products,ProductVar,Brand, Color, Size,ProductImage
from .forms import SubcategoryForm,ProductsForm,UpdateProductForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
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
                discount = request.POST.get(f'discount_{i}', None)


                print(color,size,stock,price,discount)

                color_instance, _ = Color.objects.get_or_create(color=color)
                size_instance, _ = Size.objects.get_or_create(size=size)
                if discount:
                    ProductVar.objects.create(
                        prod_id=product_instance,
                        color=color_instance,
                        size=size_instance,
                        stock=stock,
                        price=price,
                        discount=discount
                    )
                else:
                    ProductVar.objects.create(
                        prod_id=product_instance,
                        color=color_instance,
                        size=size_instance,
                        stock=stock,
                        price=price
                    )
            
            return redirect('adminapp:list_product')
        else:
           messages.error(request,"invalid form")
           return render(request,"add_product.html")
    else:
        product_form = ProductsForm()

    return render(request, 'add_product.html', {'product_form': product_form})
    
def list_product(request):
    products=Products.objects.all()
    return render (request,'product_list.html',{'products':products})

def update_product(request,id):
    product=Products.objects.get(id=id)
    image_ids=list(ProductImage.objects.filter(img_id=id).values_list('id', flat=True))
    if request.method=="POST":
        pr_name=request.POST.get('name')
        category=request.POST.get('category')
        brand=request.POST.get('brand')
        sub_category=request.POST.get('sub_category')
        is_available=request.POST.get('is_available',False)

        print(pr_name)
        print(category)
        print(brand)
        print(sub_category)
        print(is_available)
    
              #working code
        image1=request.FILES.get('image1')
        print(image1)
         #end of working code
        


        if 'image2' in request.FILES:
            image2=request.FILES.get('image2')
            
        
        else:
            image2=None  
        if 'image3' in request.FILES:
            image3=request.FILES.get('image3')
        else:
            image3=None
        print(image2)
        print(image3)
        if pr_name:
            product.pr_name=pr_name
            print('yes')
        else:
            print('no')
        if category:
            product.cat_id=category
            print('yes')
        else:
            print('no')
        if brand:
            product.brand_id=brand
            print('yes')
        else:
            print('no')
        if sub_category:
            product.subcat_id=sub_category 
        if is_available:
            product.is_available=is_available 
            print('yes')
        else:
            print('no')  
        product.save()
       
        if  image1 and image_ids:
            first_image_id = image_ids[0]
            print(image_ids)
            obj=ProductImage.objects.get(id=first_image_id)
            obj.image.delete(False)
            obj.image=image1
            obj.save()
       
        if image2 and len(image_ids) > 1:
            second_image_id = image_ids[1]
            obj= ProductImage.objects.get(id=second_image_id)
            obj.image.delete(False)
            obj.image=image2
            obj.save()
        elif image2 and len(image_ids)== 1:
            ProductImage.objects.create(img_id=product,image=image2)
            
        else:
            image2=None

    # Update image3 for the last image_id
        if image3 and len(image_ids) > 2:
            last_image_id = image_ids[-1]
            obj=ProductImage.objects.get(id=last_image_id)
            obj.image.delete(False)
            obj.image=image3
            obj.save()
        elif image3 and len(image_ids) <= 2:
            ProductImage.objects.create(img_id=product,image=image3)
        else:
            image3=None
        print(image1,image2,image3)
        return redirect('adminapp:list_product')
    
    else:

        categories = Category.objects.all()
        brands = Brand.objects.all()
        subcategories = Subcategory.objects.all()
        first_image_id=image_ids[0]
        image1=ProductImage.objects.get(id=first_image_id) 
        if len(image_ids)==2:
            second=image_ids[1] 
            image2=ProductImage.objects.get(id=second) 
        else:
            image2=None
        if len(image_ids)==3:
            second=image_ids[1] 
            image2=ProductImage.objects.get(id=second)
            third=image_ids[2] 
            image3=ProductImage.objects.get(id=third)
        else:
            image2=None
            image3=None

# Access individual images if needed
        print(image1)
        print(image2)
        print(image3)
        context = {
            'id':product.id,
            'pr_name':product.pr_name,
            # 'cat_id':product.cat_id.id if product.cat_id else None,
            # 'subcat_id':product.subcat_id.id if product.subcat_id else None,
            # 'brand_id':product.brand_id.id if product.brand_id else None,
            'cat_id':product.cat_id,
            'subcat_id':product.subcat_id,
            'brand_id':product.brand_id,
            'subcategories': subcategories,
            'brands':brands,
            'categories':categories,
            'image1':image1,
            'image2':image2,
            'image3':image3
            # 'category_id':categories.id,
            # 'category_name':categories.name,
            # 'brand_name':brands.br_name,
            # 'brands_id':brands.id,
            # 'subcat_name':subcategories.sub_name,
        }
        print(context['brand_id'])
    return render(request, 'update_product.html', {'context':context})
def delete_product(request, id):
    product = get_object_or_404(Products, id=id)
    ProductImage.objects.filter(img_id=id).delete()
    product.delete()
    messages.success("Product deleted successfully")
    return redirect('adminapp:list_product')

    
    


    