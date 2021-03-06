"""Test cases for Zinnia's quick entry"""
from django.test import TestCase
from django.contrib.auth.models import User

from zinnia.models import Entry


class QuickEntryTestCase(TestCase):
    """Test cases for quick_entry view"""
    urls = 'zinnia.tests.urls'

    def test_quick_entry(self):
        User.objects.create_user('user', 'user@example.com', 'password')
        User.objects.create_superuser('admin', 'admin@example.com', 'password')

        response = self.client.get('/quick_entry/', follow=True)
        self.assertEquals(response.redirect_chain,
                          [('http://testserver/accounts/login/?next=/quick_entry/', 302)])
        self.client.login(username='user', password='password')
        response = self.client.get('/quick_entry/', follow=True)
        self.assertEquals(response.redirect_chain,
                          [('http://testserver/accounts/login/?next=/quick_entry/', 302)])
        self.client.logout()
        self.client.login(username='admin', password='password')
        response = self.client.get('/quick_entry/', follow=True)
        self.assertEquals(response.redirect_chain,
                          [('http://testserver/admin/zinnia/entry/add/', 302)])
        response = self.client.post('/quick_entry/', {'title': 'test'}, follow=True)
        self.assertEquals(response.redirect_chain,
                          [('http://testserver/admin/zinnia/entry/add/?tags=&title=test&sites=1&content=%3Cp%3E%3C%2Fp%3E&authors=2&slug=test', 302)])
        response = self.client.post('/quick_entry/', {'title': 'test', 'tags': 'test',
                                                      'content': 'Test content'}, follow=True)
        entry = Entry.objects.get(title='test')
        self.assertEquals(response.redirect_chain,
                          [('http://testserver%s' % entry.get_absolute_url(), 302)])
