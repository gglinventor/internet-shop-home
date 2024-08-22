from django.contrib import admin

from carts.models import Cart

class CartTabAdmin(admin.TabularInline): #inline-режим
    model = Cart
    fields = 'product', 'quantity', 'created_timestamp'
    search_fields = 'product', 'quantity', 'created_timestamp'
    readonly_fields = ('created_timestamp',) #поля которые нельзя менять в inline-режиме
    extra = 1 #сколько можно добавить новых полей


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'product_display', 'quantity', 'created_timestamp',]
    list_filter = ['created_timestamp', 'user', 'product__name',] #"product__name" - поле name в записи таблицы product (иначе отображается значение в методе "__str__". Происходит такое из-за ForeignKey в котором есть метод "__str__", значение котрого и отображается). Примечание: не работает в "list_display"
    
    def user_display(self, object):
        if object.user:
            return str(object.user)
        return 'Анонимный пользователь'
    
    user_display.short_description = 'Пользователь' #название столбца в админке
    
    
    def product_display(self, object):
        return str(object.product.name)
    
    product_display.short_description = 'Товар'