# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Order, OrderFood


admin.site.register(Order)
admin.site.register(OrderFood)
