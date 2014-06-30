# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreateFoodView, UpdateFoodView, FoodListView, FoodDetailView,
    CreateCookingStepView, UpdateCookingStepView, LoadStepsView,
    LoadCommentsView
)


urlpatterns = patterns(
    '',
    url(r'^create/$', CreateFoodView.as_view(), name='create'),
    url(r'^list/$', FoodListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', FoodDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', UpdateFoodView.as_view(), name='update'),
    url(r'^load_steps/$', LoadStepsView.as_view(), name='load_steps'),
    url(r'^load_comments/$', LoadCommentsView.as_view(), name='load_comments'),

    url(r'^(?P<food_pk>\d+)/steps/create/$',
        CreateCookingStepView.as_view(), name='create_step'),
    url(r'^(?P<food_pk>\d+)/steps/(?P<pk>\d+)/update/$',
        UpdateCookingStepView.as_view(), name='update_step'),
)
