from django.shortcuts import render, get_object_or_404

from .models import Order


def order_list(request):
    """Список заказов."""
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'app_order/orders_list.html', context)


def order_detail(request, id, slug):
    """Детали заказа."""
    order = get_object_or_404(Order, id=id, slug=slug)
    context = {'order': order}
    return render(request, 'app_order/order_detail.html', context)
