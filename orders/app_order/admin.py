from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin

from .models import Customer, Equipment, Manager, Order, PaymentType, ProductType

import csv
import datetime
from django.http import HttpResponse

from django.utils.safestring import mark_safe
from django.urls import reverse


class OrderAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget)

    class Meta:
        model = Order
        fields = '__all__'


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phoneNumber')


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Customer)
class CastomerAdmit(admin.ModelAdmin):
    list_display = ('name', 'email', 'phoneNumber')


# экспорт данных в csv файл
def export_to_csv(modeladmin, request, queryset):
    """Генерация csv файла."""
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={opts.verbose_name}.csv'
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields()]
    # заголовки колонок
    header = []
    for field in fields:
        header.append(field.verbose_name)
    writer.writerow(header)
    # запись данных в колонки
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Экспорт в файл CSV'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_order', 'year', 'customer', 'product_type', 'circulation',
                    'equipment', 'date_of_acceptance_of_the_order', 'date_of_delivery_of_the_order',
                    'manager', 'the_amount_of_the_deal', 'the_date_of_payment', 'payment_type',
                    'hypperlink', 'readiness', 'completeness', 'order_pdf')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('manager', 'date_of_acceptance_of_the_order', 'customer', 'equipment',
                   'product_type')
    list_editable = ('manager', 'readiness', 'completeness')
    save_on_top = True
    form = OrderAdminForm
    actions = [export_to_csv]

    def order_pdf(self, obj):
        return mark_safe('<a href="{}">PDF</a>'.format(
            reverse('app_order:admin_order_pdf', args=[obj.id])))

    order_pdf.short_description = 'Печать'
