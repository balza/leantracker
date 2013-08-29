from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView, CreateView
from leantracker.timesheet.models import Timesheet
from leantracker.timesheet.views import create_timesheet

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=Timesheet.objects.order_by('-id')[:5],
            context_object_name='timesheet_list',
            template_name='timesheet/index.html',
        ),
        name="list"
    ),
    url(r'^create/$', create_timesheet, name="create"),
)

