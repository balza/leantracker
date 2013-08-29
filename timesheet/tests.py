from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from leantracker.timesheet.forms import TimesheetForm, first_day_of_the_week
from django.shortcuts import render_to_response
from datetime import datetime, date

class CreateTimesheetViewTests(TestCase):
    def test_create_timesheet(self):
        """
        Provided a validated TimesheetForm must create an entry in Timesheet table and an entry in TimesheetEntry table for each day 
        inserted with != 0 value
        """
        post_data = {
                'form-TOTAL_FORMS': u'1',
                'form-INITIAL_FORMS': u'0',
                'form-MAX_NUM_FORMS': u'',
                'form-0-project': u'Test',
                'form-0-tue': u'8',
        }
#        csrf_client = Client(enforce_csrf_checks=True)
        response = self.client.post(reverse('timesheet:create'), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'timesheet/timesheet_form.html')
        #self.assertQuerysetEqual(
        #    response.context['latest_poll_list'],
        #    ['<Poll: Past poll.>']
        #)

class FormTests(TestCase):
    def test_first_day_of_this_week(self):
        today = date(2013, 8, 29)
        aspected_result = date(2013, 8, 26)
        self.assertEqual(aspected_result,first_day_of_this_week(today))
        
