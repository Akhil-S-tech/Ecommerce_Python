from django.shortcuts import render
from shoping_app . models import Product,Category
from django.db.models import Q

# Create your views here.

def search_result(request):
    products=None
    query=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        products=Product.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))
    return render(request,'shop/search.html',{'query':query,"products":products})
