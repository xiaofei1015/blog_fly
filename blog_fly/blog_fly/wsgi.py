"""
WSGI config for blog_fly project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_fly.settings")
profile = os.environ.get('BLOG_FLY_PROFILE', 'local_settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_fly.settings.%s' % profile)
application = get_wsgi_application()
