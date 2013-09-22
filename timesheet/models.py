from django.db import models
from leantracker.projects.models import Project
from django.contrib.auth.models import User

TIMESHEET_STATUS = (
    ('W', 'Draft'),
    ('P', 'Submitted'),
    ('R', 'Rejected'),
    ('A', 'Accepted'),
)

class TimeEntry(models.Model):
    
  project = models.ForeignKey(Project)  
  hours = models.IntegerField()
  user = models.ForeignKey(User)
  reg_date = models.DateTimeField('Registration date')

  def __unicode__(self):
        return "For project %s the user %s in date %s worked %s" % (self.project, self.user, self.reg_date, self.hours)
        
class TimesheetManager(models.Manager):

    def create_timesheet(self, start, end, user):
        timesheet = self.create(start=start, end=end, status='W',user=user)        
        return timesheet

class Timesheet(models.Model):
    
    week_number = models.IntegerField('Week of the timesheet')     
    year = models.IntegerField('Year of the timesheet')
    status = models.CharField(max_length=20, choices=TIMESHEET_STATUS, default=0)    
    user = models.ForeignKey(User)
 
    def __unicode__(self):
        return "timesheet from %s to %s" % (self.start, self.end) 
        
    objects = TimesheetManager()
    
