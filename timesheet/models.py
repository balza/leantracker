from django.db import models
from leantracker.projects.models import Project
from django.contrib.auth.models import User

TIMESHEET_STATUS = (
    ('W', 'Draft'),
    ('P', 'Submitted'),
    ('R', 'Rejected'),
    ('A', 'Accepted'),
)

class Registration(models.Model):
  project = models.ForeignKey(Project)
  hours = models.IntegerField()
  user = models.ForeignKey(User)
  reg_date = models.DateTimeField('Registration date')

  def __unicode__(self):
        return "For project %s the user %s in date %s worked %s" % (self.project, self.user, self.reg_date, self.hours)

class Timesheet(models.Model):
  start = models.DateField('Timesheet start')
  end = models.DateField('Timesheet end') 
  status = models.CharField(max_length=20, choices=TIMESHEET_STATUS, default=0)
 
  def __unicode__(self):
    return "timesheet from %s to %s" % (self.start, self.end) 
