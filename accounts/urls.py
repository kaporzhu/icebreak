# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    ValidateUserView, SendValidationCodeView, ValidateCodeView, PhoneLoginView,
    LogoutView, AddStaffView, UpdateStaffView, AppLoginView, StaffHomeView,
    CreateMessageView
)


urlpatterns = patterns(
    '',
    url(r'^login/$', PhoneLoginView.as_view(), name='login'),
    url(r'^app_login/$', AppLoginView.as_view()),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^validate_user/$',
        ValidateUserView.as_view(), name='validate_user'),
    url(r'^send_validation_code/$',
        SendValidationCodeView.as_view(), name='send_validation_code'),
    url(r'^validate_code/$',
        ValidateCodeView.as_view(), name='validate_code'),
    url(r'^add_staff/$', AddStaffView.as_view(), name='add_staff'),
    url(r'^update_staff/(?P<pk>\d+)/$', UpdateStaffView.as_view(), name='update_staff'),
    url(r'^staff/(?P<pk>\d+)/$', StaffHomeView.as_view(), name='staff_home'),
    url(r'^staff/(?P<pk>\d+)/create_message/$', CreateMessageView.as_view(), name='create_message'),
)
