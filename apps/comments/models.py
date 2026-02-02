from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.core.models import CoreModel

User = get_user_model()

class Comment(CoreModel):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, related_name='comments', verbose_name=_("Пост"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Автор"))
    content = models.TextField(max_length=1000, verbose_name=_("Содержание"))

    class Meta:
        verbose_name = _("Комментарий")
        verbose_name_plural = _("Комментарии")
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username}: {self.content[:50]}"