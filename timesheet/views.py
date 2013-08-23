from django.views.generic.edit import FormView
from leantracker.timesheet.forms import TimesheetForm


class TimesheetView(FormView):
    form_class = TimesheetForm
    template_name = 'timesheet/timesheet_form.html'
    success_url = 'success'

    def form_invalid(self, form):
        return http.HttpResponse("form is invalid.. this is just an HttpResponse object")
