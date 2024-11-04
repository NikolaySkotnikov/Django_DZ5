from blog_app.views import menu


def get_menu(request):
    return {"menu": menu}
