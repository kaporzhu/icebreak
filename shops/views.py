# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from braces.views import(
    SuperuserRequiredMixin, SetHeadlineMixin
)

from .models import Shop


class CreateShopView(SuperuserRequiredMixin, SetHeadlineMixin, CreateView):
    """
    Create new shop
    """
    model = Shop
    headline = u'添加新店'
    success_url = reverse_lazy('shops:list')


class UpdateShopView(SuperuserRequiredMixin, SetHeadlineMixin, UpdateView):
    """
    Update shop info
    """
    model = Shop
    headline = u'更新店面信息'
    success_url = reverse_lazy('shops:list')


class ShopListView(SuperuserRequiredMixin, ListView):
    """
    Display all shops for admin
    """
    model = Shop
