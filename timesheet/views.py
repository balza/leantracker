from leantracker.timesheet.forms import TimesheetForm
from django.forms.formsets import formset_factory
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.forms.models import inlineformset_factory

def create_timesheet(request):
    TimesheetFormSet = formset_factory(TimesheetForm, can_delete=True)
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
                return render_to_response('timesheet/index.html')
        elif 'delete_rows' in request.POST:      
            formset = TimesheetFormSet(request.POST, request.FILES)
            if formset.is_valid():
                for form in formset.deleted_forms:
                    form.cleaned_data                    
    else:
        formset = TimesheetFormSet()
    return render_to_response('timesheet/timesheet_form.html', {'formset': formset}, context_instance=RequestContext(request))


