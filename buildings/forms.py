# -*- coding: utf-8 -*-
from django import forms

from .models import Room


class RoomForm(forms.ModelForm):
    """
    Model form for Room
    """
    class Meta:
        model = Room
