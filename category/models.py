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
    br_logo=models.ImageField(upload_to='',null=True, blank=True)
    br_dsc=models.TextField(max_length=200)
class Products(models.Model):
    pr_name=models.CharField(max_length=100)
    cat_id=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='prodcat')  
    brand_id=models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='brand')
    subcat_id=models.ForeignKey(Subcategory,on_delete=models.CASCADE,related_name='prosubcat')  
    price=models.FloatField()
    sale_price=models.FloatField()
    prodvar_img=models.ImageField(upload_to='',null=True, blank=True)

class ProductVarient(models.Model):
    prod_id=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='product_varient')  
    Color=models.CharField(max_length=200)
    size=models.CharField(max_length=5)
    stock=models.IntegerField()
    discount=models.IntegerField()
    prodvar_img=models.ImageField(upload_to='',null=True, blank=True)
