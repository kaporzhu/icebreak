# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

from buildings.models import Building, Zone, Room
from shops.models import Shop
from django.utils.crypto import get_random_string


class Staff(models.Model):
    """
    Staff model
    """
    user = models.OneToOneField(User)
    is_deliveryman = models.BooleanField()
    is_shop_manager = models.BooleanField()
    shop = models.ForeignKey(Shop)
    api_key = models.CharField(max_length=16, blank=True, null=True)
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


def create_api_key(sender, instance, **kwargs):
    """
    A signal for hooking up automatic ``ApiKey`` creation.
    """
    if kwargs.get('created') is True:
        instance.api_key = get_random_string(16)
        instance.save(using=False)


post_save.connect(create_api_key, sender=Staff)
