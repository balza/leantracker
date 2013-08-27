from django import forms
from django.forms import Form,ModelForm,ChoiceField
from leantracker.projects.models import Project
from leantracker.timesheet.models import Timesheet

class TimesheetForm(Form):
   projects = forms.ChoiceField(choices=[("*", "---")] + [(x.id, x.name) for x in Project.groupproject_objects.all()])
   mon = forms.IntegerField(max_value=8,min_value=0)
   tue = forms.IntegerField(max_value=8,min_value=0)
   wed = forms.IntegerField(max_value=8,min_value=0)
   thu = forms.IntegerField(max_value=8,min_value=0)
   fri = forms.IntegerField(max_value=8,min_value=0)
   sat = forms.IntegerField(max_value=8,min_value=0)
   sun = forms.IntegerField(max_value=8,min_value=0)
#   class Meta:
#     model = Timesheet
