from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

from leantracker.projects.models import Project


TIMESHEET_STATUS = (
    ('W', 'Draft'),
    ('P', 'Submitted'),
    ('R', 'Rejected'),
    ('A', 'Accepted'),
)


class TimesheetManager(models.Manager):
    def create_timesheet(self, year, week_number, user):
        timesheet = self.create(year=year, week_number=week_number, status='W', user=user)
        return timesheet


class Timesheet(models.Model):
    week_number = models.IntegerField('Week of the timesheet')
    year = models.IntegerField('Year of the timesheet')
    status = models.CharField(max_length=20, choices=TIMESHEET_STATUS, default=0)
    user = models.ForeignKey(User)

    @staticmethod
    def week_start_date(year, week):
        d = date(year, 1, 1)
        delta_days = d.isoweekday() - 1
        delta_weeks = week
        if year == d.isocalendar()[0]:
            delta_weeks -= 1
        delta = timedelta(days=-delta_days, weeks=delta_weeks)
        return d + delta

    @staticmethod
    def first_day_of_this_week(a_day):
        year = a_day.isocalendar()[0]
        week_number = a_day.isocalendar()[1]
        return Timesheet.week_start_date(year, week_number)

    objects = TimesheetManager()

    def __unicode__(self):
        return "timesheet for year %s, week number %s of %s" % (self.year, self.week_number, self.user)


class TimeEntry(models.Model):
    project = models.ForeignKey(Project)
    hours = models.IntegerField()
    user = models.ForeignKey(User)
    reg_date = models.DateTimeField('Registration date')
    timesheet = models.ForeignKey(Timesheet)

    def __unicode__(self):
        return "For project %s the user %s in date %s worked %s hour" % (
        self.project, self.user, self.reg_date, self.hours)