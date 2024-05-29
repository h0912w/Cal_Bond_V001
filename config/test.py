import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.test import TestCase


class DefaultTest(TestCase):
    def test(self):
        self.assertEquals(1, 1)
