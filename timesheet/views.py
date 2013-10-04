from leantracker.timesheet.forms import TimesheetForm, week_start_date
from leantracker.timesheet.models import TimeEntry, Timesheet
from django.forms.formsets import formset_factory
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from datetime import timedelta


@login_required
def submit_timesheet(request, week_number, year):
  TimesheetFormSet = formset_factory(TimesheetForm)
  if request.method == 'POST':
    formset = TimesheetFormSet(request.POST, request.FILES)
    if 'submit' in request.POST:
      if formset.is_valid():
        monday = week_start_date(int(year), int(week_number))
        delta = timedelta(days=1)
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
            timeentry = TimeEntry(project=project, hours=mon, user=request.user, reg_date=monday)
            timeentry.save()
          if tue != 0:
            timeentry = TimeEntry(project=project, hours=tue, user=request.user, reg_date=monday + delta)
            timeentry.save()
          if wed != 0:
            timeentry = TimeEntry(project=project, hours=wed, user=request.user, reg_date=monday + 2 * delta)
            timeentry.save()
          if thu != 0:
            timeentry = TimeEntry(project=project, hours=thu, user=request.user, reg_date=monday + 3 * delta)
            timeentry.save()
          if fri != 0:
            timeentry = TimeEntry(project=project, hours=fri, user=request.user, reg_date=monday + 4 * delta)
            timeentry.save()
          if sat != 0:
            timeentry = TimeEntry(project=project, hours=sat, user=request.user, reg_date=monday + 5 * delta)
            timeentry.save()
          if sun != 0:
            timeentry = TimeEntry(project=project, hours=sun, user=request.user, reg_date=monday + 6 * delta)
            timeentry.save()
        return render_to_response('timesheet/index.html')
  else:
    formset = TimesheetFormSet()
  return render_to_response('timesheet/timesheet_form.html', {'formset': formset},
                            context_instance=RequestContext(request))


@login_required
def load_timesheet(request, week_number, year):
  # if exist a timesheet: load, if don't exist: create a new one
  TimesheetFormSet = formset_factory(TimesheetForm)
  formset = TimesheetFormSet()
  timesheet = Timesheet(week_number=week_number, year=year, status='W', user=request.user)
  timesheet.save()
  return render_to_response('timesheet/timesheet_form.html', {'formset': formset},
                            context_instance=RequestContext(request))
