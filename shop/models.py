from django.db import models

'''Модель товара'''
class Item(models.Model):
    name = models.CharField('Название', max_length=250)
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    category = models.ForeignKey('Category', related_name='items',
                                 verbose_name='Категория товара',
                                 on_delete=models.CASCADE,
                                 blank=True, null=True)
    description = models.CharField('Краткое описание', max_length=250, blank=True)
    price = models.DecimalField('Цена', max_digits=20, decimal_places=2)
    image = models.ImageField('Изображение')
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['created_date']

    def __str__(self):
        return self.name

'''Класс категории товара'''
class Category(models.Model):
    name = models.CharField('Название категории', max_length=250)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

'''Модель отзыва к товару'''
class Review(models.Model):
    item = models.ForeignKey(Item, related_name='reviews', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField('Имя', max_length=250)
    text = models.TextField('Отзыв')
    star = models.IntegerField(null=True, blank=True)
    session_id = models.CharField('id сессии', max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-id']
