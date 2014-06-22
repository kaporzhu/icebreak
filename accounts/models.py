# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from buildings.models import Building, Zone, Room
from shops.models import Shop


class Staff(models.Model):
    """
    Staff model
    """
    user = models.OneToOneField(User)
    is_deliveryman = models.BooleanField()
    is_shop_manager = models.BooleanField()
    shop = models.ForeignKey(Shop)
    created_at = models.DateTimeField(auto_now_add=True)


class Address(models.Model):
    """
    User address
    """
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=16)
    name = models.CharField(max_length=128)
    building = models.ForeignKey(Building)
    zone = models.ForeignKey(Zone, blank=True, null=True)
    room = models.ForeignKey(Room)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        address = self.building.name
        if self.building.is_multiple:
            address += self.zone.name
        address += self.room.number
        return address
