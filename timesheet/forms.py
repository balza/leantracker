from django import forms
from django.forms import Form,ChoiceField
from leantracker.projects.models import Project

class TimesheetForm(Form):
   projects = forms.ChoiceField(choices=[("*", "---")] + [(x.id, x.name) for x in Project.groupproject_objects.all()])
