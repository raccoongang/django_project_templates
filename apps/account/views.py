from django.conf import settings
from django.utils.translation import ungettext, ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import is_password_usable
from django.contrib.sites.models import Site
from django.contrib import messages
from django.contrib.auth import (logout, login as auth_login, update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import (TemplateView, UpdateView, FormView, RedirectView, DetailView, View)

from registration.backends.default.views import ActivationView
from social.backends.utils import load_backends

from apps.account.forms import ProfileForm, EmailChangeForm, CurrentPasswordChangeForm
from apps.account.models import EmailChange, Account
from apps.account.utils import generate_key
from learnee.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, DetailView):
    context_object_name = 'account'
    template_name = 'account/profile.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        data = super(ProfileView, self).get_context_data(**kwargs)
        full_url = ''.join(['http://', get_current_site(self.request).domain])
        data.update({
            'full_url': full_url,
        })
        return data


def logout_view(request):
    logout(request)
    return redirect('home')


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name='next',
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Okay, security check complete. Log the user in.
            auth_login(request, form.get_user())

            return HttpResponse('')
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='account/password_settings.html',
                    password_change_form=CurrentPasswordChangeForm):
    post_change_redirect = reverse_lazy('account:profile-settings')
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            messages.success(request, _("Password has been changed"))
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'is_password_usable': is_password_usable(request.user.password)
    }
    return TemplateResponse(request, template_name, context)





class ProfileSettingsView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile-settings')
    template_name = 'account/profile_settings.html'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        super_valid = super(ProfileSettingsView, self).form_valid(form)
        messages.success(self.request, _("Profile has been saved"))
        return super_valid

    def get_context_data(self, **kwargs):
        data = super(ProfileSettingsView, self).get_context_data(**kwargs)
        data.update({'available_backends': load_backends(settings.AUTHENTICATION_BACKENDS)})
        return data


class EmailSettingsView(LoginRequiredMixin, FormView):
    form_class = EmailChangeForm
    success_url = reverse_lazy('account:profile-settings')
    template_name = 'account/email_settings.html'

    def get_form_kwargs(self):
        kwargs = super(EmailSettingsView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        super_valid = super(EmailSettingsView, self).form_valid(form)
        email = form.cleaned_data.get('email')
        email_change = self.save_email_change(email)
        self.send_mail(email_change)
        return super_valid

    def save_email_change(self, email):
        verification_key = generate_key(self.request.user.username, email)

        # Clean all email change made by this user
        qs = EmailChange.objects.filter(user=self.request.user)
        qs.delete()
        return EmailChange.objects.create(user = self.request.user,
                                          verification_key = verification_key,
                                          email = email)

    def send_mail(self, email_change):
        current_site = Site.objects.get_current()
        context = {
            'site': current_site,
            'verification_key': email_change.verification_key,
        }
        subject = render_to_string('send_mail/activation_email_subject.html')
        message = render_to_string('send_mail/activation_email.html',
                                   context=context)
        send_mail(subject, message, None, [email_change.email])
        messages.success(self.request, _("Check you email"))


class EmailVerifyView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('account:profile-settings')
    permanent = False

    def get(self, request, *args, **kwargs):
        get_redirect = super(EmailVerifyView, self).get(request, *args, **kwargs)
        email_change = get_object_or_404(EmailChange, verification_key=kwargs.get('verification_key'))

        if request.user != email_change.user:
            raise Http404()

        # Replace the user's email with the new email
        request.user.email = email_change.email
        request.user.save()
        email_change.delete()
        messages.success(self.request, _('Email successfuly changed to {0}.').format(request.user.email))
        return get_redirect


class CustomActivationView(ActivationView):

    def get_success_url(self, request, user):
        messages.success(request,_("You have activate your account"))
        return ('account:profile-settings', (), {})


class RequireEmailView(TemplateView):
    template_name = 'account/require_email.html'

    def dispatch(self, request, *args, **kwargs):
        self.backend = kwargs.get('backend')
        return super(RequireEmailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(RequireEmailView, self).get_context_data(**kwargs)
        data.update({'backend': self.backend})
        return data


def send_validation(strategy, backend, code):
    url = '{0}?verification_code={1}'.format(
        reverse('social:complete', args=(backend.name,)),
        code.code
    )
    url = strategy.request.build_absolute_uri(url)

    subject = render_to_string('send_mail/send_validation_email_subject.txt')
    message = render_to_string('send_mail/send_validation_activation_email.txt', context={'url': url})
    send_mail(subject, message, None, [code.email])


class EmailSentView(TemplateView):
    template_name = 'account/email_sent.html'
