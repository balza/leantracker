from django.conf.urls import *
from django.views.generic import ListView
from leantracker.timesheet.models import Timesheet
from leantracker.timesheet.views import create_timesheet, submit_timesheet
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
                       url(r'^$', 'django.contrib.auth.views.login'),
                       url(r'^list/$',
                           #login_required(ListView.as_view(
                           ListView.as_view(
                             queryset=Timesheet.objects.order_by('-id')[:5],
                             context_object_name='timesheet_list',
                             template_name='timesheet/index.html',
                            ),
                           #)),
                           name="list",
                       ),
                       url(r'^create/(?P<year>\d+)/(?P<week_number>\d+)/$', create_timesheet, name="create"),
                       url(r'^submit/(?P<year>\d+)/(?P<week_number>\d+)/$', submit_timesheet, name="submit"),
)

