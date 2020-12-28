from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from shop.models import Item


'''Модель статуса заказа'''
class Status(models.Model):
    name = models.CharField('Статус', max_length=24)
    is_active = models.BooleanField('Активен', default=True)

    def __str__(self):
        return f'Статус {self.name}'

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'


'''Модель заказа'''
class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(Status, verbose_name='Статус', on_delete=models.CASCADE,
                               default=None, blank=True, null=True)
    total_price = models.DecimalField('Итоговая цена заказа', max_digits=10, decimal_places=2, default=0)
    total_items_count = models.IntegerField('Общее количество товаров в заказе', default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'ID заказа: %s | Пользователь: %s' % (self.id, self.user)


'''Модель товара в заказе'''
class ItemInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Товар')
    count = models.IntegerField('Количество', default=1)
    price_per_item = models.DecimalField('Цена за штуку', max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField('Общая стоимость', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        price_per_item = self.item.price
        self.price_per_item = price_per_item
        self.total_price = price_per_item * self.count
        super(ItemInOrder, self).save(*args, **kwargs)


'''функция перезаписи данных в модели товара в заказе'''
def item_in_order_post_save(sender, instance, created, **kwargs):
    all_items_in_order = ItemInOrder.objects.filter(order=instance.order)
    order_total_price = 0
    total_items_count_in_order = 0

    for item in all_items_in_order:
        order_total_price += item.total_price
        total_items_count_in_order += item.count

    instance.order.total_price = order_total_price
    instance.order.total_items_count = total_items_count_in_order
    instance.order.save(force_update=True)


post_save.connect(item_in_order_post_save, sender=ItemInOrder)
