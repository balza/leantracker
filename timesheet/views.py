from leantracker.timesheet.forms import TimesheetBaseFormSet,TimesheetForm
from leantracker.timesheet.models import WeekEntry
from django.forms.models import modelformset_factory
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def create_timesheet(request):
    TimesheetFormSet = modelformset_factory(WeekEntry, form=TimesheetForm, formset=TimesheetBaseFormSet)
    if request.method == 'POST':        
        formset = TimesheetFormSet(request.POST, request.FILES, user=request.user)           
        if 'submit' in request.POST:                  
            if formset.is_valid():                                       
                formset.save()
                return render_to_response('timesheet/index.html')        
    else:                
        formset = TimesheetFormSet(user=request.user) 
        
    return render_to_response('timesheet/timesheet_form.html', {'formset': formset}, context_instance=RequestContext(request))
