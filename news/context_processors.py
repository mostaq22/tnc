from .models import Category


def navigation(request):
    return {
        'navigation_items': Category.objects.filter(show_in_menu=True).all()
    }
