from django.urls import path

from order import views

urlpatterns = [
    path('cart/<str:user_name>', views.cart_view, name='cart'),
    path('cart/<int:item_id>/<str:user>', views.add_item_to_cart, name='add_item_to_cart'),
    path('confirm_order/<int:order_id>', views.confirm_order, name='confirm_order'),
    path('not_authenticated_user/', views.not_authenticated_user, name='not_authenticated_user'),
]
