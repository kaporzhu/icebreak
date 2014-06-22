# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from shops.models import Shop


class Coupon(models.Model):
    """
    Coupon
    """
    code = models.CharField(max_length=16, unique=True)
    discount = models.FloatField()
    shop = models.ForeignKey(Shop, blank=True, null=True)
    expired_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    used_by = models.ForeignKey(User, blank=True, null=True)
    used_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, related_name='shop_coupons', blank=True,
                                null=True)

    @property
    def code_format(self):
        return '{}-{}-{}'.format(self.code[:3], self.code[3:6], self.code[6:])
