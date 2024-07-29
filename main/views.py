from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories


def index(request):
    context = {
        'title': 'Home - Главная',
        'content': 'Магазин мебели HOME',
    }
    
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        'title': 'Home - О нас',
        'content': 'О нас',
        'text_on_page': 'Лучший магазин мебели в городе! У нас самый качественный товар!'
    }
    
    return render(request, 'main/about.html', context)


def shipping_and_payment(request):
    context = {
        'title': 'Home - О нас',
        'content': 'Доставка и оплата',
        'text_on_page': 'Довезём быстро, платить наличкой 😀'
    }
    
    return render(request, 'main/about.html', context)


def contact(request):
    context = {
        'title': 'Home - О нас',
        'content': 'Контактная информация',
        'text_on_page': 'Звонить, если есть вопросы, по номеру: 8-800-555-35-35'
    }
    
    return render(request, 'main/about.html', context)