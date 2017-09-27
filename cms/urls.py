# -*- coding: utf-8 -*-
from django.conf.urls import url
from cms import views

app_name = 'cms'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^article/(?P<article_id>\d+)$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})$', views.ArchiveView.as_view(), name="archive"),
    url(r'^category/(?P<pk>[0-9]+)$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)$', views.TagView.as_view(), name='tag'),
    url(r'^comment/post/(?P<pk>[0-9]+)/$', views.CommentView.as_view(), name='comment'),
    url(r"^about$", views.about, name='abount'),
    # url(r"^search/$", views.search, name="search"),
    # url(r'^comment/post/(?P<pk>[0-9]+)$', views.CommentView.as_view(), name='comments'),                                                                                                                                                                                     $', views.CommentView.as_view(), name='comments'),
]


                                        
