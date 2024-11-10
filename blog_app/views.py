from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .forms import PostForm, CommentForm
from .models import Post, Comment

menu = [
    {"name": "Главная", "alias": "main"},
    {"name": "Блог", "alias": "blog"},
    {"name": "О проекте", "alias": "about"},
    {"name": "Добавить пост", "alias": "add_post"}
]


class Index(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_alias'] = 'main'
        context['last_posts'] = Post.objects.select_related('author', 'category').prefetch_related('tags').filter(status='published').order_by('-published_date')[:3]
        context['popular_posts'] = Post.objects.select_related('author', 'category').prefetch_related('tags').filter(status='published').order_by('-views')[:3]
        return context


class About(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_alias'] = 'about'
        return context


class Blog(ListView):
    model = Post
    template_name = 'blog_app/blog.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):

        queryset = Post.objects.select_related('author', 'category').prefetch_related('tags').filter(status='published')

        search_query = self.request.GET.get('search', '')
        search_category = self.request.GET.get('search_category')
        search_tag = self.request.GET.get('search_tag')

        if search_query:
            query = Q(text__icontains=search_query) | Q(title__icontains=search_query)
            if search_category:
                query |= Q(category__name__icontains=search_query)
            if search_tag:
                query |= Q(tags__name__icontains=search_query)

            queryset = queryset.filter(query)

        return queryset.distinct().order_by('-published_date')

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['page_alias'] = 'blog'
        return contex


class PostBySlug(DetailView):
    model = Post
    template_name = 'blog_app/post_detail.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu

        comments = Comment.objects.filter(post=self.object.id).filter(status='accept')
        paginator = Paginator(comments, 2)
        page_obj = paginator.get_page(self.request.GET.get('page'))

        context['page_obj'] = page_obj
        context['comments'] = comments
        context['form'] = CommentForm()
        return context

    def get_object(self):
        obj = super().get_object()
        Post.objects.filter(slug=obj.slug).update(views=F('views') + 1)
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
        return self.render_to_response(self.get_context_data(form=form))


class PostsByTag(ListView):
    model = Post
    template_name = 'blog_app/blog.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['tag_slug']).filter(status='published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_alias'] = 'blog'
        return context


class PostsByCategory(ListView):
    model = Post
    template_name = 'blog_app/blog.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return (Post.objects.select_related('author', 'category')
                .prefetch_related('tags')
                .filter(category__slug=self.kwargs['category_slug'])
                .filter(status='published'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_alias'] = 'blog'
        return context


class AddPost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog_app/add_post.html'
    success_url = reverse_lazy('blog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_alias'] = 'add_post'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog_app/add_post.html'
    slug_url_kwarg = 'post_slug'

    def get_success_url(self):
        return reverse_lazy('post_by_slug', kwargs={'post_slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        return context
