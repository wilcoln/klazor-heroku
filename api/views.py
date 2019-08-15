from rest_framework import viewsets, permissions
from api.serializers import *
from api.permissions import *
# Create your views here.


class TopicViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows topics to be viewed or edited.
        """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class InstructorViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows instructors to be viewed or edited.
        """
    queryset = Instructor.objects.all()
    serializer_class = DynamicInstructorSerializer


class SheetViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows sheets to be viewed or edited.
        """
    permission_classes = [permissions.IsAuthenticated,
                          IsOwner]
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer

    def get_queryset(self):
        return Sheet.objects.all().filter(user=self.request.user)


class CellViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows cells to be viewed or edited.
        """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Cell.objects.all()
    serializer_class = DynamicCellSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows courses to be viewed or edited.
        """
    permission_classes = [permissions.IsAuthenticated,
                          IsOwner]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.all().filter(user=self.request.user)


class CoursePartViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows course parts to be viewed or edited.
        """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CoursePart.objects.all()
    serializer_class = CoursePartSerializer


class FileItemViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows file items to be viewed or edited.
        """
    permission_classes = [permissions.IsAuthenticated,
                          IsOwner]
    queryset = FileItem.objects.all()
    serializer_class = FileItemSerializer
