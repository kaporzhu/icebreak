# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from braces.views import(
    SuperuserRequiredMixin, SetHeadlineMixin
)

from .mixins import FoodMixin
from .models import Food, CookingStep


class CreateFoodView(SuperuserRequiredMixin, SetHeadlineMixin, CreateView):
    """
    Create new Food
    """
    model = Food
    headline = u'添加新菜品'
    success_url = reverse_lazy('foods:list')


class UpdateFoodView(SuperuserRequiredMixin, SetHeadlineMixin, UpdateView):
    """
    Update Food info
    """
    model = Food
    headline = u'更新菜品信息'
    success_url = reverse_lazy('foods:list')


class FoodDetailView(SuperuserRequiredMixin, DetailView):
    """
    Food detail page
    """
    model = Food


class FoodListView(SuperuserRequiredMixin, ListView):
    """
    Display all Food for admin
    """
    model = Food


class CreateCookingStepView(SuperuserRequiredMixin, SetHeadlineMixin, FoodMixin,
                            CreateView):
    """
    Create new cooking step
    """
    model = CookingStep
    headline = u'添加步骤'

    def get_initial(self):
        """
        Initial data for form
        """
        return {'food': self.food}

    def get_success_url(self):
        return reverse_lazy('foods:detail', kwargs={'pk': self.food.id})


class UpdateCookingStepView(SuperuserRequiredMixin, SetHeadlineMixin, FoodMixin,
                            UpdateView):
    """
    Update cooking step info
    """
    model = CookingStep
    headline = u'更新步骤信息'

    def get_success_url(self):
        return reverse_lazy('foods:detail', kwargs={'pk': self.food.id})
