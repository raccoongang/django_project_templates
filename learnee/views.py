import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from tagging.models import Tag
from apps.account.models import Account
from learnee.mixins import LoginRequiredMixin


def home(request):
    return render(request, 'index.html')


class Search(LoginRequiredMixin, TemplateView):
    template_name = 'search.html'

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(*kwargs)
        context.update({
            'account': self.request.user
        })
        return context


def tag_list(request):
    if request.is_ajax():
        search = request.GET.get('q')
        account_id = request.GET.get('account_id')
        tag_ids = []

        if account_id:
            account = get_object_or_404(Account, id=int(account_id))
            tag_ids += list(Tag.objects.get_for_object(account).values_list('id', flat=True))

        tags = Tag.objects.exclude(id__in=tag_ids).filter(name__icontains=search).values('id', 'name')

        return HttpResponse(json.dumps({'items': list(tags)}),
                            content_type='application/json')
