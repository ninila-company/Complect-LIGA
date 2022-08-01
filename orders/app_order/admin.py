from django.contrib import admin

from .models import Customer, Equipment, Manager, Order, PaymentType


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phoneNumber')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Customer)
class CastomerAdmit(admin.ModelAdmin):
    list_display = ('name', 'email', 'phoneNumber')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_order', 'year', 'customer', 'circulation', 'equipment',
                    'date_of_acceptance_of_the_order', 'date_of_delivery_of_the_order', 'manager',
                    'the_amount_of_the_deal', 'the_date_of_payment', 'payment_type', 'hypperlink',
                    'readiness')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name', 'manager',)
    list_editable = ('manager', 'readiness')
