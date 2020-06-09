import datetime

from django.core.cache import cache
from django.db.models import Q, F
from django.shortcuts import render
from django.http import HttpResponse
from .models import Tag, Post, Category
from config.models import SideBar
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from comment.forms import CommentForm
from comment.models import Comment

def post_list(request, category_id=None, tag_id=None):
    """
    文章首页
    :param request:
    :param category_id: 分类id
    :param tag_id: 标签id
    :return:
    """
    tag = None
    category = None

    if tag_id:
        tag, post_list = Post.get_by_tag(tag_id)
    elif category_id:
        category, post_list = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all()
    }
    context.update(Category.get_navs())
    print(context)
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id=None):
    """
    文章详情
    :param request:
    :param post_id: 文章id
    :return:
    """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None

    context = {
        'post': post,
        'sidebars': SideBar.get_all()
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)


class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all()
        })
        context.update(Category.get_navs())
        posts = Post.objects.select_related('owner')
        authors = []
        for post in posts:
            if post.owner.username not in authors:
                authors.append(post.owner.username)
        context.update({
            'authors': authors
        })
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category
        })
        return context

    def get_queryset(self):
        """
        重写queryset
        :return:
        """
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag
        })
        return context

    def get_queryset(self):
        """
        重写queryset
        :return:
        """
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


class SearchView(IndexView):
    """
    首页搜索, 通过title和desc进行搜索
    """
    def get_context_data(self):
        print(self.request.GET)
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    """
    只展示特定作者的文章
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)

class PostDetailView(CommonViewMixin, DetailView):
    model = Post
    queryset = Post.objects.filter(status=Post.STATUS_NORMAL)
    template_name = "blog/detail.html"
    pk_url_kwarg = 'post_id'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' %(uid, str(datetime.date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60)

        if not cache.get(uv_key):
            current = datetime.datetime.now()
            tomorrow = (current + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            remain_seconds = (tomorrow - current).seconds  # 到明天凌晨还有多少秒
            increase_uv = True
            cache.set(uv_key, 1, remain_seconds)
        if increase_pv and increase_uv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Post.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Post.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)
