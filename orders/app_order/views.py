# from django.db.models import Q
# from django.shortcuts import render
# from django.views.generic.base import View
from django.views.generic import DetailView, ListView

from .models import Order, Manager


class Managers:
    """Менаджеры."""

    def get_managers(self):
        return Manager.objects.all()


class OrdersView(Managers, ListView):
    model = Order
    queryset = Order.objects.order_by('completeness', 'date_of_delivery_of_the_order')
    template_name = 'app_order/orders_list.html'


class OrderDetailView(Managers, DetailView):
    """Детали заказа."""

    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        return context


class FilterOrdersView(Managers, ListView):
    """Фильтрация заказов."""

    template_name = 'app_order/orders_list.html'

    def get_queryset(self):
        queryset = Order.objects.filter(manager__name__in=self.request.GET.getlist('name'))
        return queryset


class Search(ListView):
    """Поиск."""

    template_name = 'app_order/orders_list.html'

    def get_queryset(self):
        queryset = Order.objects.filter(name__icontains=self.request.GET.get('q').title())
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get('q')
        return context
