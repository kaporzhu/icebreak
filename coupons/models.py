# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class Coupon(models.Model):
    """
    Coupon
    """
    code = models.CharField(max_length=16, unique=True)
    discount = models.FloatField()
    expired_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    used_by = models.ForeignKey(User, blank=True, null=True)
    used_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
