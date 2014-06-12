# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    CreateBuildingView, UpdateBuildingView, BuildingListView, CreateZoneView,
    UpdateZoneView, CreateRoomView, UpdateRoomView, DeleteRoomView,
    RoomListView, RoomsChartView
)


urlpatterns = patterns(
    '',
    url(r'^create/$', CreateBuildingView.as_view(), name='create'),
    url(r'^list/$', BuildingListView.as_view(), name='list'),
    url(r'^update/(?P<pk>\d+)/$', UpdateBuildingView.as_view(), name='update'),

    url(r'^(?P<building_pk>\d+)/zones/create/$',
        CreateZoneView.as_view(), name='create_zone'),
    url(r'^(?P<building_pk>\d+)/zones/(?P<pk>\d+)/update/$',
        UpdateZoneView.as_view(), name='update_zone'),

    url(r'^(?P<building_pk>\d+)/(?:zones/(?P<zone_pk>\d+)/)?rooms/create/$',
        CreateRoomView.as_view(), name='create_room'),
    url(r'^(?P<building_pk>\d+)/(?:zones/(?P<zone_pk>\d+)/)?rooms/list/$',
        RoomListView.as_view(), name='room_list'),
    url(r'^(?P<building_pk>\d+)/(?:zones/(?P<zone_pk>\d+)/)?rooms/(?P<pk>\d+)/update/$',  # noqa
        UpdateRoomView.as_view(), name='update_room'),
    url(r'^(?P<building_pk>\d+)/(?:zones/(?P<zone_pk>\d+)/)?rooms/(?P<pk>\d+)/delete/$',  # noqa
        DeleteRoomView.as_view(), name='delete_room'),

    url(r'^(?P<building_pk>\d+)/(?:zones/(?P<zone_pk>\d+)/)?rooms/chart/$',
        RoomsChartView.as_view(), name='rooms_chart'),
)
