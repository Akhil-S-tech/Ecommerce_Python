
from django.shortcuts import get_object_or_404, redirect, render
from shoping_app . models import Product
from . models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=cart_id(request))
        cart.save(),
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(product=product,quantity=1,cart=cart)
        cart.save()
    return redirect('cart_app:cart_detail')

def cart_detail(request,total=0,counter=0,cart_items=None):
    try:
        cart=Cart.objects.get(cart_id=cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price *cart_item.quantity)    
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'shop/cart.html',dict(cart_items=cart_items,total=total,counter=counter))

def cart_remove(request,product_id):
    cart=Cart.objects.get(cart_id=cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_app:cart_detail')

def full_delete(request,product_id):
    cart=Cart.objects.get(cart_id=cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart_app:cart_detail')

def checkout(request,total=0,quantity=0,cart_items=None):
    grand_total=0
    tax=0
    for cart_item in cart_items:
      total += int(cart_item.price)*int(cart_item.quantity)
      quantity += cart_item.quantity
      tax = (5 * total)/100
      grand_total = total + tax

    context = {
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }
    return render(request, 'shop/cart.html', context)
    

