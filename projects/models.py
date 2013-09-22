from django.db import models
from django.db.models import Manager
from django.contrib.auth.models import Group

#Valuta anche il Project.objects.filter(groups=???)
class GroupProjectManager(Manager):
    def get_queryset(self):
        return super(ProjectGroupManager, self).get_queryset()

class Project(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(help_text="Use 'auto' or an empty field to get an unique project code", max_length=30, unique=True, blank=True)
    enabled = models.BooleanField()
    expire = models.DateField(null=True)
    public = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.code)

    def save(self, *args, **kwargs):
        super(Project, self).save(*args, **kwargs)
        if self.code == 'auto' or self.code == "":
            self.code = self.id
            super(Project, self).save(*args, **kwargs)

    group_projects = GroupProjectManager() 
    objects = Manager()
   
    class Meta:
        permissions = (
            ("can_admin_project", "Can admin Projects"),
        )
