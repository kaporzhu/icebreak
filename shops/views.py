# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from braces.views import(
    SuperuserRequiredMixin, SetHeadlineMixin, AjaxResponseMixin,
    JSONResponseMixin
)

from .models import Shop


class ShopHomeView(TemplateView):
    """
    Shop home page
    """
    template_name = 'shops/home.html'

    def get_context_data(self, **kwargs):
        """
        Add shop and shop foods to the context
        """
        data = super(ShopHomeView, self).get_context_data(**kwargs)
        shop = Shop.objects.get(slug=self.kwargs['slug'])
        data.update({
            'shop': shop,
            'foods': shop.food_set.filter(is_active=True)
        })
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
