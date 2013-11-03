from django.contrib.auth.models import User
from django.contrib.auth.models import GroupManager, Group

#http://stackoverflow.com/questions/1052531/get-user-group-in-a-view
def get_user_groups(user):
    return user.objects.all()


