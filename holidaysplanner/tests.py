from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from leantracker.holidaysplanner.views import get_user_groups


class ViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        Group.objects.create("aGroup")
        g = Group.objects.get(name='aGroup')
        g.user_set.add(self.user)


    def test_get_user_groups(self):
        groups = get_user_groups(self.user)
        self.assertEqual(1, groups.size())
