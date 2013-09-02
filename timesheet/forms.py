from django import forms
from django.forms import Form,ModelForm,ChoiceField,TextInput,ModelChoiceField
from leantracker.projects.models import Project
from leantracker.timesheet.models import Timesheet
from datetime import date, timedelta
from django.utils.safestring import mark_safe

#TODO: spostare in una classe adeguata
def first_day_of_this_week(today):
    year = today.isocalendar()[0]
    week_number= today.isocalendar()[1]    
    return week_start_date(year,week_number)

#TODO: spostare in una classe adeguata
def week_start_date(year, week):
    d = date(year, 1, 1)    
    delta_days = d.isoweekday() - 1
    delta_weeks = week
    if year == d.isocalendar()[0]:
        delta_weeks -= 1
    delta = timedelta(days=-delta_days, weeks=delta_weeks)
    return d + delta

class TimesheetForm(Form):
    #TODO: filtrare solo per il gruppo dell'utente
    project = forms.ModelChoiceField(queryset=Project.objects.all(), empty_label="-------")
    delta = timedelta(days=1)
    monday = first_day_of_this_week(date.today())  
    mon = forms.IntegerField(max_value=24,min_value=0,widget=forms.TextInput(attrs={'size':'2','value':'0'}),label=mark_safe(monday.strftime("%a <br/> %d %b")))
    tue = forms.IntegerField(max_value=24,min_value=0,widget=forms.TextInput(attrs={'size':'2','value':'0'}),label=mark_safe((monday + delta).strftime("%a <br/> %d %b")))
    wed = forms.IntegerField(max_value=24,min_value=0,widget=forms.TextInput(attrs={'size':'2','value':'0'}),label=mark_safe((monday + 2 * delta).strftime("%a <br/> %d %b")))
    thu = forms.IntegerField(max_value=24,min_value=0,widget=forms.TextInput(attrs={'size':'2','value':'0'}),label=mark_safe((monday + 3 * delta).strftime("%a <br/> %d %b")))
    fri = forms.IntegerField(max_value=24,min_value=0,widget=forms.TextInput(attrs={'size':'2','value':'0'}),label=mark_safe((monday + 4 * delta).strftime("%a <br/> %d %b")))
    sat = forms.IntegerField(max_value=24,min_value=0,widget=forms.TextInput(attrs={'size':'2','value':'0'}),label=mark_safe((monday + 5 * delta).strftime("%a <br/> %d %b")))
    sun = forms.IntegerField(max_value=24,min_value=0,widget=forms.TextInput(attrs={'size':'2','value':'0'}),label=mark_safe((monday + 6 * delta).strftime("%a <br/> %d %b")))

    
    

