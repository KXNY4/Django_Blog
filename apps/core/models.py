from django.db import models
from django.utils.translation import gettext_lazy as _

class CoreModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано в"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено в"))
    
    class Meta:
        abstract = True
