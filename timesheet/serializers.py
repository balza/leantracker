from rest_framework import serializers
from timesheet.models import TimeEntry


class TimeEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TimeEntry
        fields = ('project', 'hours', 'user','reg_date','timesheet')