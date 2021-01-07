from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Item, Review, Category
from .forms import ReviewForm, CreateUserForm


'''Получаем имя пользователя (если авторизован) или его ID сессии'''
def get_session_id(request):
    if not request.user.is_authenticated:
        user_session = request.session.session_key
        if not user_session:
            user_session = request.session.cycle_key()
    else:
        user_session = request.user.username
    return user_session


'''главная страница'''
def base_view(request):
    phones = Item.objects.filter(category=1)[:3]
    wear = Item.objects.filter(category=2)[:3]
#    categories = Category.objects.all()
    context = {
                'phones': phones,
                'wear': wear,
                'user_session': get_session_id(request)}
    return render(request, 'shop/index.html', context)


'''страница обзора выбранного товара'''
def item_view(request, item_id):
    user_session = request.session.session_key
    if not user_session:
        request.session.cycle_key()
        user_session = request.session.session_key

    item = get_object_or_404(Item, id=item_id)
    form = ReviewForm()  # форма добавления комментария из forms.py
    context = {'item': item,
               'form': form,
               'user_session': get_session_id(request),
               'categories': Category.objects.all()}

    # отображение отзывов, если они есть
    for review in item.reviews.all():
        if review.session_id == user_session:
            context['reviewd'] = True
            break

    # добавление комментария
    if request.method == 'POST':
        # обойти ошибку при отзыве
        # без выбора количества звезд
        if request.POST.get('stars'):
            form = ReviewForm(request.POST)
            if form.is_valid:
                print('form is valid')
                print(request.POST)
                Review.objects.create(item=Item.objects.get(id=item_id),
                                      name=request.POST.get('name'),
                                      text=request.POST.get('text'),
                                      star=request.POST.get('stars'),
                                      session_id=user_session
                                      )
                return redirect('item_view', item_id=item_id)
        else:
            pass
    return render(request, 'shop/item.html', context)


'''страница регистрации аккаунта'''
def registration_view(request):
    template = 'shop/registration1.html'
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Создан аккаунт пользователя ' + user)
            return redirect('login')

    context = {'form': form}
    return render(request, template, context)


'''страница авторизации'''
def login_view(request):
    template = 'shop/login1.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('base_view')
        else:
            messages.info(request, 'Логин или пароль не корректны...')

    return render(request, template)


def logout_view(request):
    logout(request)
    return redirect('login')


'''Отображение товаров выбранной категории'''
def category_view(request, category_name):
    current_category = Category.objects.get(name=category_name)
    items_in_current_category = current_category.items.all()
    template = 'shop/category_items.html'

    paginator = Paginator(items_in_current_category, 3)
    current_page = int(request.GET.get('page', 1))
    page_object = paginator.get_page(current_page)
    prev_page, next_page = None, None

    if page_object.has_next():
        next_page = f'?page={page_object.next_page_number()}'
    if page_object.has_previous():
        prev_page = f'?page={page_object.previous_page_number()}'

    context = {'user_session': get_session_id(request),
               'category_items': page_object,
               'current_page': current_page,
               'prev_page_url': prev_page,
               'next_page_url': next_page,
               'categories': Category.objects.all()}

    return render(request, template, context)


'''пустая страница'''
def empty_view(request):
#    categories = Category.objects.all()
    context = {'user_session': get_session_id(request)}
    template = 'shop/empty_section.html'
    return render(request, template, context)
