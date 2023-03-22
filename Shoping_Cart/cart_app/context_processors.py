from .models import Cart,CartItem
from .views import cart_id


def counter(request):
    if 'admin' in request.path:
        return {}
    
    else:
        try:
            cart=Cart.objects.filter(cart_id=cart_id(request))
            cart_items=CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                item_count += cart_item.quantity
        except cart.DoesNotExist:
            item_count=0
    return dict(item_count=item_count)