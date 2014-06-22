# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import(
    ValidateUserView, SendValidationCodeView, ValidateCodeView
)


urlpatterns = patterns(
    '',
    url(r'^validate_user/$',
        ValidateUserView.as_view(), name='validate_user'),
    url(r'^send_validation_code/$',
        SendValidationCodeView.as_view(), name='send_validation_code'),
    url(r'^validate_code/$',
        ValidateCodeView.as_view(), name='validate_code'),
)
