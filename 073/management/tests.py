from django.test import TestCase
from .models import generate_appointment_number


class AppointmentNumberTest(TestCase):
    def test_generate_appointment_number(self):
        number = generate_appointment_number()
        self.assertTrue(number.startswith('AP'))
        self.assertEqual(len(number), 16)
        print(f"生成的预约单号: {number}")
