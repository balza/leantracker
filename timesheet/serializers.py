from rest_framework import serializers
from timesheet.models import TimeEntry,Timesheet
from projects.models import Project
from django.contrib.auth.models import User


class TimeEntrySerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    hours = serializers.IntegerField()
    username = serializers.CharField()
    reg_date = serializers.DateField()
    timesheet_id = serializers.IntegerField()

    def restore_object(self, attrs, instance=None):
        if instance:
            project_id = attrs.get('project_id')
            instance.project = Project.objects.get(project_id)
            instance.hours = attrs.get('hours', instance.week_number)
            instance.reg_date = attrs.get('reg_date', instance.reg_date)
            username = attrs.get('username')
            instance.user = User.objects.get(username)
            timesheet_id = attrs.get('timesheet_id')
            instance.timesheet = Timesheet.objects.get(timesheet_id)
            return instance
        return TimeEntry(**attrs)
