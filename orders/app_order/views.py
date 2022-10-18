import weasyprint
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView

from .forms import LoginUserForm
from .models import Equipment, Manager, Order, ProductType


class Managers:
    """Менаджеры."""

    def get_managers(self):
        return Manager.objects.all()


class Equipments:
    """Оборудование."""

    def get_equipment(self):
        return Equipment.objects.all()


class ProductsType:
    """Типы продукции."""

    def get_type(self):
        return ProductType.objects.all()


class OrdersView(Managers, Equipments, ProductsType, ListView):
    """Заказы."""

    model = Order
    template_name = 'app_order/orders_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        queryset = Order.objects.order_by('completeness', 'date_of_delivery_of_the_order')
        return queryset.select_related('customer',
                                       'manager',
                                       'equipment',
                                       'payment_type',
                                       'product_type')

    def get_total(self):
        """Итоговая сумма."""
        queryset = Order.objects.aggregate(total=Sum('the_amount_of_the_deal'))
        return queryset['total']


class OrderDetailView(DetailView):
    """Детали заказа."""

    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        context['title'] = context['order']
        return context


class FilterOrdersView(Managers, Equipments, ProductsType, ListView):
    """Фильтрация заказов."""

    template_name = 'app_order/orders_list.html'

    def get_queryset(self):
        queryset = Order.objects.filter(
            Q(manager__name__in=self.request.GET.getlist('managerName')) |
            Q(equipment__name__in=self.request.GET.getlist('equipmentName')) |
            Q(product_type__name__in=self.request.GET.getlist('producttypeName'))
        ).order_by('completeness', 'date_of_delivery_of_the_order')
        return queryset.select_related('customer',
                                       'equipment',
                                       'manager',
                                       'payment_type',
                                       'product_type')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Фильтр: "
        return context

    def get_total(self):
        """Итоговая сумма."""
        queryset = Order.objects.filter(
            Q(manager__name__in=self.request.GET.getlist('managerName')) |
            Q(equipment__name__in=self.request.GET.getlist('equipmentName')) |
            Q(product_type__name__in=self.request.GET.getlist('producttypeName'))).aggregate(
                Sum('the_amount_of_the_deal')
            )
        return queryset['the_amount_of_the_deal__sum']


class Search(ListView):
    """Поиск."""

    template_name = 'app_order/orders_list.html'

    def get_queryset(self):
        queryset = Order.objects.filter(name__icontains=self.request.GET.get('q').title())
        return queryset.select_related('customer', 'equipment', 'manager', 'payment_type')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        context['title'] = f"Поиск:{context['q']}"
        return context


class LoginUser(LoginView):
    """Логин."""

    form_class = LoginUserForm
    template_name = 'app_order/login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


def logout_user(request):
    """Выход."""
    logout(request)
    return redirect('/')


def admin_order_pdf(request, order_id):
    """Генерация pdf файла."""
    order = get_object_or_404(Order, id=order_id)
    template_name = 'app_order/pdf.html'
    html = render_to_string(template_name, {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=\"order_{order.id}.pdf"'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                            settings.STATIC_ROOT + 'css/pdf.css')])
    return response
