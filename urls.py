from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'leantracker.views.home', name='home'),
    # url(r'^leantracker/', include('leantracker.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'django.contrib.auth.views.login', name="home"),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^timesheet/', include('timesheet.urls', namespace='timesheet', app_name='timesheet')),
    url(r'^holidaysplanner/', include('holidaysplanner.urls', namespace='holidaysplanner', app_name='holidaysplanner')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
