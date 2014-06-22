# -*- coding: utf-8 -*-
import string

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.cache import cache
from django.views.generic.base import View
from django.utils.crypto import get_random_string

from braces.views import(
    AjaxResponseMixin, JsonRequestResponseMixin
)

from icebreak.utils import send_sms
from accounts.models import Address


class ValidateUserView(AjaxResponseMixin, JsonRequestResponseMixin, View):
    """
    Validate user info.
    """
    def get_ajax(self, request, *args, **kwargs):
        """
        Check if the address with this phone number is existed
        """
        phone = request.REQUEST['phone']
        validate_required = True
        try:
            user = User.objects.get(username=phone)
            # check address info
            try:
                if str(user.address.room.id) == request.REQUEST['room']:
                    validate_required = False
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth.login(request, user)
            except Address.DoesNotExist:
                pass
        except User.DoesNotExist:
            pass
        return self.render_json_response(
            {'validate_required': validate_required})


class SendValidationCodeView(AjaxResponseMixin, JsonRequestResponseMixin,
                             View):
    """
    Send validation code to the cell phone.
    """
    def get_ajax(self, request, *args, **kwargs):
        """
        Send code
        """
        phone = request.REQUEST['phone']
        code_count_today = cache.get(u'code_count_{}'.format(phone), 0)
        if (code_count_today > 10):
            return self.render_json_response(
                {'success': False, 'reason': u'您今天发送验证码的次数已经超出限制'})

        codes = cache.get(u'codes_{}'.format(phone), [])
        new_code = get_random_string(6, string.digits)
        send_sms(phone,
                 settings.SMS_TEMPLATES['validation_code'].format(new_code))
        codes.append(new_code)
        cache.set(u'codes_{}'.format(phone), codes, 1800)
        cache.set(u'code_count_{}'.format(phone), len(codes), 43200)

        return self.render_json_response({'success': True})


class ValidateCodeView(AjaxResponseMixin, JsonRequestResponseMixin, View):
    """
    Validate code
    """
    def get_ajax(self, request, *args, **kwargs):
        """
        Validate code here
        """
        code = request.REQUEST['code']
        phone = request.REQUEST['phone']
        if code in cache.get(u'codes_{}'.format(phone), []):
            # if phone is new, create User for it and login
            try:
                user = User.objects.get(username=phone)
            except User.DoesNotExist:
                user = User(username=phone)
                user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            return self.render_json_response({'success': True})
        else:
            return self.render_json_response({'success': False})
