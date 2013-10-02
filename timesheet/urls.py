from django.conf.urls import *
from django.views.generic import ListView
from leantracker.timesheet.models import Timesheet
from leantracker.timesheet.views import create_timesheet, submit_timesheet

urlpatterns = patterns('',
                       url(r'^$',
                           ListView.as_view(
                             queryset=Timesheet.objects.order_by('-id')[:5],
                             context_object_name='timesheet_list',
                             template_name='timesheet/index.html',
                           ),
                           name="list"
                       ),
                       url(r'^create/(?P<year>\d+)/(?P<week_number>\d+)/$', create_timesheet, name="create"),
                       url(r'^submit/(?P<year>\d+)/(?P<week_number>\d+)/$', submit_timesheet, name="submit"),
)

