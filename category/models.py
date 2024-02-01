from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    cat_dsc=models.TextField(max_length=200,blank=True)
    published=models.BooleanField(default=True)
    cat_img=models.ImageField(upload_to='category_images/',null=True, blank=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    cat_id=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='subcat')  
    sub_name=models.CharField(max_length=100)
    sub_img=models.ImageField(upload_to='subcat_images/',null=True, blank=True) 
    def __str__(self):
        return self.sub_name
class Brand(models.Model):
    br_name=models.CharField(max_length=200)
    def __str__(self):
        return self.br_name

class Products(models.Model):
    pr_name=models.CharField(max_length=100)
    cat_id=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='prodcat')  
    brand_id=models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True,blank=True,related_name='brand')
    subcat_id=models.ForeignKey(Subcategory,on_delete=models.CASCADE,related_name='prosubcat')  
    is_available=models.BooleanField(default=True)
    # price=models.FloatField()
    # sale_price=models.FloatField()
    # discount=models.IntegerField(null=True,blank=True)
    def __str__(self):
        return self.pr_name
class ProductImage(models.Model):
    image=models.ImageField(upload_to='product_image/',null=True, blank=True)
    img_id=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='product_image')  

# 
class Color(models.Model):
    color=models.CharField(max_length=200)
    def __str__(self):
        return self.color

class Size(models.Model):
    size=models.CharField(max_length=200)
    def __str__(self):
        return self.size
class ProductVar(models.Model):
    prod_id=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='product_varient')  
    color=models.ForeignKey(Color,on_delete=models.CASCADE,related_name='product_color')  
    size=models.ForeignKey(Size,on_delete=models.CASCADE,related_name='product_size')  
    stock=models.IntegerField()
    price=models.FloatField(default=0,null=False,blank=False)
    discount=models.IntegerField(null=True,blank=True)
    is_active=models.BooleanField(default=True)
    # prodvar_img=models.ImageField(upload_to='',null=True, blank=True)
# class VarientImage(models.Model):
#     varient_id=models.ForeignKey(Color,on_delete=models.CASCADE,related_name='varient_image')
#     prod_img=models.ImageField(upload_to='varient_img/',null=True, blank=True)