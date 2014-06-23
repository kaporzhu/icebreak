# -*- coding: utf-8 -*-
from django import forms


class CreateCouponForm(forms.Form):
    """
    Form for create new coupon
    """
    amount = forms.IntegerField(label=u'数量')
    discount = forms.FloatField(label=u'优惠(元)')
