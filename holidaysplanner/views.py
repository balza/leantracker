from django.contrib.auth.models import User
from django.contrib.auth.models import GroupManager, Group
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required


#http://stackoverflow.com/questions/1052531/get-user-group-in-a-view
def get_user_groups(user):
    return user.groups.all()

def get_users_in_groups(group):
    return group.user_set.all()

@login_required
def load(self):
    print 'View'
    return render_to_response('holidaysplanner/holidaysplanner.html')
