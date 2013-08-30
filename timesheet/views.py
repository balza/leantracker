from leantracker.timesheet.forms import TimesheetForm,BaseTimesheetFormSet
from django.forms.formsets import formset_factory
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.forms.models import inlineformset_factory

def create_timesheet(request):
    TimesheetFormSet = formset_factory(TimesheetForm,formset=BaseTimesheetFormSet)
    if request.method == 'POST':
        if 'add_row' in request.POST:
            cp = request.POST.copy()
            cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS']) + 1
            formset = TimesheetFormSet(cp, request.FILES)           		
        elif 'submit' in request.POST:
            print "create_timesheet submit"
            formset = TimesheetFormSet(request.POST, request.FILES)        
            if formset.is_valid():
                return render_to_response('timesheet/index.html')			
    else:
        formset = TimesheetFormSet()
    return render_to_response('timesheet/timesheet_form.html', {'formset': formset}, context_instance=RequestContext(request))


