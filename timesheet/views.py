from leantracker.timesheet.forms import TimesheetForm,BaseTimesheetFormSet
from django.forms.formsets import formset_factory
from django.template.context import RequestContext
from django.shortcuts import render_to_response

def create_timesheet(request):
    TimesheetFormSet = formset_factory(TimesheetForm,BaseTimesheetFormSet,can_delete=True)
    if request.method == 'POST':
        if 'add_row' in request.POST:
            formset = TimesheetFormSet(request.POST, request.FILES)
            if formset.is_valid():
                cp = request.POST.copy()
                cp['form-TOTAL_FORMS'] = int(cp['form-TOTAL_FORMS']) + 1 
                formset = TimesheetFormSet(cp,request.FILES)           
        elif 'submit' in request.POST:
            formset = TimesheetFormSet(request.POST, request.FILES)            
            if formset.is_valid():
                formset.save()
                return render_to_response('timesheet/index.html')
        elif 'delete_rows' in request.POST:      
            formset = TimesheetFormSet(request.POST, request.FILES)
            if formset.is_valid():               
               formset.save()                    
    else:
        formset = TimesheetFormSet()
    return render_to_response('timesheet/timesheet_form.html', {'formset': formset}, context_instance=RequestContext(request))


