from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Главная'
        context['content'] = 'Магазин мебели HOME'
        return context
        

# def index(request):
    # context = {
    #     'title': 'Home - Главная',
    #     'content': 'Магазин мебели HOME',
    # }
    
    # return render(request, 'main/index.html', context)



class AboutView(TemplateView):
    template_name = 'main/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Информация'
        context['content'] = 'О нас'
        context['text_on_page'] = 'Лучший магазин мебели в городе! У нас самый качественный товар!'
        return context
    
# def about(request):
#     context = {
#         'title': 'Home - О нас',
#         'content': 'О нас',
#         'text_on_page': 'Лучший магазин мебели в городе! У нас самый качественный товар!'
#     }
    
#     return render(request, 'main/about.html', context)


class ShippingAndPaymentView(TemplateView):
    template_name = 'main/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Информация'
        context['content'] = 'Доставка и оплата'
        context['text_on_page'] = 'Довезём быстро, платить наличкой 😀'
        return context


# def shipping_and_payment(request):
#     context = {
#         'title': 'Home - О нас',
#         'content': 'Доставка и оплата',
#         'text_on_page': 'Довезём быстро, платить наличкой 😀'
#     }
    
#     return render(request, 'main/about.html', context)


class ContactView(TemplateView):
    template_name = 'main/about.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Информация'
        context['content'] = 'Контактная информация'
        context['text_on_page'] = 'Звонить, если есть вопросы, по номеру: 8-800-555-35-35'
        return context


# def contact(request):
#     context = {
#         'title': 'Home - О нас',
#         'content': 'Контактная информация',
#         'text_on_page': 'Звонить, если есть вопросы, по номеру: 8-800-555-35-35'
#     }
    
#     return render(request, 'main/about.html', context)