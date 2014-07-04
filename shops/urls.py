# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreateShopView, UpdateShopView, ShopListView, ShopDetailView,
    LoadFoodsCountView
)


urlpatterns = patterns(
    '',
    url(r'^create/$', CreateShopView.as_view(), name='create'),
    url(r'^list/$', ShopListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', ShopDetailView.as_view(), name='detail'),
    url(r'^update/(?P<pk>\d+)/$', UpdateShopView.as_view(), name='update'),
    url(r'^load_foods_count/$',
        LoadFoodsCountView.as_view(), name='load_foods_count'),
)