# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from braces.views import(
    JsonRequestResponseMixin, LoginRequiredMixin
)

from .forms import OrderForm
from accounts.models import Address
from buildings.models import Building
from foods.models import Food
from orders.models import OrderFood, Order


class CheckoutView(TemplateView):
    """
    Checkout selected foods
    """
    template_name = 'orders/checkout.html'

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(CheckoutView, self).get_context_data(**kwargs)
        data.update({'buildings': Building.objects.all()})

        return data


class CreateView(LoginRequiredMixin, JsonRequestResponseMixin, FormView):
    """
    Create order view
    """
    form_class = OrderForm

    def form_valid(self, form):
        """
        Create order
        """
        order = form.save(commit=False)
        order.user = self.request.user
        order.phone = order.user.username
        order.total_price = 0
        order.save()

        # address
        try:
            address = self.request.user.address
        except Address.DoesNotExist:
            address = Address(user=self.request.user)
        address.phone = order.phone
        address.name = order.name
        address.building = order.building
        address.zone = order.zone
        address.room = order.room
        address.save()

        # foods
        total_price = 0
        for fd in json.loads(self.request.POST['foods']):
            if fd['count'] <= 0:
                continue
            food = Food.objects.get(pk=fd['id'])
            total_price += food.price * fd['count']
            OrderFood(user=self.request.user, food=food, price=food.price,
                      order=order, count=fd['count']).save()

        order.total_price = total_price
        order.save()

        if self.request.is_ajax():
            return self.render_json_response(
                {'success': True, 'next_url': reverse('orders:mine')})


class MineView(LoginRequiredMixin, ListView):
    """
    All my orders
    """
    model = Order

    def get_queryset(self):
        """
        Filter by user
        """
        qs = super(MineView, self).get_queryset()
        return qs.filter(user=self.request.user)
