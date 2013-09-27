from django import forms
from django.forms import Form
from leantracker.projects.models import Project
from leantracker.timesheet.models import TimeEntry
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
    project = forms.ModelChoiceField(required=False,queryset=Project.objects.all(), empty_label="-------")
    delta = timedelta(days=1)
    monday = first_day_of_this_week(date.today())  
    mon = forms.IntegerField(required=False, max_value=24,min_value=0,widget=forms.TextInput(attrs={'size':'2','value':'0'}),label=mark_safe(monday.strftime("%a <br/> %d %b")))
    tue = forms.IntegerField(required=False, max_value=24,min_value=0,widget=forms.TextInput(attrs={'size':'2','value':'0'}),label=mark_safe((monday + delta).strftime("%a <br/> %d %b")))
    wed = forms.IntegerField(required=False, max_value=24,min_value=0,widget=forms.TextInput(attrs={'size':'2','value':'0'}),label=mark_safe((monday + 2 * delta).strftime("%a <br/> %d %b")))
    thu = forms.IntegerField(required=False, max_value=24,min_value=0,widget=forms.TextInput(attrs={'size':'2','value':'0'}),label=mark_safe((monday + 3 * delta).strftime("%a <br/> %d %b")))
    fri = forms.IntegerField(required=False, max_value=24,min_value=0,widget=forms.TextInput(attrs={'size':'2','value':'0'}),label=mark_safe((monday + 4 * delta).strftime("%a <br/> %d %b")))
    sat = forms.IntegerField(required=False, max_value=24,min_value=0,widget=forms.TextInput(attrs={'size':'2','value':'0'}),label=mark_safe((monday + 5 * delta).strftime("%a <br/> %d %b")))
    sun = forms.IntegerField(required=False, max_value=24,min_value=0,widget=forms.TextInput(attrs={'size':'2','value':'0'}),label=mark_safe((monday + 6 * delta).strftime("%a <br/> %d %b")))
    
    '''
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(TimesheetForm, self).__init__(*args, **kwargs)
    '''
         
    def clean(self): 
        cleaned_data = super(TimesheetForm, self).clean()          
        mon = cleaned_data.get("mon")
        tue = cleaned_data.get("tue")
        wed = cleaned_data.get("wed")
        thu = cleaned_data.get("thu")
        fri = cleaned_data.get("fri")
        sat = cleaned_data.get("sat")
        sun = cleaned_data.get("sun")         
        if mon==0 and tue==0 and wed==0 and thu==0 and fri==0 and sat==0  and sun==0:            
            raise forms.ValidationError("Insert at least a day")       
        return cleaned_data
    
    def save(self):
      project = self.cleaned_data["project"]
      mon = self.cleaned_data["mon"]                        
      tue = self.cleaned_data["tue"]
      wed = self.cleaned_data["wed"]
      thu = self.cleaned_data["thu"]
      fri = self.cleaned_data["fri"]
      sat = self.cleaned_data["sat"]
      sun = self.cleaned_data["sun"]
      if mon != 0:                        
          timeEntry = TimeEntry(project = project, hours = 8, user = self._user, reg_date = date(2005, 1, 1))
          timeEntry.save()
      if tue != 0:
          timeEntry = TimeEntry(project = project, hours = 8, user = self._user, reg_date = date(2005, 1, 1))
          timeEntry.save()
      if wed != 0:                        
          timeEntry = TimeEntry(project = project, hours = 8, user = self._user, reg_date = date(2005, 1, 1))
          timeEntry.save()
      if thu != 0:                        
          timeEntry = TimeEntry(project = project, hours = 8, user = self._user, reg_date = date(2005, 1, 1))
          timeEntry.save()
      if fri != 0:                        
          timeEntry = TimeEntry(project = project, hours = 8, user = self._user, reg_date = date(2005, 1, 1))
          timeEntry.save()
      if sat != 0:                        
          timeEntry = TimeEntry(project = project, hours = 8, user = self._user, reg_date = date(2005, 1, 1))
          timeEntry.save()
      if sun != 0:                        
          timeEntry = TimeEntry(project = project, hours = 8, user = self._user, reg_date = date(2005, 1, 1))
          timeEntry.save()   
       