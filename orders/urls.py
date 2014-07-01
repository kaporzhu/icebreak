# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CheckoutView, CreateView, MineView, OrderDetailView, ShopOrderListView,
    UpdateStatusView, OrderListView, AppGetOrdersView, PrintOrdersView,
    AppFinishOrderView, CommentView, AppBatchStatusUpdateView
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
    url(r'^app_get_orders/$', AppGetOrdersView.as_view()),
    url(r'^app_finish_order/$', AppFinishOrderView.as_view()),
    url(r'^app_batch_status_update/$', AppBatchStatusUpdateView.as_view()),
    url(r'^print_orders/$', PrintOrdersView.as_view(), name='print_orders'),
    url(r'^comment/(?P<code>\w+)/$', CommentView.as_view(), name='comment'),
)
