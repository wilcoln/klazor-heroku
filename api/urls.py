from django.urls import include, path
from rest_framework import routers
from api.views import *

router = routers.DefaultRouter()
router.register(r'sheet', SheetViewSet)
router.register(r'cell', CellViewSet)
router.register(r'instructor', InstructorViewSet)
router.register(r'mooc-course', MoocCourseViewSet)
router.register(r'school-course', SchoolCourseViewSet)
router.register(r'course', CourseViewSet)
router.register(r'sheet', SheetViewSet)
router.register(r'course-part', CoursePartViewSet)
router.register(r'file', FileItemViewSet)
router.register(r'topic', TopicViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]