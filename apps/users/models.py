from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from apps.core.models import CoreModel

class CustomUser(AbstractUser):
    
    email = models.EmailField(unique=True, verbose_name=_("Электронная почта"))
    username = models.CharField(max_length=50, unique=True, verbose_name=_("Имя пользователя"))
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_("Аватар"))
    bio = models.TextField(max_length=500, blank=True, verbose_name=_("Биография"))
    email_verified = models.BooleanField(default=False, verbose_name=_("Электронная почта подтверждена"))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")
        ordering = ['-date_joined']