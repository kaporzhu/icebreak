# -*- coding: utf-8 -*-
from django import forms


class ShopManagementForm(forms.Form):
    """
    Form for manage shop.
    """
    is_open = forms.CharField(required=False)
    close_tip = forms.CharField(required=False)
