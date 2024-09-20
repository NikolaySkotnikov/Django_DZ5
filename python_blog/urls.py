from django.contrib import admin
from django.urls import path, include
from blog_app.views import index, about

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='main'),
    path('about/', about, name='about'),
    path('blog/', include('blog_app.urls')),
]
