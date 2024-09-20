from django.urls import path
from blog_app.views import blog, post_by_slug

urlpatterns = [
    path('', blog, name='blog'),
    path('<slug:post_slug>', post_by_slug, name='post_by_slug')
]