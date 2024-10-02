from django.core.paginator import Paginator
from django.shortcuts import render
from .dataset import dataset
from .models import Post

menu = [
    {"name": "Главная", "alias": "main"},
    {"name": "Блог", "alias": "blog"},
    {"name": "О проекте", "alias": "about"},
]


def index(request):

    context = {
        'menu': menu,
        'page_alias': 'main',
        'last_posts': Post.objects.all().order_by('-published_date')[:3],
        'popular_posts': Post.objects.all().order_by('-views')[:3],
    }

    return render(request, 'main.html', context=context)


def about(request):
    context = {
        'menu': menu,
        'page_alias': 'about',
    }
    return render(request, 'about.html', context=context)


def blog(request):

    posts = Post.objects.all()

    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'menu': menu,
        'page_alias': 'blog',
        'page_obj': page_obj,
    }
    return render(request, 'blog_app/blog.html', context=context)


def post_by_slug(request, post_slug):

    post = Post.objects.get(slug=post_slug)
    context = {'post': post,
               'menu': menu}

    return render(request, 'blog_app/post_detail.html', context=context)
