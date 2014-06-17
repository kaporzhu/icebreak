# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView

from foods.models import Food


class HomeView(TemplateView):
    """
    Web site home page
    """
    template_name = 'portals/home.html'

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(HomeView, self).get_context_data(**kwargs)
        data.update({'foods': Food.objects.filter(is_active=True)})
        return data
