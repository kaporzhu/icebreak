# -*- coding: utf-8 -*-
from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """
    Model form for Order
    """
    class Meta:
        model = Order
        fields = ('delivery_time', 'phone', 'name', 'building', 'zone', 'room',
                  'time_frame')


class CommentForm(forms.Form):
    """
    Form for food comment
    """
    content = forms.CharField(required=False)
    rating = forms.IntegerField()
