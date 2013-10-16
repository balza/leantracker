import django.forms.formsets
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
def timesheet(request, week_number, year):
    TimesheetFormSet = django.forms.formsets.formset_factory(TimesheetForm)
    if request.method == 'POST':
        formset = TimesheetFormSet(request.POST, request.FILES)
        if 'submit' in request.POST:
            if formset.is_valid():
                monday = Timesheet.week_start_date(int(year), int(week_number))
                delta = timedelta(days=1)
                try:
                    readed_timesheet = Timesheet.objects.get(year=year, week_number=week_number, user=request.user)
                    timesheet = Timesheet(id=readed_timesheet.id, year=year, week_number=week_number, user=request.user)
                except Exception as inst:
                    print "not found " + str(inst)
                    timesheet = Timesheet(year=year, week_number=week_number, user=request.user)
                timesheet.save()
                for form in formset:
                    project = form.cleaned_data["project"]
                    for i in range(1, 7):
                        hours = form.cleaned_data[week_day[i]]
                        if hours != 0:
                            timeentry = TimeEntry(project=project, hours=hours, user=request.user,
                                                  reg_date=monday + ((i - 1) * delta),
                                                  timesheet=timesheet)
                            timeentry.save()
            return render_to_response('timesheet/timesheet_list.html')
    else:
        formset = load_timesheet(request, week_number, year)
    return render_to_response('timesheet/timesheet_form.html', {'formset': formset},
                              context_instance=RequestContext(request))


@login_required
def load_timesheet(request, week_number, year):
    data = {
        'form-INITIAL_FORMS': u'0',
        'form-MIN_NUM_FORMS': u'',
        'form-MAX_NUM_FORMS': u'',
        'form-0-project': u'1',
        'form-0-mon': u'0',
        'form-0-tue': u'0',
        'form-0-wed': u'0',
        'form-0-thu': u'0',
        'form-0-fri': u'0',
        'form-0-sat': u'0',
        'form-0-sun': u'0',
    }
    try:
        timesheet = Timesheet.objects.get(week_number=week_number, year=year, user=request.user)
        timeentries = timesheet.timeentry_set.all()
        projects = timeentries.order_by('project').distinct()
        if projects.count() == 0:
            data['form-TOTAL_FORMS'] = u'1'
        else:
            data['form-TOTAL_FORMS'] = u'' + str(projects.count()) + ''
        project_index = 0
        for project in projects:
            data['form-' + str(project_index) + '-project'] = u'' + str(project.id) + ''
            for day in range(1, 7):
                hours = 0
                for timeentry in timeentries:
                    if timeentry.project.id == project.id and day == timeentry.reg_date.isoweekday():
                        hours = timeentry.hours
                data['form-' + str(project_index) + '-' + str(week_day[day])] = u'' + str(hours) + ''
            project_index += 1
        timesheetFormSet = django.forms.formsets.formset_factory(TimesheetForm)
        return timesheetFormSet(data)
    except Timesheet.DoesNotExist:
        data['form-TOTAL_FORMS'] = u'1'
        timesheetFormSet = django.forms.formsets.formset_factory(TimesheetForm)
        return timesheetFormSet()
