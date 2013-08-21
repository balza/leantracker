from django.views.generic.edit import CreateView
from leantracker.timesheet.forms import TimesheetForm


class TimesheetCreateView(CreateView):
    form_class = TimesheetForm
    template_name = 'timesheet/timesheet_form.html'
    success_url = 'success'

    def form_invalid(self, form):
        return http.HttpResponse("form is invalid.. this is just an HttpResponse object")
