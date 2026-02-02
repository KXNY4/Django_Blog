from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from apps.core.models import CoreModel
from apps.core.utils import generate_unique_slug

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