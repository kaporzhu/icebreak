# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CheckoutView, CreateView, MineView, OrderDetailView
)


urlpatterns = patterns(
    '',
    url(r'^mine/$', MineView.as_view(), name='mine'),
    url(r'^create/$', CreateView.as_view(), name='create'),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^(?P<code>\d+)/$', OrderDetailView.as_view(), name='detail'),
)
