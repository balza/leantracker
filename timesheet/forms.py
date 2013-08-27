from django import forms
from django.forms import Form,ModelForm,ChoiceField,TextInput
from leantracker.projects.models import Project
from leantracker.timesheet.models import Timesheet

class TimesheetForm(Form):
   projects = forms.ChoiceField(choices=[("*", "---")] + [(x.id, x.name) for x in Project.group_projects.all()])
   mon = forms.IntegerField(max_value=8,min_value=0,widget=forms.TextInput(attrs={'size':'2'}))
   tue = forms.IntegerField(max_value=8,min_value=0,widget=forms.TextInput(attrs={'size':'2'}))
   wed = forms.IntegerField(max_value=8,min_value=0,widget=forms.TextInput(attrs={'size':'2'}))
   thu = forms.IntegerField(max_value=8,min_value=0,widget=forms.TextInput(attrs={'size':'2'}))
   fri = forms.IntegerField(max_value=8,min_value=0,widget=forms.TextInput(attrs={'size':'2'}))
   sat = forms.IntegerField(max_value=8,min_value=0,widget=forms.TextInput(attrs={'size':'2'}))
   sun = forms.IntegerField(max_value=8,min_value=0,widget=forms.TextInput(attrs={'size':'2'}))

