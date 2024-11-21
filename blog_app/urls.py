from django.urls import path
from blog_app.views import blog, post_by_slug, posts_by_tag, posts_by_category

urlpatterns = [
    path('', blog, name='blog'),
    path('<slug:post_slug>', post_by_slug, name='post_by_slug'),
    path('category/<slug:category_slug>', posts_by_category, name='posts_by_category'),
    path('tag/<slug:tag_slug>', posts_by_tag, name='posts_by_tag'),
]
