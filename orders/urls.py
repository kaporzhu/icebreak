# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CheckoutView, CreateView, MineView, OrderDetailView, ShopOrderListView,
    UpdateStatusView, OrderListView
)


urlpatterns = patterns(
    '',
    url(r'^shop_list/$', ShopOrderListView.as_view(), name='shop_list'),
    url(r'^list/$', OrderListView.as_view(), name='list'),
    url(r'^mine/$', MineView.as_view(), name='mine'),
    url(r'^create/$', CreateView.as_view(), name='create'),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^(?P<code>\d+)/$', OrderDetailView.as_view(), name='detail'),
    url(r'^update_status/$', UpdateStatusView.as_view(), name='update_status'),
)
