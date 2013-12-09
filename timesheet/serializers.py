from rest_framework import serializers
from timesheet.models import TimeEntry


class TimeEntrySerializer(serializers.Serializer):
    hours = serializers.IntegerField()
    reg_date = serializers.DateField()

    def restore_object(self, attrs, instance=None):
        if instance:
            # Update existing instance
            instance.hours = attrs.get('hours', instance.week_number)
            instance.reg_date = attrs.get('reg_date', instance.reg_date)
            return instance
        return TimeEntry(**attrs)
