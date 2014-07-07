# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreateFoodView, UpdateFoodView, FoodListView, FoodDetailView,
    CreateCookingStepView, UpdateCookingStepView, LoadStepsView,
    LoadCommentsView, ShopFoodListView, UpdateCountTodayView, UpdateStatusView,
    TimeFrameView, CreateTimeFrameView, UpdateTimeFrameView
)


urlpatterns = patterns(
    '',
    url(r'^create/$', CreateFoodView.as_view(), name='create'),
    url(r'^list/$', FoodListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', FoodDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', UpdateFoodView.as_view(), name='update'),
    url(r'^load_steps/$', LoadStepsView.as_view(), name='load_steps'),
    url(r'^load_comments/$', LoadCommentsView.as_view(), name='load_comments'),
    url(r'^shop_list/$', ShopFoodListView.as_view(), name='shop_list'),
    url(r'^time_frame/$', TimeFrameView.as_view(), name='time_frame'),
    url(r'^time_frame/create/$',
        CreateTimeFrameView.as_view(), name='create_time_frame'),
    url(r'^time_frame/(?P<pk>\d+)/update/$',
        UpdateTimeFrameView.as_view(), name='update_time_frame'),
    url(r'^update_count_today/$',
        UpdateCountTodayView.as_view(), name='update_count_today'),
    url(r'^update_status/$', UpdateStatusView.as_view(), name='update_status'),

    url(r'^(?P<food_pk>\d+)/steps/create/$',
        CreateCookingStepView.as_view(), name='create_step'),
    url(r'^(?P<food_pk>\d+)/steps/(?P<pk>\d+)/update/$',
        UpdateCookingStepView.as_view(), name='update_step'),
)
