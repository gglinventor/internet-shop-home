from django.contrib import admin

from goods.models import Categories, Products

#admin.site.register(Categories)
#admin.site.register(Products)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name',]
    
@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name', 'quantity', 'price', 'discount'] #отображение товаров значениями в виде столбцов
    list_editable = ['quantity', 'discount',] #возможность изменять характеристику товара без его открытия
    search_fields = ['name', 'description'] #добавление кнопки поиска и поиск по данным полям
    list_filter = ['discount', 'quantity', 'category'] #добавление фильтров по данным полям
    fields = ['name', 'category', 'slug', 'description', 'image', ('price', 'discount'), 'quantity'] #порядок выведения полей (в скобках, если в одной строке находится несколько полей)