from django import template
from friendship.models import Follow

register = template.Library()


@register.filter
def social_backends(backends):
    backends = [(name, backend) for name, backend in backends.items()
                    if name not in ['username', 'email']]
    backends.sort(key=lambda b: b[0])
    return [backends[n:n + 10] for n in range(0, len(backends), 10)]


@register.simple_tag(takes_context=True)
def associated(context, backend):
    user = context.get('user')
    context['association'] = None
    if user and user.is_authenticated():
        try:
            context['association'] = user.social_auth.filter(
                provider=backend.name
            )[0]
        except IndexError:
            pass
    return ''
