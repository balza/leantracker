from leantracker.timesheet.forms import TimesheetForm
from django.forms.formsets import formset_factory
from django.shortcuts import render_to_response

def manage_timesheet(request):
    TimesheetFormSet = formset_factory(TimesheetForm)
    if request.method == 'POST':
        formset = TimesheetFormSet(request.POST, request.FILES)
        if formset.is_valid():
           return render_to_response('timesheet/index.html')
    else:
        formset = TimesheetFormSet()
    return render_to_response('timesheet/timesheet_form.html', {'formset': formset})

