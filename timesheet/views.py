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
            print "submit"                  
            if formset.is_valid():
                print "is_valid"       
                timesheet = Timesheet()
                timesheet.save()
                for form in formset: 
                    project = request.cleaned_data("project")
                    timeEntry = TimeEntry(project = project, hours = 8, user = request.user, reg_date = date(2005, 1, 1))
                    timeEntry.save()
                    print "Form"
                
                return render_to_response('timesheet/index.html')        
    else:                
        formset = TimesheetFormSet() 
        
    return render_to_response('timesheet/timesheet_form.html', {'formset': formset}, context_instance=RequestContext(request))
