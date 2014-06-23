# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    ValidateView, CouponCreateView, CouponListView
)


urlpatterns = patterns(
    '',
    url(r'^create/$', CouponCreateView.as_view(), name='create'),
    url(r'^validate/$', ValidateView.as_view(), name='validate'),
    url(r'^list/$', CouponListView.as_view(), name='list'),
)