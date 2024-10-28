from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db.models import Prefetch
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from carts.models import Cart
from orders.models import Order, OrderItem
from common.mixins import CacheMixin
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    #success_url = reverse_lazy('main:index') #возвращает страницу для перехода только тогда, кодка действия все сделаны, потому что функция "reverse" может сработать раньше времени
    
    def get_success_url(self):
        redirect_page = self.request.POST.get('next', None)
        if redirect_page and redirect_page != reverse('user:logout'):
            return redirect_page
        return reverse_lazy('main:index')
    
    
    def form_valid(self, form): #срабатывает только после валидации и аутентификация (не авторизация) пользователя (проверка в системе на наличие такого пользователя с его данными)
        session_key = self.request.session.session_key
        user = form.get_user() #получение объекта пользователя
        if user:
            auth.login(self.request, user)
            if user.is_superuser:
                messages.success(self.request, f'{user.username}, добро пожаловать домой, хозяин!')
            elif user.is_staff:
                messages.success(self.request, f'{user.username}, добро пожаловать на работу!')
            else:
                messages.success(self.request, f'{user.username}, вы вошли в аккаунт')
        
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            
            return HttpResponseRedirect(self.get_success_url())
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Авторизация'
        return context


class UserRegistrationView(CreateView): #"CreateView" - для любой информации, которая вносится в базу данных
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user:profile')
    
    def form_valid(self, form): #срабатывает после валидации
        session_key = self.request.session.session_key
        user = form.instance #берём данные пользователя, так как в "form.get_user()" их нет, из-за того, что пользователь ещё не сформирован
        
        if user:
            form.save()
            auth.login(self.request, user)
            
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(self.request, f'{user.username}, вы успешно зарегистрированы и вошли в аккаунт')
            
            return HttpResponseRedirect(self.success_url)
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Регистрация'
        return context


class UserProfileView(LoginRequiredMixin, CacheMixin, UpdateView): #"LoginRequiredMixin", как и все Mixin-ы, надо указывать первыми
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('user:profile')
    context_object_name = 'user' #по умолчанию название такое же, как и название таблицы в базе данных


    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлён')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request, 'Произошла ошибка')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Home - Кабинет'
        
        orders = Order.objects.filter(user=self.request.user).prefetch_related(Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('product'),)).order_by('-id') #запрос не делается, так как Django делает запрос только тогда, когда это становится восстребовано(например: при присвоении значения переменной в контекстную переменную для html-шаблона)
        
        data = self.set_get_cache(orders, f'orders_for_user_{self.request.user.id}', 60)
        context['orders'] = data[0]
        context['all_price'] = data[1]
        
        # cache_orders = cache.get(f'orders_for_user_{self.request.user.id}')
        # if cache_orders:
        #     context['orders'] = cache_orders[0]
        #     context['all_price'] = cache_orders[1]
        # else:
        #     orders = Order.objects.filter(user=self.request.user).prefetch_related(Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('product'),)).order_by('-id')
        #     all_price = {}
        #     for order in orders:
        #         order_price = 0
        #         for item in order.orderitem_set.all():
        #             order_price += item.price * item.quantity
        #             all_price[order.id] = order_price
            
        #     cache.set(f'orders_for_user_{self.request.user.id}', [orders, all_price], 60)
        #     context['orders'] = orders
        #     context['all_price'] = all_price
        
        return context


@login_required()
def logout(request):
    messages.success(request, f'{request.user.username}, вы вышли из аккаунта')
    auth.logout(request)
    return redirect(reverse('main:index'))

class UserCartView(TemplateView):
    template_name = 'users/users_cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Home - Корзина'
        return context


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
            
#             session_key = request.session.session_key
            
#             if user:
#                 auth.login(request, user)
#                 messages.success(request, f'{username}, вы вошли в аккаунт')
                
#                 if session_key:
#                     Cart.objects.filter(session_key=session_key).update(user=user)
                
#                 redirect_page = request.POST.get('next', None)
#                 if redirect_page and redirect_page != reverse('user:logout'):
#                     return HttpResponseRedirect(request.POST.get('next'))
                
#                 return HttpResponseRedirect(reverse('main:index'))
#     else:
#         form = UserLoginForm()
    
#     context = {
#         'title': 'Home - Авторизация',
#         'form': form,
#     }
    
#     return render(request, 'users/login.html', context)


# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
            
#             session_key = request.session.session_key
            
#             user = form.instance
#             auth.login(request, user)
            
#             if session_key:
#                 Cart.objects.filter(session_key=session_key).update(user=user)
            
#             messages.success(request, f'{user.username}, вы успешно зарегистрированы и вошли в аккаунт')
#             return HttpResponseRedirect(reverse('main:index'))
#     else:
#         form = UserRegistrationForm()
    
#     context = {
#         'title': 'Home - Регистрация',
#         'form': form,
#     }
    
#     return render(request, 'users/registration.html', context)

# @login_required()
# def profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Профиль успешно обновлён')
#             return HttpResponseRedirect(reverse('user:profile'))
#     else:
#         form = ProfileForm(instance=request.user)
    
#     orders = Order.objects.filter(user=request.user).prefetch_related(Prefetch('orderitem_set', queryset=OrderItem.objects.select_related('product'),)).order_by('-id')
    
#     all_price = {}
#     for order in orders:
#         order_price = 0
#         for item in order.orderitem_set.all():
#             order_price += item.price * item.quantity
#         all_price[order.id] = order_price
    
#     context = {
#         'title': 'Home - Кабинет',
#         'form': form,
#         'orders': orders,
#         'all_price': all_price,
#     }
    
#     return render(request, 'users/profile.html', context)
#


# def users_cart(request):
#     context = {
#         'title': 'Home - Корзина'
#     }
#     return render(request, 'users/users_cart.html', context)