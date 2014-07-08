# -*- coding: utf-8 -*-
from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """
    Model form for Order
    """
    class Meta:
        model = Order
        exclude = ('user', 'status', 'total_price', 'phone', 'coupon', 'shop',
                   'delivery_man', 'discount', 'steps')


class CommentForm(forms.Form):
    """
    Form for food comment
    """
    content = forms.CharField(required=False)
    rating = forms.IntegerField()
