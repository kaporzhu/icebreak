# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Staff, StaffMessage, Address


admin.site.register(Staff)
admin.site.register(StaffMessage)
admin.site.register(Address)
