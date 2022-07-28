from django.test import TestCase
from django.contrib.auth.models import User
from .models import Manager, Equipment


class ManagerTests(TestCase):
    """Проверка создания модели 'менеджер'."""

    @classmethod
    def setUpTestData(cls):
        testuser1 = User.objects.create_user(username='testuser1', password='abc123')
        testuser1.save()

        test_manager = Manager.objects.create(name='Test Manager', phone=1234567,
                                              email='test@mail.ru')
        test_manager.save()

    def test_manager(self):
        manager = Manager.objects.get(id=1)
        name = f'{manager.name}'
        phone = f'{manager.phone}'
        email = f'{manager.email}'
        self.assertEqual(name, 'Test Manager')
        self.assertEqual(phone, '1234567')
        self.assertEqual(email, 'test@mail.ru')


class EquipmentTest(TestCase):
    """Проверка создания модели 'оборудование'."""

    @classmethod
    def setUpTestData(cls):
        testuser1 = User.objects.create_user(username='testuser1', password='abc123')
        testuser1.save()

        test_equipment = Equipment.objects.create(name='Test_Equipment')
        test_equipment.save()

    def test_equipment(self):
        equipment = Equipment.objects.get(id=1)
        name = f'{equipment.name}'
        self.assertEqual(name, 'Test_Equipment')
