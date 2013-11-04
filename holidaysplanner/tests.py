from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from holidaysplanner.views import get_user_groups, get_users_in_groups


class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user2 = User.objects.create_user('paul', 'paul@thebeatles.com', 'paulpassword')
        self.g1 = Group.objects.create(name="aGroup1")
        self.g2 = Group.objects.create(name="aGroup2")

    def test_get_user_groups1(self):
        self.g1.user_set.add(self.user1)
        groups = get_user_groups(self.user1)
        self.assertEqual(1, len(groups))

    def test_get_user_groups2(self):
        self.g1.user_set.add(self.user1)
        self.g2.user_set.add(self.user1)
        groups = get_user_groups(self.user1)
        self.assertEqual(2, len(groups))

    def test_get_users_in_groups(self):
        self.g1.user_set.add(self.user1)
        self.g1.user_set.add(self.user2)
        users = get_users_in_groups(self.g1)
        self.assertEqual(2, len(users))
