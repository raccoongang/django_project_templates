import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from tagging.models import Tag
from apps.account.models import Account
from learnee.mixins import LoginRequiredMixin


def home(request):
    return render(request, 'index.html')
