from django.db import models
from django.contrib.auth.models import Group

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

    class Meta:
        permissions = (
            ("can_admin_project", "Can admin Projects"),
        )

