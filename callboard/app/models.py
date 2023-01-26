from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Response(models.Model):
    response_post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Отклик поста')
    response_content = models.TextField(verbose_name='Текст отклика')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создание')
    response_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор отклика')
    is_accepted = models.BooleanField(default=False, verbose_name='Состояния отклика')

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

class Post(models.Model):
    post_title = models.CharField(max_length=64, verbose_name='Название')
    post_content = models.TextField(verbose_name='Контент')
    created_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    changed_date = models.DateField(auto_now=True, verbose_name='Дата изменения')
    post_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    post_category = models.ManyToManyField('Category', through='PostCategory', verbose_name='Категория')

    def __str__(self):
        return f'{self.post_title}'
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
    def preview(self):
        return self.post_content[:64]
        
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Category(models.Model):
    Tanks = 'TN'
    Heals = 'HL'
    DD = 'DD'
    Sellers = 'SL'
    Gildmasters = 'GM'
    Questgivers = 'QG'
    Hammersmithes = 'HS'
    Skinners = 'SK'
    Potions = 'PO'
    Spell_masters = 'SM'

    CATS = [
        (Tanks, 'Танки'),
        (Heals, 'Хилы'),
        (DD, 'ДД'),
        (Sellers, 'Торговцы'),
        (Gildmasters, 'Гилдмастеры'),
        (Questgivers, 'Квестгиверы'),
        (Hammersmithes, 'Кузнецы'),
        (Skinners, 'Кожевники'),
        (Potions, 'Зельевары'),
        (Spell_masters, 'Мастера заклинаний'),
    ]
    category_name = models.CharField(max_length = 2, choices = CATS, default = Tanks, unique = True, verbose_name='Название Категории')
    subscribers = models.ManyToManyField(User, related_name='subscribers', verbose_name='Подписчики')
    
    def __str__(self):
        return f'{self.get_category_name_display()}'
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class PostCategory(models.Model):
    posts = models.ForeignKey(Post, on_delete = models.CASCADE)
    categories = models.ForeignKey(Category, on_delete = models.CASCADE)