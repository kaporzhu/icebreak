# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from braces.views import(
    SuperuserRequiredMixin, SetHeadlineMixin, AjaxResponseMixin,
    JSONResponseMixin, StaffuserRequiredMixin
)
from easy_thumbnails.files import get_thumbnailer

from .mixins import FoodMixin
from .models import Food, CookingStep
from accounts.mixins import ShopManagerRequiredMixin


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


class LoadStepsView(AjaxResponseMixin, JSONResponseMixin, View):
    """
    Load steps for the food
    """
    def get_ajax(self, request, *args, **kwargs):
        """
        Load now
        """
        food = Food.objects.get(pk=request.GET['id'])
        steps_json = []
        options = {'size': (100, 100), 'crop': True}
        for step in food.cookingstep_set.all().order_by('index'):
            steps_json.append({
                'description': step.description,
                'image': get_thumbnailer(step.image).get_thumbnail(options).url
            })
        return self.render_json_response(steps_json)


class LoadCommentsView(AjaxResponseMixin, JSONResponseMixin, View):
    """
    Load comments for the food
    """

    page_size = 1

    def get_ajax(self, request, *args, **kwargs):
        """
        Load now
        """
        food = Food.objects.get(pk=request.GET['id'])
        page = int(request.GET.get('page', '1'))
        comments_json = []
        for comment in food.foodcomment_set.all().order_by('-id')[(page-1)*self.page_size: page*self.page_size]:
            comments_json.append({
                'content': comment.content,
                'building': comment.address.building.name,
                'name': comment.address.name,
                'rating': comment.rating,
                'created_at': comment.created_at.strftime('%m-%d %H:%M')
            })
        return self.render_json_response(comments_json)


class ShopFoodListView(StaffuserRequiredMixin, ShopManagerRequiredMixin,
                       ListView):
    """
    Display all the foods in the shop
    """
    model = Food
    template_name = 'foods/shop_food_list.html'

    def get_queryset(self):
        """
        Filter the foods
        """
        qs = super(ShopFoodListView, self).get_queryset()
        return qs.filter(shop=self.staff.shop)


class UpdateCountTodayView(StaffuserRequiredMixin, ShopManagerRequiredMixin,
                           AjaxResponseMixin, JSONResponseMixin, View):
    """
    Update food count today
    """
    def get_ajax(self, request, *args, **kwargs):
        food = self.staff.shop.food_set.get(pk=request.GET['id'])
        food.count_today = request.GET['count']
        food.save()
        self.staff.shop.update_food_count(food)
        return self.render_json_response({'success': True})


class UpdateStatusView(StaffuserRequiredMixin, ShopManagerRequiredMixin,
                       AjaxResponseMixin, JSONResponseMixin, View):
    """
    Activate or disable the food
    """
    def get_ajax(self, request, *args, **kwargs):
        food = self.staff.shop.food_set.get(pk=request.GET['id'])
        food.is_active = not food.is_active
        food.save()
        return self.render_json_response({'success': True, 'is_active': food.is_active})
