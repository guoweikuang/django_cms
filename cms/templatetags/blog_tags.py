# -*- coding: utf-8 -*-
from django import template
from cms.models import Article, Tag, Category
from django.db.models.aggregates import Count

register = template.Library()


@register.simple_tag
def get_recent_article(num=5):
    return Article.objects.all().order_by('-create_time')[:num]


@register.simple_tag
def archive():
    return Article.objects.dates('create_time', 'month', order='DESC')


@register.simple_tag
def get_category():
    return Category.objects.annotate(num_posts=Count('article')).filter(num_posts__gt=0)


@register.simple_tag
def get_tag():
    return Tag.objects.all()
