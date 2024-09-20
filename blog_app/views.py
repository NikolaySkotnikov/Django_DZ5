from lib2to3.fixes.fix_input import context

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from .dataset import dataset

menu = [
    {"name": "Главная", "alias": "main"},
    {"name": "Блог", "alias": "blog"},
    {"name": "О проекте", "alias": "about"},
]


def data_sort(x):
    return x['views']

def index(request):

    context = {
        'menu': menu,
        'page_alias': 'main',
        'last_posts': dataset[-3:],
        'popular_posts': sorted(dataset, key=data_sort, reverse=True)[:3],
    }

    return render(request, 'main.html', context=context)


def about(request):
    context = {
        'posts': dataset,
        'menu': menu,
        'page_alias': 'about',
    }
    return render(request, 'about.html', context=context)


def blog(request):

    paginator = Paginator(dataset, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': dataset,
        'menu': menu,
        'page_alias': 'blog',
        'page_obj': page_obj,
    }
    return render(request, 'blog_app/blog.html', context=context)


def post_by_slug(request, post_slug):
    post = [post for post in dataset if post['slug'] == post_slug]
    return render(request, 'blog_app/post_detail.html', context={'post':post[0], 'menu': menu})
