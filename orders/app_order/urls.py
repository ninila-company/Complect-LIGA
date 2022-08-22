from django.urls import path

from . import views
from .views import OrderDetailView, OrdersView, FilterOrdersView, Search, LoginUser, logout_user


app_name = 'order'
urlpatterns = [
    path('', OrdersView.as_view(), name='order_list'),
    path('<int:id>/<slug:slug>/', OrderDetailView.as_view(), name='order_detail'),
    path('admin/app_order/order/', views.OrdersView.as_view(), name='admin_order'),
    path('filter/', FilterOrdersView.as_view(), name='filter'),
    path('search/', Search.as_view(), name='search'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
]
