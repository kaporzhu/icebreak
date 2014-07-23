# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Building, Zone, Room


admin.site.register(Building)
admin.site.register(Zone)
admin.site.register(Room)
