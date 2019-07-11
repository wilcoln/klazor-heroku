from rest_framework import viewsets
from api.serializers import *
# Create your views here.


class TopicViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows sheets to be viewed or edited.
        """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class InstructorViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows sheets to be viewed or edited.
        """
    queryset = Instructor.objects.all()
    serializer_class = DynamicInstructorSerializer


class SheetViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows sheets to be viewed or edited.
        """
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer


class CellViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows sheets to be viewed or edited.
        """
    queryset = Cell.objects.all()
    serializer_class = DynamicCellSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows sheets to be viewed or edited.
        """
    queryset = Course.objects.all()
    serializer_class = DynamicCourseSerializer


class MoocCourseViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows sheets to be viewed or edited.
        """
    queryset = MoocCourse.objects.all()
    serializer_class = MoocCourseSerializer


class SchoolCourseViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows sheets to be viewed or edited.
        """
    queryset = SchoolCourse.objects.all()
    serializer_class = SchoolCourseSerializer


class CoursePartViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows sheets to be viewed or edited.
        """
    queryset = CoursePart.objects.all()
    serializer_class = CoursePartSerializer


class FileItemViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows sheets to be viewed or edited.
        """
    queryset = FileItem.objects.all()
    serializer_class = FileItemSerializer
