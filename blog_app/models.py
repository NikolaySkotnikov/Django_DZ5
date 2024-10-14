from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class Post(models.Model):

    STATUS_CHOICES = (
        ("published", "Опубликовано"),
        ("draft", "Черновик")
    )

    title = models.CharField(max_length=300, unique=True, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    slug = models.SlugField(unique=True, verbose_name='Адрес страницы')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Автор', related_name='posts')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория',
                                 related_name='posts', null=True, default=None)
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='Теги', related_name='posts', default=None)
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    cover_image = models.ImageField(blank=True, null=True, verbose_name='Обложка', upload_to='media/images/')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')

    def save(self, *args, **kwargs):
        slug = slugify(unidecode(self.title))
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_by_slug", args=[str(self.slug)])

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Category(models.Model):

    name = models.CharField(max_length=300, unique=True, verbose_name='Категория')
    slug = models.SlugField(unique=True, verbose_name='Адрес страницы')

    def save(self, *args, **kwargs):
        slug = slugify(unidecode(self.name))
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("posts_by_category", args=[str(self.slug)])

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(models.Model):

    name = models.CharField(max_length=100, unique=True, verbose_name='Тег')
    slug = models.SlugField(unique=True, verbose_name='Адрес страницы')

    def save(self, *args, **kwargs):
        slug = slugify(unidecode(self.name))
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'#{self.name}'

    def get_absolute_url(self):
        return reverse('posts_by_tag', args=[str(self.slug)])

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Comment(models.Model):

    STATUS_CHOICES = (
        ("unchecked", "Не проверен"),
        ("accept", "Проверен"),
        ("rejected", "Отклонен"),
    )

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(max_length=2000, verbose_name='Текст комментария')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='unchecked')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост', related_name='comments')
    created_data = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
