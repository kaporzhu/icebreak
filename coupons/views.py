# -*- coding: utf-8 -*-
import string
from datetime import datetime

from django.db.models import Q
from django.utils.crypto import get_random_string
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from braces.views import(
    LoginRequiredMixin, AjaxResponseMixin, JsonRequestResponseMixin,
    StaffuserRequiredMixin
)

from .forms import CreateCouponForm
from .models import Coupon


class ValidateView(LoginRequiredMixin, AjaxResponseMixin,
                   JsonRequestResponseMixin, View):
    """
    Validate coupon code
    """
    def get_ajax(self, request, *args, **kwargs):
        """
        Check coupon code
        """
        code = request.REQUEST['code']
        result = {}
        try:
            coupon = Coupon.objects.get(code=code)
            if coupon.is_used:
                result['active'] = False
                result['reason'] = u'优惠码已经在{}被使用'.format(datetime.now().strftime('%m-%d %H:%M'))  # noqa
            else:
                result['active'] = True
                result['discount'] = coupon.discount
        except Coupon.DoesNotExist:
            result['active'] = False
            result['reason'] = u'优惠码不存在'

        return self.render_json_response(result)


class CouponCreateView(StaffuserRequiredMixin, FormView):
    """
    Create coupon code
    """
    form_class = CreateCouponForm
    template_name = 'coupons/create.html'

    def form_valid(self, form):
        """
        Generate code
        """
        amount = int(form.data['amount'])
        discount = float(form.data['discount'])
        codes = []
        for i in range(amount):
            coupon = Coupon(discount=discount,
                            expired_at=datetime.now(),
                            code=get_random_string(9, string.digits))
            coupon.save()
            codes.append(coupon.code_format)
        return self.render_to_response(
            self.get_context_data(codes='\n'.join(codes), form=form))


class CouponListView(StaffuserRequiredMixin, ListView):
    """
    Display all the coupons
    """
    model = Coupon
    paginate_by = 50

    def get_queryset(self):
        """
        Filter coupons
        """
        qs = super(CouponListView, self).get_queryset()

        # code
        code = self.request.REQUEST.get('code')
        if code:
            code_Q = Q(code=code)
        else:
            code_Q = Q()

        # status
        status = self.request.REQUEST.get('status', all)
        if status == 'all':
            status_Q = Q()
        else:
            status_Q = Q(is_used=True if status=='true' else False)

        return qs.filter(code_Q, status_Q).order_by('-id')

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(CouponListView, self).get_context_data(**kwargs)
        data.update(self.request.GET.dict())
        return data
