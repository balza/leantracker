from rest_framework import viewsets
from projects.serializers import ProjectSerializer
from projects.models import Project

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
