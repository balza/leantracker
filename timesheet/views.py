from django.forms.formsets import formset_factory
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from datetime import timedelta

from leantracker.timesheet.forms import TimesheetForm
from leantracker.timesheet.models import TimeEntry, Timesheet


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
                monday = Timesheet.week_start_date(int(year), int(week_number))
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
                        timeentry = TimeEntry(project=project, hours=mon, user=request.user, reg_date=monday,
                                              timesheet=timesheet)
                        timeentry.save()
                    if tue != 0:
                        timeentry = TimeEntry(project=project, hours=tue, user=request.user, reg_date=monday + delta,
                                              timesheet=timesheet)
                        timeentry.save()
                    if wed != 0:
                        timeentry = TimeEntry(project=project, hours=wed, user=request.user,
                                              reg_date=monday + 2 * delta,
                                              timesheet=timesheet)
                        timeentry.save()
                    if thu != 0:
                        timeentry = TimeEntry(project=project, hours=thu, user=request.user,
                                              reg_date=monday + 3 * delta,
                                              timesheet=timesheet)
                        timeentry.save()
                    if fri != 0:
                        timeentry = TimeEntry(project=project, hours=fri, user=request.user,
                                              reg_date=monday + 4 * delta,
                                              timesheet=timesheet)
                        timeentry.save()
                    if sat != 0:
                        timeentry = TimeEntry(project=project, hours=sat, user=request.user,
                                              reg_date=monday + 5 * delta,
                                              timesheet=timesheet)
                        timeentry.save()
                    if sun != 0:
                        timeentry = TimeEntry(project=project, hours=sun, user=request.user,
                                              reg_date=monday + 6 * delta,
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
        'form-0-mon': u'0',
        'form-0-tue': u'0',
        'form-0-wed': u'0',
        'form-0-thu': u'0',
        'form-0-fri': u'0',
        'form-0-sat': u'0',
        'form-0-sun': u'0',
    }
    #dynamic values
    timeentries = timesheet.timeentry_set.all()
    projects = timeentries.order_by('project').distinct()
    data['form-TOTAL_FORMS'] = u'' + str(projects.count() + 1) + ''
    print 'project count :' + str(projects.count())
    for timeentry in timeentries:
        project_index = 0
        for project in projects:
            data['form-' + str(project_index) + '-project'] = u'' + str(project) + ''
            for day in range(0, 6):
                if timeentry.project == project:
                    data['form-' + str(day) + '-' + str(week_day[day+1])] = u'' + str(timeentry.hours) + ''
                else:
                    data['form-' + str(day) + '-' + str(week_day[day+1])] = u'0'
            project_index += 1

    '''
    project_index = 0
    for timeentry in timeentries:
      data['form-' + str(project_index) + '-project'] = u'' + str(timeentry.project) + ''
      data['form-' + str(project_index) + '-' + str(week_day[timeentry.reg_date.isoweekday()])] = u'' + str(timeentry.hours) + ''
      project_index += 1
    '''
    timesheetFormSet = formset_factory(TimesheetForm)
    formset = timesheetFormSet(data)
    #Timesheet.objects.create_timesheet(week_number=week_number, year=year, user=request.user)
    return render_to_response('timesheet/timesheet_form.html', {'formset': formset},
                              context_instance=RequestContext(request))
