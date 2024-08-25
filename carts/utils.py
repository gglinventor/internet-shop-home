from carts.models import Cart

def get_user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).select_related('product') #одним запросом сразу же выбрать корзины, которые ссылаются на выбранные
    
    if not request.session.session_key:
        request.session.create()
    
    return Cart.objects.filter(session_key=request.session.session_key).select_related('product') #когда выбираются корзины, сразу же выбрать одним запросом выбрать те, которые на них ссылаются