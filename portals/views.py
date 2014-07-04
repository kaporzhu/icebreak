# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView

from shops.models import Shop


class HomeView(RedirectView):
    """
    Web site home page
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Return shop home page
        """
        return reverse('shops:home',
                       kwargs={'slug': Shop.objects.first().slug})
