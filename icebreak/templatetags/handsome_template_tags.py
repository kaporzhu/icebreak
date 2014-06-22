# -*- coding: utf-8 -*-
from django import template
from django.forms.widgets import CheckboxInput, RadioInput


register = template.Library()


@register.filter
def add_attrs(field, attrs_str):
    """
    Add attribute to the html tag.
    Exclude checkbox and radiobox
    """
    # exclude widgets
    exclude_widgets = (CheckboxInput, RadioInput,)
    for widget in exclude_widgets:
        if isinstance(field.field.widget, widget):
            return field.as_widget()

    attrs = {}
    for attr in attrs_str.split(';'):
        attr_name, attr_value = attr.split(':')
        attrs[attr_name] = attr_value
    return field.as_widget(attrs=attrs)


@register.filter
def dim(s):
    """
    Hide some of the chars in this string
    """
    if len(s) > 4:
        return s[:-4] + '**' + s[-2:]
    else:
        return s
