from django.shortcuts import render

from .models import Order


def order_list(request):
    """Список заказов."""
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'app_order/orders_list.html', context)
