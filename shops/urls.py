# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreateShopView, UpdateShopView, ShopListView
)


urlpatterns = patterns(
    '',
    url(r'^create/$', CreateShopView.as_view(), name='create'),
    url(r'^list/$', ShopListView.as_view(), name='list'),
    url(r'^update/(?P<pk>\d+)/$', UpdateShopView.as_view(), name='update'),
)