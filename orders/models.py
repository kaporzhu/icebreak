# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

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
