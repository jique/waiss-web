from django.core.exceptions import ValidationError
from django.test import TestCase

from waiss.apps.models import PositiveDecimalField


class PositiveDecimalFieldTests(TestCase):
    def test_negative_value(self):
        field = PositiveDecimalField(max_digits=4, decimal_places=2)
        msg = "%s is not positive."
        tests = [
            "-1.3",
            "-0.23",
        ]
        for value in tests:
            with self.subTest(value):
                with self.assertRaisesMessage(ValidationError, msg % (value,)):
                    field.clean(value, None)