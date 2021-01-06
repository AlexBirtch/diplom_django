
from .models import Category

def menu(request):
    categories = Category.objects.all()

    return {"categories_list": categories}
