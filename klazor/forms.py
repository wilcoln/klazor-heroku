from django import forms
from klazor.models import *


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'tag_set', 'instructor_set', 'release_date']
