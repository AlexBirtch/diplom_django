from django.contrib import admin

from .models import Order, Status, ItemInOrder


class ItemInOrderInline(admin.TabularInline):
    model = ItemInOrder
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'is_active', 'status']
    list_display_links = ['id', 'user']
    list_filter = ['user', 'status']

    inlines = [ItemInOrderInline]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active']
    list_display_links = ['id', 'name']
    list_filter = ['name', 'is_active']


@admin.register(ItemInOrder)
class ItemInOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'item', 'count', 'price_per_item', 'total_price']
    list_display_links = ['id', 'order', 'item']
    list_filter = ['order', 'item']
