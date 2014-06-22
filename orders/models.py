# -*- coding: utf-8 -*-
import string
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string

from .constants import(
    UNPAID, PAID, PACKING_DONE, ON_THE_WAY, DISTRIBUTING, DONE
)
from buildings.models import Building, Zone, Room
from coupons.models import Coupon
from foods.models import Food


class Order(models.Model):
    """
    Order model
    """
    STATUS_CHOICES = (
        (UNPAID, u'等待付款'),
        (PAID, u'已付款'),
        (PACKING_DONE, u'打包完成'),
        (ON_THE_WAY, u'配送途中'),
        (DISTRIBUTING, u'正在写字楼中配送'),
        (DONE, u'完成'),
    )
    code = models.CharField(max_length=32, unique=True, blank=True, null=True)
    user = models.ForeignKey(User)
    total_price = models.FloatField()
    coupon = models.ForeignKey(Coupon, blank=True, null=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES,
                              default=UNPAID, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # address info
    phone = models.CharField(max_length=16)
    name = models.CharField(max_length=128)
    building = models.ForeignKey(Building)
    zone = models.ForeignKey(Zone, blank=True, null=True)
    room = models.ForeignKey(Room)

    @property
    def address(self):
        if self.zone:
            return u'{} {} {}'.format(self.building, self.zone, self.room)
        else:
            return u'{} {}'.format(self.building, self.room)


class OrderFood(models.Model):
    """
    Food for order
    """
    food = models.ForeignKey(Food)
    order = models.ForeignKey(Order)
    user = models.ForeignKey(User)
    count = models.SmallIntegerField()
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal_price(self):
        return self.price * self.count


def generate_order_code(sender, instance, created, *args, **kwargs):
    """
    Generate order code
    """
    if created:
        instance.code = u'600{}{}{}'.format(
            instance.user.id,
            datetime.now().strftime('%y%m%d'),
            get_random_string(8, string.digits))
        instance.save(using=False)


post_save.connect(generate_order_code, Order)
