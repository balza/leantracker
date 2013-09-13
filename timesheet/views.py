from leantracker.timesheet.forms import TimesheetForm,TimesheetBaseFormSet
from django.forms.formsets import formset_factory
from django.template.context import RequestContext
from django.shortcuts import render_to_response

def create_timesheet(request):
    TimesheetFormSet = formset_factory(TimesheetForm, TimesheetBaseFormSet)
    if request.method == 'POST':        
        formset = TimesheetFormSet(request.POST, request.FILES)           
        if 'submit' in request.POST:                  
            if formset.is_valid():                         
                formset.salva(request.user)
                return render_to_response('timesheet/index.html')        
    else:        
        formset = TimesheetFormSet()    
    return render_to_response('timesheet/timesheet_form.html', {'formset': formset}, context_instance=RequestContext(request))
