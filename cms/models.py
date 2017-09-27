# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import markdown

from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags


@python_2_unicode_compatible
class Article(models.Model):
    """文章各字段的定义，其中需要注意的是
    一篇文章只有一个分类，而一篇文章可以打多个标签
    """
    STATUS_CHIOCE = (
        ('p', '发布'),
        ('d', '草稿')
    )
    title = models.CharField('标题', max_length=100)
    body = models.TextField('正文')
    author = models.ForeignKey(User)
    abstract = models.CharField('文章摘要', max_length=120, blank=True,
                                null=True, help_text=u"可选, 若没有则取文章前60字符")
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHIOCE)
    create_time = models.DateField('创建时间', auto_now_add=True)
    update_time = models.DateField('更新时间', auto_now=True)
    category = models.ForeignKey('Category', verbose_name='分类',
                                 null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', verbose_name='标签', blank=True)
    view = models.PositiveIntegerField('浏览量', default=0)
    like = models.PositiveIntegerField('喜欢量', default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cms:detail', kwargs={'article_id': self.pk})

    def increase_view(self):
        self.view += 1
        self.save(update_fields=['view'])

    def save(self, *args, **kwargs):
        """重写save方法，目地是为了自动获取文章摘要"""
        if not self.abstract:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.abstract = strip_tags(md.convert(self.body))[:54]

        super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-update_time']


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField('类别名', max_length=20)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField('标签名', max_length=20)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Comment(models.Model):
    name = models.CharField('用户名', max_length=30)
    email = models.CharField('用户邮箱', max_length=50)
    body = models.TextField('评论内容')
    create_time = models.DateField('评论时间', auto_now_add=True)
    article = models.ForeignKey('Article', verbose_name='评论所属文章', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
