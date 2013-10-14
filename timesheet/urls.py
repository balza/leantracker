from django.conf.urls import *
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from leantracker.timesheet.models import Timesheet
from leantracker.timesheet.views import timesheet


# Important: authentication, as often in django, It's a little bit alien for a java programmer,
# seems .html pages mix responsabilities with url.py
#   ref https://docs.djangoproject.com/en/1.5/topics/auth/default/#module-django.contrib.auth.views

urlpatterns = patterns('',
                       url(r'^$', 'django.contrib.auth.views.login', name="home"),
                       url(r'^logout/$', 'django.contrib.auth.views.logout'),
                       url(r'^list/$',
                           login_required(ListView.as_view(
                               queryset=Timesheet.objects.order_by('-id')[:5],
                               context_object_name='timesheet_list',
                           )),
                           name="list"),
                       url(r'^load/(?P<year>\d+)/(?P<week_number>\d+)/$', timesheet, name="load"),
)

