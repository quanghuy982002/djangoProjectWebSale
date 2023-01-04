from django.db.models import Max, Min
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

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


# # Filter Data
# def filter_data(request):
#     colors = request.GET.getlist('color[]')
#     categories = request.GET.getlist('category[]')
#     brands = request.GET.getlist('brand[]')
#     sizes = request.GET.getlist('size[]')
#     minPrice = request.GET['minPrice']
#     maxPrice = request.GET['maxPrice']
#     allProducts = Product.objects.all().order_by('-id').distinct()
#     allProducts = allProducts.filter(productattribute__price__gte=minPrice)
#     allProducts = allProducts.filter(productattribute__price__lte=maxPrice)
#     if len(colors) > 0:
#         allProducts = allProducts.filter(productattribute__color__id__in=colors).distinct()
#     if len(categories) > 0:
#         allProducts = allProducts.filter(category__id__in=categories).distinct()
#     if len(brands) > 0:
#         allProducts = allProducts.filter(brand__id__in=brands).distinct()
#     if len(sizes) > 0:
#         allProducts = allProducts.filter(productattribute__size__id__in=sizes).distinct()
#     t = render_to_string('ajax/product-list.html', {'data': allProducts})
#     return JsonResponse({'data': t})

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


# Add to cart
def add_to_cart(request):
    # del request.session['cartdata']
    cart_p = {}
    cart_p[str(request.GET['id'])] = {
        'image': request.GET['image'],
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})
