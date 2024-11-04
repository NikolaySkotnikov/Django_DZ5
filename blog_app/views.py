from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import render, redirect
from .forms import PostForm, CommentForm
from .models import Post, Comment

menu = [
    {"name": "Главная", "alias": "main"},
    {"name": "Блог", "alias": "blog"},
    {"name": "О проекте", "alias": "about"},
    {"name": "Добавить пост", "alias": "add_post"}
]


def index(request):

    context = {
        'menu': menu,
        'page_alias': 'main',
        'last_posts': Post.objects.select_related('author', 'category').prefetch_related('tags').
                      filter(status='published').order_by('-published_date')[:3],
        'popular_posts': Post.objects.select_related('author', 'category').prefetch_related('tags').
                         filter(status='published').order_by('-views')[:3],
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
    search_category = request.GET.get('search_category')
    search_tag = request.GET.get('search_tag')
    page_number = request.GET.get('page')

    posts = Post.objects.select_related('author', 'category').prefetch_related('tags').filter(status='published')

    if search_query:
        query = Q(text__icontains=search_query) | Q(title__icontains=search_query)
        if search_category:
            query |= Q(category__name__icontains=search_query)
        if search_tag:
            query |= Q(tags__name__icontains=search_query)

        posts = posts.filter(query)

    posts = posts.distinct().order_by('-published_date')

    paginator = Paginator(posts, 4)
    page_obj = paginator.get_page(page_number)

    context = {
        'menu': menu,
        'page_alias': 'blog',
        'page_obj': page_obj,
    }
    return render(request, 'blog_app/blog.html', context=context)


def post_by_slug(request, post_slug):
    page_number = request.GET.get('page')

    post = Post.objects.get(slug=post_slug)
    Post.objects.filter(slug=post_slug).update(views=F('views') + 1)
    comments = Comment.objects.filter(post=post.id).filter(status='accept')

    paginator = Paginator(comments, 2)
    page_obj = paginator.get_page(page_number)

    context = {'post': post,
               'menu': menu,
               'page_obj': page_obj,
               'comments': comments}

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            context['form'] = form
            return render(request, 'blog_app/post_detail.html', context=context)
    else:
        form = CommentForm()
        context['form'] = form
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

    posts = (Post.objects.select_related('author', 'category').prefetch_related('tags').
             filter(category__slug=category_slug).filter(status='published'))

    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'menu': menu,
        'page_obj': page_obj,
        'page_alias': 'blog'}

    return render(request, 'blog_app/blog.html', context=context)


@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=True, author=request.user)
            return redirect('blog')
    else:
        form = PostForm()
    return render(request, 'blog_app/add_post.html', {'form': form, 'menu': menu, 'page_alias': 'add_post'})


def update_post(request, post_slug):
    post = Post.objects.get(slug=post_slug)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_by_slug', post_slug=post_slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog_app/add_post.html', {'form': form, 'menu':menu})
