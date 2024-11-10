from .views import menu


def get_menu(request):
    return {"menu": menu}
