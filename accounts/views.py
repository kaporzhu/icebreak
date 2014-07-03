# -*- coding: utf-8 -*-
import re
import string

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import View, RedirectView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.utils.crypto import get_random_string

from braces.views import(
    AjaxResponseMixin, JsonRequestResponseMixin, SuperuserRequiredMixin,
    JSONResponseMixin
)

from .constants import VALIDATION_CODE_PREFIX, VALIDATION_CODE_COUNT_PREFIX
from .forms import PhoneLoginForm, StaffForm
from .models import Address, Staff
from icebreak.utils import send_sms
from shops.models import Shop


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
        if not re.match('^1[3-9]\d{9}$', phone):
            return self.render_json_response(
                {'success': False, 'reason': u'手机号码不对，请检查一下'})
        code_count_today = cache.get(VALIDATION_CODE_COUNT_PREFIX + phone, 0)
        if (code_count_today > 10):
            return self.render_json_response(
                {'success': False, 'reason': u'您今天发送验证码的次数已经超出限制'})

        codes = cache.get(VALIDATION_CODE_PREFIX + phone, [])
        new_code = get_random_string(4, string.digits)
        send_sms(phone,
                 settings.SMS_TEMPLATES['validation_code'].format(new_code))
        codes.append(new_code)
        cache.set(VALIDATION_CODE_PREFIX + phone, codes, 1800)
        cache.set(VALIDATION_CODE_COUNT_PREFIX + phone, len(codes), 43200)

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
        if code in cache.get(VALIDATION_CODE_PREFIX + phone, []):  # noqa
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


class PhoneLoginView(FormView):
    """
    Allow the user to login with phone
    """
    template_name = 'accounts/phone_login.html'
    form_class = PhoneLoginForm
    success_url = reverse_lazy('portals:home')

    def form_valid(self, form):
        """
        Login the user here
        """
        user = User.objects.get(username=form.cleaned_data['phone'])
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(self.request, user)
        return super(PhoneLoginView, self).form_valid(form)


class AppLoginView(JSONResponseMixin, View):
    """
    Login from mobile app. Auth with username and password.
    Return api key when success.
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Auth staff user.
        """
        user = auth.authenticate(username=request.REQUEST['username'],
                                 password=request.REQUEST['password'])
        if user:
            return self.render_json_response({
                'success': True,
                'api_key': user.staff.api_key,
                'staff_id': user.staff.id
            })
        else:
            return self.render_json_response({'success': False})


class LogoutView(RedirectView):
    """
    Logout current user and redirect to sign in page
    """
    permanent = False
    url = reverse_lazy('portals:home')

    def get(self, request, *args, **kwargs):
        """
        Logout here
        """
        auth.logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class AddStaffView(SuperuserRequiredMixin, CreateView):
    """
    Add new staff for the shop
    """
    model = Staff
    form_class = StaffForm

    def form_valid(self, form):
        """
        Create new staff
        """
        shop = Shop.objects.get(pk=self.request.GET['shop_id'])
        user = User(username=form.data['username'], first_name=form.data['name'])
        user.is_staff = True
        user.is_active = form.data['is_active']
        user.set_password(form.data['password'])
        user.save()
        staff = form.save(commit=False)
        staff.user = user
        staff.shop = shop
        staff.save()
        return super(AddStaffView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('shops:detail',
                            kwargs={'pk': self.request.GET['shop_id']})


class UpdateStaffView(SuperuserRequiredMixin, UpdateView):
    """
    Update staff info
    """
    model = Staff
    form_class = StaffForm

    def get_initial(self):
        """
        Add extra initial data to the form
        """
        initial = super(UpdateStaffView, self).get_initial()
        initial.update({
            'is_active': self.object.user.is_active,
            'username': self.object.user.username,
            'name': self.object.user.get_full_name()
        })
        return initial

    def form_valid(self, form):
        """
        Update staff info
        """
        form.save()
        self.object.user.username = form.data['username']
        self.object.user.name = form.data['name']
        self.object.user.is_active = form.data['is_active']
        self.object.user.save()
        return super(UpdateStaffView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('shops:detail',
                            kwargs={'pk': self.object.shop.id})
