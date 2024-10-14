from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import render
from .models import Post, Comment

menu = [
    {"name": "Главная", "alias": "main"},
    {"name": "Блог", "alias": "blog"},
    {"name": "О проекте", "alias": "about"},
]


def index(request):

    context = {
        'menu': menu,
        'page_alias': 'main',
        'last_posts': Post.objects.filter(status='published').order_by('-published_date')[:3],
        'popular_posts': Post.objects.filter(status='published').order_by('-views')[:3],
    }

    return render(request, 'main.html', context=context)


def about(request):
    context = {
        'menu': menu,
        'page_alias': 'about',
    }
    return render(request, 'about.html', context=context)


def blog(request):

    search_query = request.GET.get('search', '')

    if search_query:
        posts = (Post.objects.filter(Q(text__icontains=search_query) | Q(title__icontains=search_query)).filter(status='published'))
    else:
        posts = Post.objects.filter(status='published')

    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'menu': menu,
        'page_alias': 'blog',
        'page_obj': page_obj,
    }
    return render(request, 'blog_app/blog.html', context=context)


def post_by_slug(request, post_slug):

    post = Post.objects.get(slug=post_slug)
    Post.objects.filter(slug=post_slug).update(views=F('views') + 1)
    comments = Comment.objects.filter(post=post.id)

    context = {'post': post,
               'menu': menu,
               'comments': comments}

    return render(request, 'blog_app/post_detail.html', context=context)


def posts_by_tag(request, tag_slug):

    posts = Post.objects.filter(tags__slug=tag_slug).filter(status='published')

    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'menu': menu,
        'page_obj': page_obj,
        'page_alias': 'blog'}

    return render(request, 'blog_app/blog.html', context=context)


def posts_by_category(request, category_slug):

    posts = Post.objects.filter(category__slug=category_slug).filter(status='published')

    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'menu': menu,
        'page_obj': page_obj,
        'page_alias': 'blog'}

    return render(request, 'blog_app/blog.html', context=context)
