# -*- coding: utf-8 -*-
from django.db import models


class Shop(models.Model):
    """
    Shop model.
    Each shop covers about 3 office buildings.
    """
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    phone = models.CharField(max_length=16, blank=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    open_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name
