from time import strftime
from leantracker.timesheet.forms import TimesheetForm, week_start_date
from leantracker.timesheet.models import TimeEntry, Timesheet
from django.forms.formsets import formset_factory
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from datetime import timedelta

week_day = {
    1: 'mon',
    2: 'tue',
    3: 'wed',
    4: 'thu',
    5: 'fri',
    6: 'sat',
    7: 'sun',
}


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
          timesheet = Timesheet.objects.get(year=year, week_number=week_number, user=request.user)
          if mon != 0:
            timeentry = TimeEntry(project=project, hours=mon, user=request.user, reg_date=monday, timesheet=timesheet)
            timeentry.save()
          if tue != 0:
            timeentry = TimeEntry(project=project, hours=tue, user=request.user, reg_date=monday + delta,
                                  timesheet=timesheet)
            timeentry.save()
          if wed != 0:
            timeentry = TimeEntry(project=project, hours=wed, user=request.user, reg_date=monday + 2 * delta,
                                  timesheet=timesheet)
            timeentry.save()
          if thu != 0:
            timeentry = TimeEntry(project=project, hours=thu, user=request.user, reg_date=monday + 3 * delta,
                                  timesheet=timesheet)
            timeentry.save()
          if fri != 0:
            timeentry = TimeEntry(project=project, hours=fri, user=request.user, reg_date=monday + 4 * delta,
                                  timesheet=timesheet)
            timeentry.save()
          if sat != 0:
            timeentry = TimeEntry(project=project, hours=sat, user=request.user, reg_date=monday + 5 * delta,
                                  timesheet=timesheet)
            timeentry.save()
          if sun != 0:
            timeentry = TimeEntry(project=project, hours=sun, user=request.user, reg_date=monday + 6 * delta,
                                  timesheet=timesheet)
            timeentry.save()
        return render_to_response('timesheet/timesheet_list.html')
  else:
    formset = TimesheetFormSet()
  return render_to_response('timesheet/timesheet_form.html', {'formset': formset},
                            context_instance=RequestContext(request))


@login_required
def load_timesheet(request, week_number, year):
  timesheet = Timesheet.objects.get(week_number=week_number, year=year, user=request.user)
  #static values
  data = {
    'form-INITIAL_FORMS': u'0',
    'form-MIN_NUM_FORMS': u'',
    'form-MAX_NUM_FORMS': u'',
  }
  #dynamic values
  rows = timesheet.timeentry_set.all()
  data['form-TOTAL_FORMS'] = u'' + str(rows.count()) + ''
  i=0
  for timeentry in rows:
    data['form-' + str(i) + '-project'] = u'' + str(timeentry.project) + ''
    data['form-' + str(i) + '-' + str(week_day[timeentry.reg_date.isoweekday()])] = u'' + str(timeentry.hours) + ''
    i += 1
  TimesheetFormSet = formset_factory(TimesheetForm)
  formset = TimesheetFormSet(data)
  #Timesheet.objects.create_timesheet(week_number=week_number, year=year, user=request.user)
  return render_to_response('timesheet/timesheet_form.html', {'formset': formset},
                            context_instance=RequestContext(request))
