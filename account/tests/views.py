__author__ = 'xahgmah'

from django.test import TestCase, RequestFactory, Client
from django.core import mail
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm
from account.models import Account, EmailChange
from account.forms import EmailChangeForm, ProfileForm, \
    CurrentPasswordChangeForm, PasswordChangeForm


class LogoutTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'mypassword'
        self.user = Account.objects.create_superuser(
            self.username,
            'myemail@test.com',
            self.password
        )

    def test_logout(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        response = c.get(reverse('account:logout'))
        self.assertNotIn('_auth_user_id', c.session)

    def tearDown(self):
        self.user.delete()


class LoginTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'mypassword'
        self.user = Account.objects.create_superuser(
            self.username,
            'myemail@test.com',
            self.password
        )

    def test_show_form(self):
        c = Client()
        response = c.get(reverse('account:login'))
        self.assertIn('form', response.context_data)
        self.assertIsInstance(response.context_data['form'],
                              AuthenticationForm)

    def test_login(self):
        c = Client()
        response = c.post(reverse('account:login'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', c.session)

    def test_wrong_user_login(self):
        c = Client()
        response = c.post(reverse('account:login'), {
            'username': 'wrong',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context_data['form'].errors), 0)

    def test_try_login_with_authenticated_user(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        response = c.post(reverse('account:login'), {
            'username': 'wrong',
            'password': 'wrong'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            response.url.endswith(reverse('account:profile-settings')))

    def tearDown(self):
        self.user.delete()


class PasswordChangeTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'mypassword'
        self.new_passwrord = 'newpassword'
        self.user = Account.objects.create_superuser(
            self.username,
            'myemail@test.com',
            self.password
        )

    def test_show_form(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        response = c.get(reverse('account:password-settings'))
        self.assertIn('form', response.context_data)
        self.assertIsInstance(response.context_data['form'],
                              CurrentPasswordChangeForm)

    def test_wrong_old_password(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        response = c.post(reverse('account:password-settings'), {
            'old_password': 'wrong',
            'new_password1': self.new_passwrord,
            'new_password2': self.new_passwrord
        })
        self.assertGreater(len(response.context_data['form'].errors), 0)


    def test_password_change(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        response = c.post(reverse('account:password-settings'), {
            'old_password': self.password,
            'new_password1': self.new_passwrord,
            'new_password2': self.new_passwrord
        })
        self.assertTrue(
            Account.objects.get(username=self.username).check_password(
                self.new_passwrord))

    def tearDown(self):
        self.user.delete()


class ProfileSettingsTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'mypassword'
        self.new_passwrord = 'newpassword'
        data = {
            'username': 'test',
            'first_name': 'first name',
            'last_name': 'last name',
            'bdate': '2015-09-22',
            'my_site': 'http://site.my',
            'description': 'description',
            'skype': 'skype',
            'country': 'country',
            'city': 'city'
        }
        self.new_data = {
            'username': 'newusername',
            'first_name': 'new first name',
            'last_name': 'new last name',
            'bdate': '22.09.2014',
            'my_site': 'http://newsite.my',
            'description': 'new description',
            'skype': 'new skype',
            'country': 'new country',
            'city': 'new city'
        }
        self.user = Account.objects.create_superuser(
            self.username,
            'myemail@test.com',
            self.password
        )
        models = Account.objects.filter(pk=self.user.pk)
        models.update(**data)

    def test_update_profiles(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        response = c.post(reverse('account:profile-settings'), self.new_data)
        self.new_data['bdate'] = '2014-09-22'
        self.user = Account.objects.get(username=self.new_data['username'])
        self.assertDictEqual(self.new_data, {
            'username': str(self.user.username),
            'first_name': str(self.user.first_name),
            'last_name': str(self.user.last_name),
            'bdate': str(self.user.bdate),
            'my_site': str(self.user.my_site),
            'description': str(self.user.description),
            'skype': str(self.user.skype),
            'country': str(self.user.country),
            'city': str(self.user.city)
        })

    def tearDown(self):
        self.user.delete()


class EmailSettingsTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'mypassword'
        self.newemail = 'new@email.com'
        self.user = Account.objects.create_superuser(
            self.username,
            'myemail@test.com',
            self.password
        )
        mail.outbox = []

    def test_change_with_wrong_password(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        response = c.post(reverse('account:email-settings'), {
            'email': self.newemail,
            'password': 'wrong',
        })
        self.assertGreater(len(response.context_data['form'].errors), 0)

    def test_change_to_similar_email(self):
        c = Client()
        c.login(username=self.username, password=self.password)
        response = c.post(reverse('account:email-settings'), {
            'email': 'myemail@test.com',
            'password': self.password,
        })
        self.assertGreater(len(response.context_data['form'].errors), 0)

    def test_password_change(self):
        c1 = Client()
        c1.login(username=self.username, password=self.password)
        c1.post(reverse('account:email-settings'), {
            'email': self.newemail,
            'password': self.password,
        })
        self.assertGreater(len(mail.outbox), 0)
        self.assertIn('settings/email/verify', mail.outbox[0].body)
        emailchange = EmailChange.objects.get(user_id=self.user.pk)
        c2 = Client()
        c2.login(username=self.username, password=self.password)
        c2.get(
            reverse('account:email-verify',
                    args=(emailchange.verification_key,)))
        self.assertEqual(Account.objects.get(username='test').email,
                         self.newemail)

    def test_wrong_user(self):
        user = Account.objects.create_user('wrong', 'wrong@wro.ng', '123123')
        c1 = Client()
        c1.login(username='wrong', password='123123')
        c1.post(reverse('account:email-settings'), {
            'email': 'new@wro.ng',
            'password': '123123',
        })
        emailchange = EmailChange.objects.get(user=user)
        c2 = Client()
        #Login as another user
        c2.login(username=self.username, password=self.password)
        response = c2.get(reverse('account:email-verify',
                       args=(emailchange.verification_key,)))
        self.assertEqual(response.status_code,404)

    def tearDown(self):
        self.user.delete()


class SendValidationTestCase(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'mypassword'
        self.newemail = 'new@email.com'
        self.user = Account.objects.create_superuser(
            self.username,
            'myemail@test.com',
            self.password
        )
        mail.outbox = []

    def test_send_validation(self):
        pass
