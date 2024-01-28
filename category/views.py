from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from .models import Category,Subcategory,Products,ProductVarient,Brand
# Create your views here.
def add_category(request):
    return render(request,'add_category.html')