from .base import *


DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': 'xiaofei1017',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}