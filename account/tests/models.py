__author__ = 'xahgmah'

from django.test import TestCase, RequestFactory
from account.models import Account, EmailChange
from django.core.urlresolvers import reverse


class AccountTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'mypassword'
        self.user = Account.objects.create_superuser(
            self.username,
            'myemail@test.com',
            self.password
        )

    def test_full_name(self):
        result = self.user.full_name()
        self.assertEqual(type(result), str)
