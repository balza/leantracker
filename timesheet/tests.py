from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

class CreateTimesheetViewTests(TestCase):
    def test_insert_timesheet(self):
        """
        Provided a validated TimesheetForm must create an entry in Timesheet table and an entry in TimesheetEntry table for each day 
        inserted with != 0 value
        """
        csrf_client = Client(enforce_csrf_checks=True)
        response = self.client.get(reverse('timesheet:create'))
