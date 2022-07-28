from datetime import date

from django.db import models


class Manager(models.Model):
    """Менеджер."""

    name = models.CharField('Ф.И.О.', max_length=200, db_index=True)
    phone = models.PositiveIntegerField('Номер телефона')
    email = models.EmailField('Почта', max_length=254)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

    def __str__(self):
        return self.name


class Equipment(models.Model):
    """Оборудование."""

    name = models.CharField('Название оборудования', max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'

    def __str__(self):
        return self.name


class PaymentType(models.Model):
    """Способ оплаты."""

    name = models.CharField('Вид платежа', max_length=100)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Вид платежа'
        verbose_name_plural = 'Виды платежей'

    def __str__(self):
        return self.name


class Order(models.Model):
    """Заказ."""

    number_order = models.PositiveSmallIntegerField('Номер заказа')
    name = models.CharField('Название заказа', max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    year = models.PositiveSmallIntegerField('Год')
    customer = models.CharField('Заказчик', max_length=200)
    circulation = models.PositiveSmallIntegerField('Тираж')
    equipment = models.ForeignKey(Equipment, 'Название оборудования',
                                  on_delete=models.SET_NULL, null=True)
    date_of_acceptance_of_the_order = models.DateField('Дата принятия заказа',
                                                       default=date.today)
    date_of_delivery_of_the_order = models.DateField('Дата сдачи заказа')
    manager = models.ForeignKey(Manager, 'Менеджер', on_delete=models.SET_NULL,
                                null=True)
    the_amount_of_the_deal = models.DecimalField('Сумма договора', max_digits=20, decimal_places=2)
    the_date_of_payment = models.DateField('Дата оплаты')
    payment_type = models.ForeignKey(PaymentType, 'Вид платежа', on_delete=models.SET_NULL,
                                     null=True)
    readiness = models.BooleanField('Готовность')
    hypperlink = models.CharField('Гипперссылка', max_length=100)

    class Meta:
        ordering = ('-date_of_acceptance_of_the_order',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.name
