from leantracker.timesheet.forms import TimesheetForm
from leantracker.timesheet.models import TimeEntry,Timesheet
from django.forms.formsets import formset_factory
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required
def create_timesheet(request):
    TimesheetFormSet = formset_factory(TimesheetForm)    
    if request.method == 'POST':        
        formset = TimesheetFormSet(request.POST, request.FILES)           
        if 'submit' in request.POST:                 
            if formset.is_valid():                
                timesheet = Timesheet(week_number=23, year=2013, status='W',user = request.user)
                timesheet.save()
                for form in formset:  
                    project = form.cleaned_data["project"]
                    mon = form.cleaned_data["mon"]                        
                    tue = form.cleaned_data["tue"]
                    wed = form.cleaned_data["wed"]
                    thu = form.cleaned_data["thu"]
                    fri = form.cleaned_data["fri"]
                    sat = form.cleaned_data["sat"]
                    sun = form.cleaned_data["sun"]
                    if mon != 0:                        
                        timeEntry = TimeEntry(project = project, hours = 8, user = request.user, reg_date = date(2005, 1, 1))
                        timeEntry.save()
                    if tue != 0:
                        timeEntry = TimeEntry(project = project, hours = 8, user = request.user, reg_date = date(2005, 1, 1))
                        timeEntry.save()
                    if wed != 0:                        
                        timeEntry = TimeEntry(project = project, hours = 8, user = request.user, reg_date = date(2005, 1, 1))
                        timeEntry.save()
                    if thu != 0:                        
                        timeEntry = TimeEntry(project = project, hours = 8, user = request.user, reg_date = date(2005, 1, 1))
                        timeEntry.save()
                    if fri != 0:                        
                        timeEntry = TimeEntry(project = project, hours = 8, user = request.user, reg_date = date(2005, 1, 1))
                        timeEntry.save()
                    if sat != 0:                        
                        timeEntry = TimeEntry(project = project, hours = 8, user = request.user, reg_date = date(2005, 1, 1))
                        timeEntry.save()
                    if sun != 0:                        
                        timeEntry = TimeEntry(project = project, hours = 8, user = request.user, reg_date = date(2005, 1, 1))
                        timeEntry.save()                                        
                return render_to_response('timesheet/index.html')        
    else:                
        formset = TimesheetFormSet()        
    return render_to_response('timesheet/timesheet_form.html', {'formset': formset}, context_instance=RequestContext(request))
