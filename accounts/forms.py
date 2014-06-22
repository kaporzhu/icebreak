# -*- coding: utf-8 -*-
import re

from django import forms
from django.core.cache import cache

from .constants import VALIDATION_CODE_PREFIX
from django.contrib.auth.models import User


class PhoneLoginForm(forms.Form):
    """
    Form for user login with phone
    """
    phone = forms.CharField(label=u'手机号')
    code = forms.CharField(label=u'验证码')

    def clean_phone(self):
        """
        Check phone number
        """
        phone = self.data.get('phone')
        if not re.match('^1[3-9]\d{9}$', phone):
            raise forms.ValidationError(u'无效的手机号码')

        return phone

    def clean(self):
        """
        Check phone and validation code
        """
        data = self.data
        phone = data.get('phone')
        code = data.get('code')
        if not User.objects.filter(username=phone).exists():
            raise forms.ValidationError(u'这个手机号还没下过单')

        if code not in cache.get(VALIDATION_CODE_PREFIX + phone, []):
            raise forms.ValidationError(u'验证码错误')

        return data
