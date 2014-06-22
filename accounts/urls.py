# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    ValidateUserView, SendValidationCodeView, ValidateCodeView, PhoneLoginView,
    LogoutView
)


urlpatterns = patterns(
    '',
    url(r'^login/$', PhoneLoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^validate_user/$',
        ValidateUserView.as_view(), name='validate_user'),
    url(r'^send_validation_code/$',
        SendValidationCodeView.as_view(), name='send_validation_code'),
    url(r'^validate_code/$',
        ValidateCodeView.as_view(), name='validate_code'),
)
