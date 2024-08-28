from django.http import Http404
from django.views.generic import DetailView, ListView

from goods.models import Products
from goods.utils import q_search


class CatalogView(ListView):
    model = Products #равносильно Products.objects.all() - если нет метода "get_queryset"
    #queryset = Products.objects.filter(category__slug=category_slug).order_by('-id') - если надо получить записи таблицы, обработанные Django ORM
    template_name = 'goods/catalog.html'
    context_object_name = 'goods' #переопределение названия контекстной переменной (изначальное название "object_list")
    paginate_by = 3 #сколько товаров на странице отображать
    allow_empty = False
    
    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug') #название конвертора
        on_sale = self.request.GET.get('on_sale')
        order_by = self.request.GET.get('order_by') 
        query = self.request.GET.get('q')
        
        if category_slug == 'all':
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()
        
        if on_sale:
            goods = goods.filter(discount__gt=0)
        
        if order_by and order_by != "default":
            goods = goods.order_by(order_by)
            
        return goods
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Каталог"
        context["category_slug"] = self.kwargs.get('category_slug')
        return context


class ProductView(DetailView): #в данном классе нет пагинации
    #model = Products
    #slug_field = 'slug' - в каком столбце модели хранится значение "slug"
    
    template_name = 'goods/product.html'
    slug_url_kwarg = 'product_slug' #какое название конвертора с "slug"
    context_object_name = 'product' #переопределение названия контекстной переменной (изначальное название "object")
    
    def get_object(self, queryset=None):
        product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name #"object" - непереопределённая контекстная переменная, к которой можно обращаться через точку
        return context

 
# def catalog(request, category_slug=None):
#     page = request.GET.get('page', 1)
#     on_sale = request.GET.get('on_sale', None)
#     order_by = request.GET.get('order_by', None)
#     query = request.GET.get('q', None)
    
    
#     if category_slug == 'all':
#         goods = Products.objects.all()
#     #else:
#         #goods = get_list_or_404(Products.objects.filter(category__slug=category_slug)) не работает. Ниже код, чтобы хоть как-то отображалось
#     elif query:
#         goods = q_search(query)
#     #else:
#         #goods = Products.objects.filter(category__slug=category_slug) моя версия исправленного кода
#     else:
#         goods = Products.objects.filter(category__slug=category_slug)
#         if not goods.exists():
#             raise Http404()
    
#     if on_sale:
#         goods = goods.filter(discount__gt=0)
#     if order_by and order_by != "default":
#         goods = goods.order_by(order_by)

#     paginator = Paginator(goods, 3)
#     current_page = paginator.page(int(page)) #текущая страница    

#     context = {
#         "title": "Home - Каталог",
#         "goods": current_page,
#         "category_slug": category_slug,
#     }
#     return render(request, "goods/catalog.html", context)


# def product(request, product_slug):
#     product = Products.objects.get(slug=product_slug)

#     context = {
#         "title": f"Home - {product.name}",
#         "product": product,
#     }

#     return render(request, "goods/product.html", context)
