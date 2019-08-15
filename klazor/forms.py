from django.forms import ModelForm
from klazor.models import *


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'topic_set', 'instructor_set', 'year']
