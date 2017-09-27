# -*- coding: utf-8 -*-
"""
Rss 模块

--Usage
    实现Rss订阅
"""

from django.contrib.syndication.views import Feed

from cms.models import Article


class AllArticeRssFeed(Feed):
    # 显示在聚合阅读器上的标题
    title = u"郭伟匡的个人技术博客"
    link = '/'
    description = u"个人发布的所有文章"

    def items(self):
        return Article.objects.all()

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.body

