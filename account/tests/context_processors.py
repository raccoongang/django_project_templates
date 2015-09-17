__author__ = 'xahgmah'

from django.test import TestCase, RequestFactory
from account.context_processors import project_name
from django.core.urlresolvers import reverse


class ContextProcessorsTestCase(TestCase):
    def test_project_name(self):
        factory = RequestFactory()
        request = factory.get(reverse('home'))
        result = project_name(request)
        self.assertEqual(type(result), dict)
        self.assertIn("PROJECT_NAME", result)
