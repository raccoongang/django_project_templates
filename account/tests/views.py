__author__ = 'xahgmah'

from django.test import TestCase, RequestFactory, Client
from account.models import Account
from account import views
from django.core.urlresolvers import reverse


# class LogoutTestCase(TestCase):
#     def setUp(self):
#         self.username = 'test'
#         self.password = 'mypassword'
#         self.user = Account.objects.create_superuser(
#             self.username,
#             'myemail@test.com',
#             self.password
#         )
#
#     def test_logout(self):
#         c = Client()
#         c.login(username=self.username, password=self.password)
#         response = c.get(reverse('logout'))
#         self.assertEqual(response.status_code, 200)
#         self.assertNotIn('_auth_user_id', c.session)
#
#     def tearDown(self):
#         self.user.delete()
#
#
# class LoginTestCase(TestCase):
#     def setUp(self):
#         self.username = 'test'
#         self.password = 'mypassword'
#         self.user = Account.objects.create_superuser(
#             self.username,
#             'myemail@test.com',
#             self.password
#         )
#
#     def test_login(self):
#         c = Client()
#         response = c.post(reverse('login'), {
#             'username': self.username,
#             'password': self.password,
#         })
#         self.assertEqual(response.status_code, 302)
#         self.assertIn('_auth_user_id', c.session)
#
#     def test_wrong_user_login(self):
#         c = Client()
#         response = c.post(reverse('login'), {
#             'username': 'wrong',
#             'password': 'wrong'
#         })
#         self.assertEqual(response.status_code, 200)
#         self.assertGreater(len(response.context_data['form'].errors), 0)
#
#     def tearDown(self):
#         self.user.delete()
#
#
# class PasswordChangeTestCase(TestCase):
#     def setUp(self):
#         self.username = 'test'
#         self.password = 'mypassword'
#         self.new_passwrord = 'newpassword'
#         self.user = Account.objects.create_superuser(
#             self.username,
#             'myemail@test.com',
#             self.password
#         )
#
#     def test_password_change(self):
#         c = Client()
#         c.login(username=self.username, password=self.password)
#         response = c.post(reverse('account:password-settings',current_app='account'), {
#             'old_password': self.password,
#             'new_password1': self.new_passwrord,
#             'new_password2': self.new_passwrord
#         })
#         # self.assertEqual(response.status_code, 200)
#         self.assertTrue(
#             Account.objects.get(username=self.username).check_password(
#                 self.new_passwrord))
#
#     def tearDown(self):
#         self.user.delete()

class ProfileSettingsTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'mypassword'
        self.new_passwrord = 'newpassword'
        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'bdate': 'first_name',
            'first_name': 'first_name',
            'first_name': 'first_name'
        }
        self.user = Account.objects.create_superuser(
            self.username,
            'myemail@test.com',
            self.password
        )