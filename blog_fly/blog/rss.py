from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Post


class ExtendRssFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        handler.addQuickElement('content:html', item['content_html'])


class LatestPostFeed(Feed):
    feed_type = ExtendRssFeed
    title = 'fly Blog system'
    link = '/rss/'
    description = 'fly is a blog system power by django'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return reverse('post_detail', args=[item.pk])

    def item_description(self, item):
        return item.desc

    def item_extra_kwargs(self, item):
        return {'content_html': self.content_html(item)}

    def content_html(self, item):
        return item.content_html



