# -*- coding: utf-8 -*-
from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """
    Model form for Order
    """
    class Meta:
        model = Order
        exclude = ('user', 'status', 'total_price', 'phone', 'coupon',)
