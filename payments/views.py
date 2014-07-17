# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.http.response import Http404, HttpResponseForbidden, HttpResponse
from django.views.generic.base import RedirectView, TemplateView, View

from braces.views import(
    LoginRequiredMixin, CsrfExemptMixin
)

from .alipay import Alipay
from .models import Payment
from orders.constants import UNPAID, PAID
from orders.models import Order


class PayView(LoginRequiredMixin, RedirectView):
    """
    Trigger alipay payment request
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Generate alipay request url
        """
        order = Order.objects.get(code=self.request.GET['code'])
        if order.status != UNPAID:
            raise Http404()
        site = get_current_site(self.request)

        alipay = Alipay(pid=settings.ALIPAY_PID, key=settings.ALIPAY_KEY,
                        seller_email=settings.ALIPAY_EMAIL)
        params = {
            'notify_url': u'http://{}{}'.format(site.domain, reverse('payments:notify')),
            'return_url': u'http://{}{}'.format(site.domain, reverse('payments:success')),
            'out_trade_no': order.code,
            'subject': u'担保交易付款',
        }

        params.update({'logistics_type': 'EXPRESS',
                       'logistics_fee': 0,
                       'logistics_payment': 'SELLER_PAY',
                       'price': 0.01,
                       'quantity': 1})

        return alipay.create_partner_trade_by_buyer_url(**params)


class SuccessView(LoginRequiredMixin, TemplateView):
    """
    Payment success.
    return_url for Alipay.
    """
    template_name = 'payments/success.html'

    def get(self, request, *args, **kwargs):
        """
        Verify notify
        """
        alipay = Alipay(pid=settings.ALIPAY_PID, key=settings.ALIPAY_KEY,
                        seller_email=settings.ALIPAY_EMAIL)
        if not alipay.verify_notify(**request.GET.dict()):
            return HttpResponseForbidden()
        code = request.GET['out_trade_no']
        order = Order.objects.get(code=code)
        payment = Payment()
        payment.buyer_id = request.GET.get('buyer_id')
        payment.buyer_email = request.GET.get('buyer_email')
        payment.trade_no = request.GET.get('trade_no')
        payment.trade_status = request.GET.get('trade_status')
        payment.full_content = json.dumps(request.GET.dict())
        payment.order = order
        payment.save()
        if payment.trade_status == 'TRADE_SUCCESS':
            order.status = PAID
            order.save()
        return super(SuccessView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add extra data to the context
        """
        data = super(SuccessView, self).get_context_data(**kwargs)
        code = self.request.GET['out_trade_no']
        order = Order.objects.get(code=code)
        data.update({'order': order, 'PAID': PAID})
        return data


class NotifyView(CsrfExemptMixin, View):
    """
    notify_url for Alipay.
    Alipay will post the payment info to the server.
    Return 'success' to end the Alipay notification.
    """
    def post(self, request, *args, **kwargs):
        """
        Payment notify from alipay
        """
        alipay = Alipay(pid=settings.ALIPAY_PID, key=settings.ALIPAY_KEY,
                        seller_email=settings.ALIPAY_EMAIL)
        if not alipay.verify_notify(**request.POST.dict()):
            return HttpResponseForbidden()
        code = request.POST['out_trade_no']
        order = Order.objects.get(code=code)
        payment = Payment()
        payment.buyer_id = request.POST.get('buyer_id')
        payment.buyer_email = request.POST.get('buyer_email')
        payment.trade_no = request.POST.get('trade_no')
        payment.trade_status = request.POST.get('trade_status')
        payment.full_content = json.dumps(request.POST.dict())
        payment.order = order
        payment.is_notify = True
        payment.save()
        if payment.trade_status == 'TRADE_SUCCESS':
            order.status = PAID
            order.save()
        return HttpResponse('success')
