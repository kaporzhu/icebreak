# -*- coding: utf-8 -*-
import re

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache

from .constants import VALIDATION_CODE_PREFIX

from .models import Staff


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

        if code != settings.MASTER_KEY and code not in cache.get(VALIDATION_CODE_PREFIX + phone, []):  # noqa
            raise forms.ValidationError(u'验证码错误')

        return data


class StaffForm(forms.ModelForm):
    """
    Model form for Staff
    """
    is_active = forms.BooleanField(label=u'启用账号', required=False)
    username = forms.CharField(label=u'用户名')
    password = forms.CharField(label=u'密码', required=False)
    name = forms.CharField(label=u'名字')

    class Meta:
        model = Staff
        exclude = ('user','shop', 'api_key')
