from django.contrib import admin

from .models import Item, Category, Review


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'id']
    list_display_links = ['id', 'name', 'category']
    list_filter = ['name', 'category', 'price']
    search_fields = ('name', 'price')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', 'star', 'session_id', 'name']
    list_display_links = ['id', 'item', 'session_id', 'star', 'name']
    list_filter = ['item', 'star', 'session_id', 'name']
    search_fields = ('name', 'session_id', 'item')
