# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.text import slugify
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.db.models import Q

from cms.forms import CommentForm
from cms.models import Article, Tag, Category
import markdown
from markdown.extensions.toc import TocExtension


class IndexView(ListView):
    """
    首页视图，使用类视图
    """
    template_name = 'cms/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        """
        重写该方法，目的是为了处理装换数据，如markdown转化
        """
        articles = Article.objects.all()

        for article in articles:
            article.body = markdown.markdown(article.body,
                                             extensions=[
                                                 'markdown.extensions.extra',
                                                 'markdown.extensions.codehilite',
                                                 'markdown.extensions.toc',
                                             ])
        return articles

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['categorys'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'cms/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'article_id'

    def get_object(self):
        post = super(ArticleDetailView, self).get_object()
        md = markdown.Markdown(extensions=[
                                'markdown.extensions.extra',
                                'markdown.extensions.codehilite',
                                TocExtension(slugify=slugify)
                               ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        post.increase_view()

        return post

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
        })
        return context


class CategoryView(ListView):
    template_name = 'cms/index.html'
    context_object_name = 'articles'
    model = Article

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)


class TagView(ListView):
    template_name = 'cms/index.html'
    context_object_name = 'articles'
    model = Article

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


class ArchiveView(ListView):
    model = Article
    template_name = 'cms/index.html'
    context_object_name = 'articles'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(create_time__year=year,
                                                             create_time__month=month)


class CommentView(FormView):
    form_class = CommentForm
    template_name = 'cms/detail.html'

    def form_valid(self, form):
        import logging
        logging.info('hello`')
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.article = article
        comment.save()

        self.success_url = article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        import logging
        logging.info('hello, world')
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        # return HttpResponseRedirect('http://localhost:8000')
        return render(self.request, 'cms/detail.html', {
            'form': form,
            'post': article,
            'comment_list': article.comment_set.all(),
        })


def about(request):
    return render(request, 'cms/about.html')


def search(request):
    q = request.GET.get('q')
    error_msg = u"请输入关键词"

    if not q:
        error_msg = u"请输入关键词"
        return render(request, 'cms/index.html', {'error_msg': error_msg})
    post_list = Article.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'cms/index.html', {'error_msg': error_msg,
                                              'articles': post_list})
