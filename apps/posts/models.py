from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.core.models import CoreModel
from apps.core.utils import generate_unique_slug

User =get_user_model()

class Post(CoreModel):
    class Status(models.TextChoices):
        DRAFT = 'draft', _("Черновик")
        PUBLISHED = 'published', _("Опубликовано")

    title = models.CharField(max_length=128, verbose_name=_("Заголовок"))
    content = models.TextField(verbose_name=_("Содержание"))
    image = models.ImageField(upload_to='posts/', null=True, blank=True, verbose_name=_("Изображение"))
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PUBLISHED, verbose_name=_("Статус"))
    slug = models.SlugField(unique=True, verbose_name=_("Слаг"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", verbose_name=_("Автор"))
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name="posts", verbose_name=_("Категория"))
    tags = models.ManyToManyField('Tag', related_name="posts", blank=True, verbose_name=_("Теги"))

    class Meta:
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = generate_unique_slug(Post, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class PostLike(CoreModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_likes", verbose_name=_("Пользователь"))
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", verbose_name=_("Пост"))

    class Meta:
        verbose_name = _("Лайк поста")
        verbose_name_plural = _("Лайки постов")
        unique_together = ('user', 'post')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} -> {self.post.title}"
    

class Category(CoreModel):
    name = models.CharField(max_length=100, verbose_name=_("Наименование категории"))
    slug = models.SlugField(unique=True, verbose_name=_("Слаг категории"))

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = generate_unique_slug(Category, self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    

class Tag(CoreModel):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Название тега"))
    slug = models.SlugField(unique=True, verbose_name=_("Слаг"))

    class Meta:
        verbose_name = _("Тег")
        verbose_name_plural = _("Теги")
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = generate_unique_slug(Tag, self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name