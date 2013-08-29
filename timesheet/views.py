from leantracker.timesheet.forms import TimesheetForm
from django.forms.formsets import formset_factory
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.forms.models import inlineformset_factory

def create_timesheet(request):
    #TimesheetFormSet = inlineformset_factory(TimesheetForm)
    TimesheetFormSet = formset_factory(TimesheetForm)
    if request.method == 'POST':
        formset = TimesheetFormSet(request.POST, request.FILES)
        # if 'add_row' in request.POST:
        #     cp = request.POST.copy()
        #     cp['form-TOTAL_FORMS'] = int(cp['car-TOTAL_FORMS'])+ 1
        #     formset = TimesheetFormSet(cp)
        # elif 'submit' in request.POST:
        if formset.is_valid():
          return render_to_response('timesheet/index.html')
    else:
        formset = TimesheetFormSet()
    return render_to_response('timesheet/timesheet_form.html', {'formset': formset}, context_instance=RequestContext(request))


