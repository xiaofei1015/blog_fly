"""blog_fly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemap_views
from django.conf import settings
from rest_framework.routers import DefaultRouter

from blog.views import (
    PostDetailView, CategoryView, TagView, IndexView,
    SearchView, AuthorView
)
from config.views import LinkListView
from comment.views import CommentView
from blog.rss import LatestPostFeed
from blog.sitemap import PostSiteMap
from blog.apis import PostViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'post', PostViewSet, base_name='api_post')
router.register(r'category', CategoryViewSet, base_name='api_category')

urlpatterns = [
    url(r'^super_admin/', admin.site.urls, name='super_admin'),
    url(r'^admin/', xadmin.site.urls, name='xadmin'),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^post/(?P<post_id>\d+).html', PostDetailView.as_view(), name='post_detail'),
    url(r'^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category_list'),
    url(r'^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag_list'),
    url('^search/&',SearchView.as_view(), name='search'),
    url(r'^author/(?P<owner_id>\d+)/$', AuthorView.as_view(), name='author'),
    url(r'^links/$', LinkListView.as_view(), name='links'),
    url(r'^comment/$', CommentView.as_view(), name="comment"),
    url(r'^rss|feed/', LatestPostFeed(), name='rss'),
    url(r'^sitemap\.xml$', sitemap_views.sitemap, {'sitemaps': {'posts': PostSiteMap}}),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^api/', include(router.urls, namespace='api'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns =[
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
