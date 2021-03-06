from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from datetime import date
from django.contrib.auth.models import User

from timesheet.forms import TimesheetForm
from timesheet.models import TimeEntry, Timesheet
from projects.models import Project
from rest_framework.test import APIRequestFactory,APIClient
from timesheet.views import InsertHolidayViewSet
from timesheet.serializers import TimeEntrySerializer


class TimesheetViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.p1 = Project(name="project1", code="pj1")
        self.p1.save()
        self.p2 = Project(name="project2", code="pj2")
        self.p2.save()

    def test_submit_timesheet_post(self):
        """
        Provided a validated TimesheetForm must create an entry in Timesheet table and an entry in TimesheetEntry table for each day
        inserted with != 0 value
        """
        self.client.login(username='john', password='johnpassword')
        post_data = {
            'form-TOTAL_FORMS': u'2',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-project': u'1',
            'form-0-mon': u'0',
            'form-0-tue': u'8',
            'form-0-wed': u'0',
            'form-0-thu': u'0',
            'form-0-fri': u'0',
            'form-0-sat': u'0',
            'form-0-sun': u'0',
            'form-1-project': u'2',
            'form-1-mon': u'0',
            'form-1-tue': u'8',
            'form-1-wed': u'8',
            'form-1-thu': u'0',
            'form-1-fri': u'0',
            'form-1-sat': u'0',
            'form-1-sun': u'0',
            u'submit': [u'Submit timesheet']
        }
        Timesheet.objects.create_timesheet(year=2013, week_number=32, user=self.user)
        response = self.client.post(reverse('timesheet:load', kwargs={'year': 2013, 'week_number': 32}), post_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(3, TimeEntry.objects.count())
        self.assertTemplateUsed(response, 'timesheet/timesheet_list.html')

    def test_load_a_new_timesheet(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('timesheet:load', kwargs={'year': 2013, 'week_number': 32}))
        self.assertEqual(response.status_code, 200)

    def test_load_timesheet(self):
        self.client.login(username='john', password='johnpassword')
        timesheet = Timesheet.objects.create_timesheet(year=2013, week_number=32, user=self.user)
        response = self.client.get(reverse('timesheet:load', kwargs={'year': 2013, 'week_number': 32}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, Timesheet.objects.count())
        self.assertTemplateUsed(response, 'timesheet/timesheet_form.html')
        self.assertEqual(0, timesheet.timeentry_set.count())

    def test_load_an_empty_timesheet_get(self):
        self.client.login(username='john', password='johnpassword')
        timesheet = Timesheet.objects.create_timesheet(year=2013, week_number=32, user=self.user)
        response = self.client.get(reverse('timesheet:load', kwargs={'year': 2013, 'week_number': 32}))
        self.assertEqual(response.status_code, 200)
        #print response.context[-1]['formset']
        self.assertContains(response, 'name="form-0-mon" size="2" type="text" value="0"', 1, 200)
        self.assertContains(response, 'name="form-0-fri" size="2" type="text" value="0"', 1, 200)
        self.assertNotContains(response, 'name="form-1-thu"')
        self.assertEqual(0, timesheet.timeentry_set.count())

    def test_load_a_full_timesheet_get(self):
        self.client.login(username='john', password='johnpassword')
        timesheet = Timesheet.objects.create_timesheet(year=2013, week_number=40, user=self.user)
        TimeEntry.objects.create(project=self.p1, hours=8, user=self.user, reg_date='2013-10-4', timesheet=timesheet)
        response = self.client.get(reverse('timesheet:load', kwargs={'year': 2013, 'week_number': 40}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="form-0-fri" size="2" type="text" value="8"', 1, 200)
        self.assertNotContains(response, 'name="form-1-thu"')
        self.assertEqual(1, timesheet.timeentry_set.count())

    '''
    TODO
    def test_load_a_full_timesheet_duplicate_project_get(self):
        self.client.login(username='john', password='johnpassword')
        timesheet = Timesheet.objects.create_timesheet(year=2013, week_number=40, user=self.user)
        TimeEntry.objects.create(project=self.p1, hours=4, user=self.user, reg_date='2013-10-4', timesheet=timesheet)
        TimeEntry.objects.create(project=self.p1, hours=4, user=self.user, reg_date='2013-10-4', timesheet=timesheet)
        response = self.client.get(reverse('timesheet:load', kwargs={'year': 2013, 'week_number': 40}))
        self.assertEqual(response.status_code, 200)
        #print response.context[-1]['formset']
        self.assertContains(response, 'name="form-0-fri" value="8"', 1, 200)
    '''


    def test_load_a_full_timesheet_with_more_projects_get(self):
        self.client.login(username='john', password='johnpassword')
        timesheet = Timesheet.objects.create_timesheet(year=2013, week_number=39, user=self.user)
        TimeEntry.objects.create(project=self.p1, hours=8, user=self.user, reg_date='2013-10-4', timesheet=timesheet)
        TimeEntry.objects.create(project=self.p2, hours=4, user=self.user, reg_date='2013-10-3', timesheet=timesheet)
        response = self.client.get(reverse('timesheet:load', kwargs={'year': 2013, 'week_number': 39}))
        self.assertEqual(response.status_code, 200)
        #print response.context[-1]['formset']
        self.assertContains(response, 'name="form-0-fri" size="2" type="text" value="8"', 1, 200)
        self.assertContains(response, 'name="form-1-thu" size="2" type="text" value="4"', 1, 200)
        self.assertNotContains(response, 'name="form-2-thu"')
        self.assertEqual(2, timesheet.timeentry_set.count())


    def test_update_an_existing_timesheet_post(self):
        self.client.login(username='john', password='johnpassword')
        timesheet = Timesheet.objects.create_timesheet(year=2013, week_number=40, user=self.user)
        # 2013-10-3 was a thu ;-)
        TimeEntry.objects.create(project=self.p2, hours=4, user=self.user, reg_date='2013-10-3', timesheet=timesheet)
        post_data = {
            'form-TOTAL_FORMS': u'2',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-project': u'1',
            'form-0-mon': u'0',
            'form-0-tue': u'8',
            'form-0-wed': u'0',
            'form-0-thu': u'0',
            'form-0-fri': u'0',
            'form-0-sat': u'0',
            'form-0-sun': u'0',
            'form-1-project': u'2',
            'form-1-mon': u'0',
            'form-1-tue': u'8',
            'form-1-wed': u'8',
            'form-1-thu': u'0',
            'form-1-fri': u'0',
            'form-1-sat': u'0',
            'form-1-sun': u'0',
            u'submit': [u'Submit timesheet']
        }
        response = self.client.post(reverse('timesheet:load', kwargs={'year': 2013, 'week_number': 40}), post_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(3, TimeEntry.objects.filter(reg_date__range=(date(2013, 9, 30), date(2013, 10, 6))).count())
        self.assertEqual(3, timesheet.timeentry_set.count())
        self.assertTemplateUsed(response, 'timesheet/timesheet_list.html')

    def test_delete_an_existing_timesheet_post(self):
        self.client.login(username='john', password='johnpassword')
        timesheet = Timesheet.objects.create_timesheet(year=2013, week_number=40, user=self.user)
        # 2013-10-3 was a thu ;-)
        TimeEntry.objects.create(project=self.p2, hours=4, user=self.user, reg_date='2013-10-3', timesheet=timesheet)
        post_data = {
            'form-TOTAL_FORMS': u'1',
            'form-INITIAL_FORMS': u'0',
            'form-MAX_NUM_FORMS': u'',
            'form-0-project': u'1',
            'form-0-mon': u'0',
            'form-0-tue': u'8',
            'form-0-wed': u'0',
            'form-0-thu': u'0',
            'form-0-fri': u'0',
            'form-0-sat': u'0',
            'form-0-sun': u'0',
            u'submit': [u'Submit timesheet']
        }
        response = self.client.post(reverse('timesheet:load', kwargs={'year': 2013, 'week_number': 40}), post_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, TimeEntry.objects.filter(reg_date__range=(date(2013, 9, 30), date(2013, 10, 6))).count())
        self.assertEqual(1, timesheet.timeentry_set.count())
        self.assertTemplateUsed(response, 'timesheet/timesheet_list.html')

    def test_InsertHolidayViewSet(self):
        url = '/timesheet/insert/'
        data = {"project": "1", "hours": "8", "user": "user", "reg_date": "2013-12-12", "timesheet": "1"}
        response = self.client.post(url, data, format='json')
        #self.assertEqual(response.status_code, 200)


class TimesheetFormsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        p = Project(name="project1", code="pj1")
        p.save()

    def test_first_day_of_this_week(self):
        today = date(2013, 8, 29)
        aspected_result = date(2013, 8, 26)
        self.assertEqual(aspected_result, Timesheet.first_day_of_this_week(today))

    def test_clean_true(self):
        post_data = {
            'mon': u'8',
            'project': u'1',
        }
        timesheet_form = TimesheetForm(data=post_data)
        print timesheet_form.errors
        self.assertEquals(0, len(timesheet_form.errors))
        self.assertTrue(timesheet_form.is_valid())

    def test_clean_false(self):
        post_data = {
            'project': u'1',
            'mon': u'0',
            'tue': u'0',
            'wed': u'0',
            'thu': u'0',
            'fri': u'0',
            'sat': u'0',
            'sun': u'0',
        }
        timesheetForm = TimesheetForm(data=post_data)
        self.assertEquals(1, len(timesheetForm.errors))
        self.assertFalse(timesheetForm.is_valid())

'''
class TimeEntrySerializerTests(TestCase):
    def test_restore_object(self):
        timeEntrySerializer = TimeEntrySerializer()
        attrs={"hours":"8"}
        timeEntry = timeEntrySerializer.restore_object(self, attrs)
        self.assertIsNotNone(timeEntry)
'''