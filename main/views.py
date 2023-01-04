from django.contrib.auth import authenticate, login
from django.db.models import Max, Min
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from main.forms import SignupForm
from main.models import Category, Brand, Product, ProductAttribute


# Create your views here.

# Home Page
def home(request):
    # banners= Banner.objects.all().order_by('-id')
    data = Product.objects.filter(is_featured=True).order_by('id')
    return render(request, 'index.html', {'data': data})


# Category
def category_list(request):
    data = Category.objects.all().order_by('id')
    return render(request, 'category_list.html', {'data': data})


# Brand
def brand_list(request):
    data = Brand.objects.all().order_by('-id')
    return render(request, 'brand_list.html', {'data': data})


# Cart
def cart(request):
    return render(request, 'cart.html')


# # Product
# def product_list(request):
#     total_data = Product.objects.count()
#     data = Product.objects.all().order_by('-id')[:3]
#     min_price = ProductAttribute.objects.aggregate(Min('price'))
#     max_price = ProductAttribute.objects.aggregate(Max('price'))
#     return render(request, 'product_list.html',
#                   {'data': data, 'total_data': total_data, 'min_price': min_price, 'max_price': max_price, })

def product_list(request):
    data = Product.objects.all().order_by('id')
    cats = Product.objects.distinct().values('category__title', 'category__id')
    brands = Product.objects.distinct().values('brand__title', 'brand_id')
    colors = ProductAttribute.objects.distinct().values('color__title', 'color_id', 'color__color_code')
    sizes = ProductAttribute.objects.distinct().values('size__title', 'size_id')
    return render(request, 'product_list.html',
                  {'data': data, 'cats': cats, 'brands': brands, 'colors': colors, 'sizes': sizes})


# Product Detail
def product_detail(request, slug, id):
    product = Product.objects.get(id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    colors = ProductAttribute.objects.filter(product=product).values('color__id', 'color__title',
                                                                     'color__color_code').distinct()
    sizes = ProductAttribute.objects.filter(product=product).values('size__id', 'size__title', 'price',
                                                                    'color__id').distinct()

    return render(request, 'product_detail.html',
                  {'data': product, 'related': related_products, 'colors': colors, 'sizes': sizes})


# Signup Form
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=pwd)
            login(request, user)
            return redirect('home')
    form = SignupForm
    return render(request, 'registration/signup.html', {'form': form})
