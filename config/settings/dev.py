from .base import *

"""
    Development settings for drf_mini_blog project.
"""

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'drf_mini_blog_dev',
        'USER': 'postgres_dev',
        'PASSWORD': 'postgres_password_dev',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}