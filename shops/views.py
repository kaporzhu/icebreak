# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.list import ListView

from braces.views import(
    SuperuserRequiredMixin, SetHeadlineMixin, AjaxResponseMixin,
    JSONResponseMixin, StaffuserRequiredMixin
)

from .forms import ShopManagementForm
from .models import Shop
from accounts.mixins import ShopManagerRequiredMixin


class ShopHomeView(TemplateView):
    """
    Shop home page
    """
    template_name = 'shops/home.html'

    def get_template_names(self):
        """
        If the shop is closed, display the close board page
        """
        if self.shop.is_closed:
            return 'shops/close_board.html'
        else:
            return super(ShopHomeView, self).get_template_names()

    def get_context_data(self, **kwargs):
        """
        Add shop and shop foods to the context
        """
        data = super(ShopHomeView, self).get_context_data(**kwargs)
        self.shop = Shop.objects.get(slug=self.kwargs['slug'])
        data.update({'shop': self.shop})
        return data


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


class ShopDetailView(SuperuserRequiredMixin, DetailView):
    """
    Shop detail page
    """
    model = Shop


class LoadFoodsCountView(AjaxResponseMixin, JSONResponseMixin, View):
    """
    Load foods count for the shop
    """
    def get_ajax(self, request, *args, **kwargs):
        shop =Shop.objects.get(id=request.GET['id'])
        return self.render_json_response(shop.foods_count())


class ShopManagementView(StaffuserRequiredMixin, ShopManagerRequiredMixin,
                         FormView):
    """
    Manage shop.
    Open or close the shop.
    """
    template_name = 'shops/management.html'
    form_class = ShopManagementForm

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(ShopManagementView, self).get_context_data(**kwargs)
        data.update({'shop': self.staff.shop})
        return data

    def form_valid(self, form):
        """
        Update shop
        """
        data = form.cleaned_data
        self.staff.shop.is_closed = not data['is_open']
        self.staff.shop.close_tip = data.get('close_tip')
        self.staff.shop.save()
        return self.render_to_response(self.get_context_data())
