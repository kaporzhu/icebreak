# -*- coding: utf-8 -*-
import json
from datetime import datetime

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http.response import HttpResponseForbidden
from django.views.generic.base import TemplateView, View, RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from braces.views import(
    JsonRequestResponseMixin, LoginRequiredMixin, StaffuserRequiredMixin,
    AjaxResponseMixin, JSONResponseMixin, SuperuserRequiredMixin
)

from .constants import(
    ON_THE_WAY, PACKING_DONE, PAID, DELIVERY_TIMES, DISTRIBUTING, DONE,
    PRINTED
)
from .forms import OrderForm, CommentForm
from .models import OrderFood, Order
from accounts.mixins import ShopManagerRequiredMixin
from accounts.models import Address
from buildings.models import Building
from coupons.models import Coupon
from foods.models import Food, FoodComment
from icebreak.mixins import AppRequestMixin
from shops.models import Shop


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


class PayOrderView(LoginRequiredMixin, RedirectView):
    """
    Pay the order
    """
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """
        Fake payment. Update order status here.
        """
        order = Order.objects.get(code=kwargs['code'])
        order.status = PAID
        order.paid_at = datetime.now()
        order.save()

        for order_food in order.orderfood_set.all():
            order_food.food.sales += order_food.count
            order_food.food.save()

        return reverse('orders:detail', kwargs={'code': kwargs['code']})


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
        order.shop = order.building.shop
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
            food.count_today -= fd['count']
            food.save()
            order.shop.update_food_count(food)  # update food count today
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

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(MineView, self).get_context_data(**kwargs)
        data.update({'DISTRIBUTING': DISTRIBUTING})
        return data


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    Order detail page
    """
    slug_field = 'code'
    slug_url_kwarg = 'code'
    model = Order

    def get_context_data(self, **kwargs):
        """
        Add extra data to context
        """
        data = super(OrderDetailView, self).get_context_data(**kwargs)
        data.update({'DISTRIBUTING': DISTRIBUTING, 'DONE': DONE})
        return data


class OrderListView(SuperuserRequiredMixin, ListView):
    """
    All orders for the superuser
    """
    model = Order

    def get_queryset(self):
        """
        Filter the orders
        """
        qs = super(OrderListView, self).get_queryset()

        # shop
        shop = self.request.GET.get('shop', 'all')
        if shop == 'all':
            shop_Q = Q()
        else:
            shop_Q = Q(shop=Shop.objects.get(pk=shop))

        # today's order only
        now = datetime.now()
        start_str = self.request.GET.get('start', now.strftime('%Y-%m-%d'))
        end_str = self.request.GET.get('end', now.strftime('%Y-%m-%d'))
        start = datetime.strptime(start_str, '%Y-%m-%d')
        end = datetime.strptime(end_str, '%Y-%m-%d')
        time_Q = Q(created_at__range=(
            datetime(start.year, start.month, start.day, 0, 0),
            datetime(end.year, end.month, end.day, 23, 59)))

        # status
        status = self.request.GET.get('status', 'all')
        if status == 'all':
            status_Q = Q()
        else:
            status_Q = Q(status=status)

        return qs.filter(shop_Q, status_Q, time_Q).order_by('-id')

    def get_context_data(self, **kwargs):
        """
        Add extra data
        """
        data = super(OrderListView, self).get_context_data(**kwargs)
        data.update({
            'shops': Shop.objects.all(),
            'STATUS_CHOICES': Order.STATUS_CHOICES
        })
        data.update(self.request.GET.dict())

        now = datetime.now()
        if not self.request.GET.get('start'):
            data.update({'start': now.strftime('%Y-%m-%d')})
        if not self.request.GET.get('end'):
            data.update({'end': now.strftime('%Y-%m-%d')})

        return data


class ShopOrderListView(StaffuserRequiredMixin, ShopManagerRequiredMixin,
                        ListView):
    """
    All orders for current shop
    """
    model = Order
    template_name = 'orders/shop_order_list.html'

    def get_queryset(self):
        """
        Filter the orders
        """
        qs = super(ShopOrderListView, self).get_queryset()

        shop_Q = Q(shop=self.staff.shop)

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

        return qs.filter(shop_Q, status_Q, building_Q, time_Q).filter(delivery_time_Q).order_by('-id')  # noqa

    def get_context_data(self, **kwargs):
        """
        Add extra data
        """
        data = super(ShopOrderListView, self).get_context_data(**kwargs)
        data.update({
            'buildings': self.request.user.staff.shop.building_set.all(),
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


class PrintOrdersView(StaffuserRequiredMixin, TemplateView):
    """
    Print selected orders and update the status to PRINTED
    """
    template_name = 'orders/print_order.html'

    def get_context_data(self, **kwargs):
        """
        Get orders from ids
        """
        data = super(PrintOrdersView, self).get_context_data(**kwargs)
        ids = self.request.GET['ids'].split(',')
        orders = []
        for order in Order.objects.in_bulk(ids).values():
            if order.status == PAID:
                orders.append(order)
                order.status = PRINTED
                order.save()
        data.update({'orders': orders})
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
            if order.status in [PAID, PRINTED, PACKING_DONE]:
                order.status = status
                order.save()
        return self.render_json_response({
            'success': True,
            'status_label': order.get_status_display(),
            'status_color': order.status_color
        })


class AppGetOrdersView(AppRequestMixin, JSONResponseMixin, View):
    """
    Get orders by building
    """
    def get(self, request, *args, **kwargs):
        building = Building.objects.get(pk=request.REQUEST['building_id'])
        now = datetime.now()
        start = datetime(now.year, now.month, now.day, 0, 0)
        end = datetime(now.year, now.month, now.day, 23, 59)
        statuses = [PACKING_DONE, ON_THE_WAY, DISTRIBUTING]
        orders = building.order_set.filter(status__in=statuses).filter(created_at__range=(start, end))  # noqa
        orders_json = []
        for order in orders:
            orders_json.append({
                'id': order.id,
                'delivery_time': order.delivery_time,
                'status': order.status,
                'phone': order.phone,
                'name': order.name,
                'zone': order.zone.id if order.zone else -1,
                'floor': order.room.floor,
                'number': order.room.number,
                'address': order.short_address
            })
        return self.render_json_response(orders_json)


class AppFinishOrderView(AppRequestMixin, JSONResponseMixin, View):
    """
    Update order status to DONE
    """
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=request.GET['order_id'])
        order.status = DONE
        order.save()
        order.building.update_order_status_in_whole(order)
        return self.render_json_response({'success': True})


class CommentView(FormView):
    """
    Comment food.
    QRCode will be on the meal box. The user can scan will weixin and
    do a quick feedback.
    """
    template_name = 'orders/comment.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        """
        Add extra data to the context
        """
        data = super(CommentView, self).get_context_data(**kwargs)
        order_food = OrderFood.objects.get(code=self.kwargs['code'])
        data.update({'order_food': order_food})
        return data

    def form_valid(self, form):
        """
        Save the comment
        """
        data = form.cleaned_data
        order_food = OrderFood.objects.get(code=self.kwargs['code'])
        FoodComment(food=order_food.food,
                    address=order_food.user.address,
                    rating=data['rating'],
                    content=data.get('content')).save()
        context = self.get_context_data(form=form)
        context.update({'show_thanks': True})
        return self.render_to_response(context)


class AppBatchStatusUpdateView(AppRequestMixin, JSONResponseMixin, View):
    """
    View for update order status in batch
    """
    def get(self, request, *args, **kwargs):
        status = request.GET['status']
        building = Building.objects.get(pk=request.GET['building_id'])
        if status == ON_THE_WAY:
            orders = Order.objects.filter(building=building,
                                          status=PACKING_DONE)
            orders.update(status=ON_THE_WAY, delivery_man=self.staff)
        elif status == DISTRIBUTING:
            orders = Order.objects.filter(building=building, status=ON_THE_WAY)
            orders.update(status=DISTRIBUTING)
            building.whole_with_orders(refersh=True)
        return self.render_json_response({'success': True})
