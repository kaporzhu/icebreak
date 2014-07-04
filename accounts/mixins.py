# -*- coding: utf-8 -*-
from django.http.response import Http404


class ShopManagerRequiredMixin(object):
    """
    If authenticated user is not shop manager, raise error
    """
    def dispatch(self, request, *args, **kwargs):
        staff = request.user.staff
        if not staff.is_shop_manager:
            raise Http404
        self.staff = staff
        return super(ShopManagerRequiredMixin, self).dispatch(request, *args, **kwargs)
