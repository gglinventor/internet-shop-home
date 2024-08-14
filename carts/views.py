from django.shortcuts import redirect, render

from goods.models import Products
from carts.models import Cart


def cart_add(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)
        if carts.exists(): #если есть корзины у пользователя
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
            
    return redirect(request.META['HTTP_REFERER']) #"request.META['HTTP_REFERER']" - с какой страницы попал в этот контролер


def cart_change(request, product_slug):
    ...

def cart_remove(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    return redirect(request.META['HTTP_REFERER'])