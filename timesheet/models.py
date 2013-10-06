from django.db import models
from leantracker.projects.models import Project
from django.contrib.auth.models import User

TIMESHEET_STATUS = (
    ('W', 'Draft'),
    ('P', 'Submitted'),
    ('R', 'Rejected'),
    ('A', 'Accepted'),
)

class TimesheetManager(models.Manager):

    def create_timesheet(self, year, week_number,  user):
        timesheet = self.create(year=year,  week_number=week_number, status='W', user=user)
        return timesheet


class Timesheet(models.Model):
    
    week_number = models.IntegerField('Week of the timesheet')     
    year = models.IntegerField('Year of the timesheet')
    status = models.CharField(max_length=20, choices=TIMESHEET_STATUS, default=0)    
    user = models.ForeignKey(User)
 
    def __unicode__(self):
        return "timesheet for year %s, week number %s" % (self.year, self.week_number)
        
    objects = TimesheetManager()

class TimeEntry(models.Model):

  project = models.ForeignKey(Project)
  hours = models.IntegerField()
  user = models.ForeignKey(User)
  reg_date = models.DateTimeField('Registration date')
  timesheet = models.ForeignKey(Timesheet)

  def __unicode__(self):
        return "For project %s the user %s in date %s worked %s hour" % (self.project, self.user, self.reg_date, self.hours)