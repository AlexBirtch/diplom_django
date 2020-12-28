from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from shop.models import Item, Category
from .models import Order, ItemInOrder, Status


'''добавление товара в заказ'''
def add_item_to_cart(request, item_id, user):
    item = Item.objects.get(id=item_id)
    user_object = User.objects.get(username=user)

    try:
        current_order = Order.objects.get(user=user_object, is_active=True)
    except ObjectDoesNotExist:  # если заказа нет, то создаем
        current_order = Order.objects.create(user=user_object, is_active=True)

    # проверим наличие данного товара в заказе, если есть то увеличим его кол-во += 1
    try:
        current_item = ItemInOrder.objects.get(order=current_order, item=item)
        current_item.count += 1
        current_item.save()
    except ObjectDoesNotExist:
        ItemInOrder.objects.create(order=current_order, item=item)

    return redirect('base_view')


'''Отображение корзины конкретного полтзователя'''
def cart_view(request, user_name):
    template = 'shop/cart.html'
    current_user = User.objects.get(username=user_name)

    try:
        order = Order.objects.get(user=current_user, is_active=True)
        all_items_in_order = ItemInOrder.objects.filter(order=order)
        context = {'cart_items': all_items_in_order,
                   'cart_order': order,
                   'categories': Category.objects.all()}
    except ObjectDoesNotExist:
        context = {'empty_cart': True}

    return render(request, template, context)


'''Кнопка подтверждения заказа в корзине'''
def confirm_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.is_active = False
    order.save()
    return redirect('base_view')


def not_authenticated_user(request):
    template = 'shop/not_authenticated_user.html'
    return render(request, template)
