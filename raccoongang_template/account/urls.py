from django.conf.urls import url

from account import views

urlpatterns = [
    url(r'^activate/(?P<activation_key>\w+)/$', views.CustomActivationView.as_view(), name='registration_activate'),
    url(r'^register/$', views.CustomRegistrationView.as_view(),
                           name='registration_register'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^login/$', views.login, name='login'),
    url(r'^$', views.ProfileSettingsView.as_view(), name='profile-settings'),
    url(r'^settings/email/$', views.EmailSettingsView.as_view(), name='email-settings'),
    url(r'^settings/email/verify/(?P<verification_key>\w+)/$', views.EmailVerifyView.as_view(), name='email-verify'),
    url(r'^settings/password/$', views.password_change, name='password-settings'),
    url(r'^require_email/(?P<backend>[^/]+)/$', views.RequireEmailView.as_view(), name='require_email'),
    url(r'^email_sent/$', views.EmailSentView.as_view(), name='email-sent'),
]
