# -*- coding: utf-8 -*-
from django import template
from django.forms.widgets import CheckboxInput, RadioInput
from django.template.base import TemplateSyntaxError, Node


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
        return '*' + s[1:]


class RangeNode(Node):
    def __init__(self, num, context_name):
        self.num, self.context_name = num, context_name
    def render(self, context):
        num = template.Variable(self.num).resolve(context)
        context[self.context_name] = range(int(num))
        return ""


@register.tag
def num_range(parser, token):
    """
    Takes a number and iterates and returns a range (list) that can be 
    iterated through in templates

    Syntax:
    {% num_range 5 as some_range %}

    {% for i in some_range %}
      {{ i }}: Something I want to repeat\n
    {% endfor %}

    Produces:
    0: Something I want to repeat 
    1: Something I want to repeat 
    2: Something I want to repeat 
    3: Something I want to repeat 
    4: Something I want to repeat
    """
    try:
        fnctn, num, trash, context_name = token.split_contents()
    except ValueError:
        raise TemplateSyntaxError, '%s takes the syntax %s number_to_iterate\
            as context_variable' % (fnctn, fnctn)
    if not trash == 'as':
        raise TemplateSyntaxError, '%s takes the syntax %s number_to_iterate\
            as context_variable' % (fnctn, fnctn)
    return RangeNode(num, context_name)
