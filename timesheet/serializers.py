from rest_framework import serializers
from timesheet.models import TimeEntry,Timesheet
from projects.models import Project
from django.contrib.auth.models import User


class TimeEntrySerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    hours = serializers.IntegerField()
    user_id = serializers.IntegerField()
    reg_date = serializers.DateField()
    timesheet_id = serializers.IntegerField()

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.project = attrs.get('project_id', instance.project_id)
            instance.hours = attrs.get('hours', instance.week_number)
            instance.reg_date = attrs.get('reg_date', instance.reg_date)
            instance.user_id = attrs.get('user_id', instance.user_id)
            instance.timesheet_id = attrs.get('timesheet_id', instance.timesheet_id)
            return instance
        return TimeEntry(**attrs)
