# -*- coding: utf-8 -*-
from django import forms

from .models import TimeFrame


class TimeFrameForm(forms.ModelForm):
    """
    Model form for TimeFrame
    """
    class Meta:
        model = TimeFrame
        exclude = ('shop',)
