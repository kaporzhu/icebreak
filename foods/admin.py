# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Food, CookingStep, FoodComment, TimeFrame


admin.site.register(Food)
admin.site.register(CookingStep)
admin.site.register(FoodComment)
admin.site.register(TimeFrame)
