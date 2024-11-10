from django.urls import path
from blog_app.views import Blog, PostBySlug, PostsByTag, PostsByCategory, AddPost, UpdatePost

urlpatterns = [
    path('', Blog.as_view(), name='blog'),
    path('<slug:post_slug>', PostBySlug.as_view(), name='post_by_slug'),
    path('category/<slug:category_slug>', PostsByCategory.as_view(), name='posts_by_category'),
    path('tag/<slug:tag_slug>', PostsByTag.as_view(), name='posts_by_tag'),
    path('add_post/', AddPost.as_view(), name='add_post'),
    path('update_post/<slug:post_slug>', UpdatePost.as_view(), name='update_post'),
]
