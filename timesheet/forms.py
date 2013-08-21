from django.forms import ModelForm
from leantracker.timesheet.models import Timesheet

class TimesheetForm(ModelForm):
    class Meta:
        model = Timesheet
