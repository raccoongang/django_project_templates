from paved import *
from paved.django import *
from paver.easy import *
from paved.django import manage
#
__path__ = path(__file__).abspath().dirname()
#
options.paved.django.manage_py = './manage.py'
options.paved.django.settings = '{{ project_name }}.settings'
