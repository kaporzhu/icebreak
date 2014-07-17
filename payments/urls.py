# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    PayView, SuccessView, NotifyView
)


urlpatterns = patterns(
    '',
    url(r'^pay/$', PayView.as_view(), name='pay'),
    url(r'^success/$', SuccessView.as_view(), name='success'),
    url(r'^notify/$', NotifyView.as_view(), name='notify'),
)
