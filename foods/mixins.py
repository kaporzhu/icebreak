# -*- coding: utf-8 -*-
from .models import Food


class FoodMixin(object):
    """
    Mixin for foods app views
    """

    def dispatch(self, request, *args, **kwargs):
        """
        If food_pk is existed, set food to current object.
        """
        if kwargs.get('food_pk'):
            self.food = Food.objects.get(pk=kwargs['food_pk'])
        return super(FoodMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add food to the context
        """
        data = super(FoodMixin, self).get_context_data(**kwargs)
        if hasattr(self, 'food'):
            data.update({'food': self.food})

        return data
