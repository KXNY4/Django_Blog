from django.utils.text import slugify


def generate_unique_slug(model, pre_slug):
    """
    Генерация уникального слага для модели на основе заданного префикса.
    """
    slug = slugify(pre_slug)
    uq_slug = slug
    n = 1
    while model.objects.filter(slug=uq_slug).exists():
        uq_slug = f"{slug}-{n}"
        n += 1
    return uq_slug 