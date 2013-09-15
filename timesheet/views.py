from leantracker.timesheet.forms import TimesheetBaseFormSet,TimesheetForm
from leantracker.timesheet.models import TimeEntry
from django.forms.models import modelformset_factory
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.utils.functional import curry

@login_required
def create_timesheet(request):
    TimesheetFormSet = modelformset_factory(TimeEntry, form=TimesheetForm, formset=TimesheetBaseFormSet)
    TimesheetFormSet.form = staticmethod(curry(TimesheetForm, user=request.user))
    if request.method == 'POST':        
        formset = TimesheetFormSet(request.POST, request.FILES, user=request.user)           
        if 'submit' in request.POST:                  
            if formset.is_valid():                                       
                formset.save()
                return render_to_response('timesheet/index.html')        
    else:                
        formset = TimesheetFormSet(user=request.user) 
        
    return render_to_response('timesheet/timesheet_form.html', {'formset': formset}, context_instance=RequestContext(request))
