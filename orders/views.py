# -*- coding: utf-8 -*-
import json
from datetime import datetime

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http.response import HttpResponseForbidden
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from braces.views import(
    JsonRequestResponseMixin, LoginRequiredMixin, StaffuserRequiredMixin,
    AjaxResponseMixin, JSONResponseMixin
)

from .constants import ON_THE_WAY, PACKING_DONE, PAID, DELIVERY_TIMES
from .forms import OrderForm
from .models import OrderFood, Order
from accounts.models import Address
from buildings.models import Building
from coupons.models import Coupon
from foods.models import Food


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

        # get available delivery times
        delivery_times = []
        now = datetime.now().time()
        for time in DELIVERY_TIMES:
            if time['cutoff_time'] > now:
                delivery_times.append(time)

        data.update({
            'buildings': Building.objects.all(),
            'delivery_times': delivery_times
        })

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

        # coupon
        if self.request.POST.get('coupon'):
            try:
                coupon = Coupon.objects.get(code=self.request.POST['coupon'])
                if not coupon.is_used:
                    coupon.is_used = True
                    coupon.used_by = self.request.user
                    coupon.used_at = datetime.now()
                    coupon.save()
                    order.coupon = coupon
                    order.save()
            except Coupon.DoesNotExist:
                pass

        if self.request.is_ajax():
            return self.render_json_response(
                {'success': True, 'next_url': reverse('orders:mine')})


class MineView(LoginRequiredMixin, ListView):
    """
    All my orders
    """
    model = Order
    template_name = 'orders/mine.html'

    def get_queryset(self):
        """
        Filter by user
        """
        qs = super(MineView, self).get_queryset()
        return qs.filter(user=self.request.user).order_by('-id')[:10]


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    Order detail page
    """
    slug_field = 'code'
    slug_url_kwarg = 'code'
    model = Order


class OrderListView(StaffuserRequiredMixin, ListView):
    """
    All orders for the staff user
    """
    model = Order

    def get_queryset(self):
        """
        Filter the orders
        """
        qs = super(OrderListView, self).get_queryset()

        # today's order only
        now = datetime.now()
        start_str = self.request.GET.get('start', now.strftime('%Y-%m-%d'))
        end_str = self.request.GET.get('end', now.strftime('%Y-%m-%d'))
        start = datetime.strptime(start_str, '%Y-%m-%d')
        end = datetime.strptime(end_str, '%Y-%m-%d')
        time_Q = Q(created_at__range=(
            datetime(start.year, start.month, start.day, 0, 0),
            datetime(end.year, end.month, end.day, 23, 59)))

        # building
        building = self.request.GET.get('building', 'all')
        if building == 'all':
            building_Q = Q()
        else:
            building_Q = Q(building=Building.objects.get(pk=building))

        # status
        status = self.request.GET.get('status', 'all')
        if status == 'all':
            status_Q = Q()
        else:
            status_Q = Q(status=status)

        # delivery time
        delivery_time = self.request.GET.get('delivery_time', 'all')
        if delivery_time == 'all':
            delivery_time_Q = Q()
        else:
            delivery_time_Q = Q(delivery_time=delivery_time)

        return qs.filter(status_Q, building_Q, time_Q).filter(delivery_time_Q).order_by('-id')  # noqa

    def get_context_data(self, **kwargs):
        """
        Add extra data
        """
        data = super(OrderListView, self).get_context_data(**kwargs)
        data.update({
            'buildings': Building.objects.all(),
            'STATUS_CHOICES': Order.STATUS_CHOICES,
            'staff_statuses': [PACKING_DONE, ON_THE_WAY],
            'delivery_times': DELIVERY_TIMES
        })
        data.update(self.request.GET.dict())

        now = datetime.now()
        if not self.request.GET.get('start'):
            data.update({'start': now.strftime('%Y-%m-%d')})
        if not self.request.GET.get('end'):
            data.update({'end': now.strftime('%Y-%m-%d')})

        return data


class UpdateStatusView(StaffuserRequiredMixin, AjaxResponseMixin,
                       JSONResponseMixin, View):
    """
    Update order status
    """
    def get_ajax(self, request, *args, **kwargs):
        """
        Update status for orders and return the new status color
        """
        status = request.GET['status']
        if status not in [PACKING_DONE, ON_THE_WAY]:
            return HttpResponseForbidden()
        for order in Order.objects.in_bulk(request.GET['ids'].split(',')).values():  # noqa
            if order.status in [PAID, PACKING_DONE, ON_THE_WAY]:
                order.status = status
                order.save()
        return self.render_json_response({
            'success': True,
            'status_label': order.get_status_display(),
            'status_color': order.status_color
        })
