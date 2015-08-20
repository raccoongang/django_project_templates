from urllib import urlopen
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import redirect

from social.pipeline.partial import partial
from social.exceptions import InvalidEmail


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get('ajax') or user and user.email:
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
            details['validation'] = True
        else:
            return redirect('account:require_email', kwargs.get('backend').name)


@partial
def mail_validation(backend, details, is_new=False, *args, **kwargs):
    requires_validation = backend.REQUIRES_EMAIL_VALIDATION or \
                          backend.setting('FORCE_EMAIL_VALIDATION', False)
    send_validation = details.get('email') and \
                      (is_new or backend.setting('PASSWORDLESS', False)) and details.get('validation')
    if requires_validation and send_validation:
        data = backend.strategy.request_data()
        if 'verification_code' in data:
            backend.strategy.session_pop('email_validation_address')
            if not backend.strategy.validate_email(details['email'],
                                           data['verification_code']):
                raise InvalidEmail(backend)
        else:
            backend.strategy.send_email_validation(backend, details['email'])
            backend.strategy.session_set('email_validation_address',
                                         details['email'])
            return backend.strategy.redirect(
                backend.strategy.setting('EMAIL_VALIDATION_URL')
            )

@partial
def save_profile_picture_and_profile_url(backend, user, response, *args, **kwargs):
    if user is None or not response:
        return

    image_url = None
    profile_url = None

    if backend.name == 'vk-oauth2':
        image_url = response.get('photo_100')
        profile_url = 'https://vk.com/id{}'.format(response.get('uid'))
        user.vkontakte = profile_url
    elif backend.name == 'facebook':
        image_url = 'http://graph.facebook.com/{0}/picture?type=normal'.format(response['id'])
        profile_url = response.get('link')
        user.facebook = profile_url
    elif backend.name == 'odnoklassniki-oauth2':
        image_url = response.get('pic_2')
        if 'stub' in image_url: # No real image
            image_url = None
        profile_url = 'http://ok.ru/profile/{}'.format(response.get('uid'))
        user.odnoklassniki = profile_url
    elif backend.name == 'linkedin-oauth2':
        image_url = response.get('pictureUrl')
        profile_url = response.get('publicProfileUrl')
        user.linkedin = profile_url

    if profile_url:
        user.save()

    if image_url and not user.avatar:
        try:
            image_content = urlopen(image_url)
            image_name = default_storage.get_available_name(user.avatar.field.upload_to + '/' + str(user.id) + '.' + image_content.headers.subtype)
            user.avatar.save(image_name, ContentFile(image_content.read()))
            user.save()
        except Exception:
            pass


@partial
def disconnect(backend, user, *args, **kwargs):
    if user is None or not backend:
        return

    if backend.name == 'vk-oauth2':
        user.vkontakte = None
    elif backend.name == 'facebook':
        user.facebook = None
    elif backend.name == 'odnoklassniki-oauth2':
        user.odnoklassniki = None
    elif backend.name == 'linkedin-oauth2':
        user.linkedin = None

    user.save()
    return
