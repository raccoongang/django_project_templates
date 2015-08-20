# -*- coding: utf8 -*-
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import is_password_usable
from apps.account.models import Account


class ProfileForm(forms.ModelForm):
    last_name = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length=255)

    class Meta:
        model = Account
        fields = ['username', 'last_name', 'first_name', 'my_site', 'description', 'skype', 'city', 'country',
                  'university', 'education_level', 'bdate', 'avatar']
        help_texts = {
            'education_level': u'Например: бакалавр, магистр, аспирант...',
        }

class EmailChangeForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(max_length=255)

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if self.user.email == email:
            raise forms.ValidationError(u'Новый адрес электронной почты не может быть такой же как ваш текущий адрес')

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not self.user.check_password(password):
            raise forms.ValidationError(u'Пароль не верный')

        return password


class CurrentPasswordChangeForm(PasswordChangeForm):

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if is_password_usable(self.user.password) and not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password