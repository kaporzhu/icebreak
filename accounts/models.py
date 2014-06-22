# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from buildings.models import Building, Zone, Room


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
