from rest_framework import serializers
from klazor.models import *


class FileItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileItem
        fields = ('id', 'title', 'file',)


class DynamicCellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = ()

    def to_representation(self, obj):
        if isinstance(obj, MarkdownCell):
            return MarkdownCellSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, ImageCell):
            return ImageCellSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, VideoCell):
            return VideoCellSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, YoutubeCell):
            return YoutubeCellSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, AudioCell):
            return AudioCellSerializer(obj, context=self.context).to_representation(obj)


class SheetSerializer(serializers.HyperlinkedModelSerializer):
    cell_set = DynamicCellSerializer(required=False, many=True)  # May be an anonymous user.

    class Meta:
        model = Sheet
        fields = ('id', 'title', 'cell_set')


class CellSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cell
        fields = ()


class MarkdownCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = MarkdownCell
        fields = ('id', 'sequence', 'text',)


class VideoCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = VideoCell
        fields = ('id', 'sequence', 'title', 'video', 'scale')


class YoutubeCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = YoutubeCell
        fields = ('id', 'sequence', 'title', 'youtube', 'scale')


class ImageCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = ImageCell
        fields = ('id', 'sequence', 'title', 'image', 'scale')


class AudioCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = AudioCell
        fields = ('id', 'sequence', 'title', 'audio')


class CourseElementSerializer(SheetSerializer):
    class Meta(SheetSerializer.Meta):
        model = CourseElement
        fields = ('id', 'sequence', 'title', 'cell_set')


class CoursePartSerializer(serializers.ModelSerializer):
    courseelement_set = CourseElementSerializer(many=True)

    class Meta:
        model = CoursePart
        fields = ('id', 'level', 'sequence', 'label', 'title', 'courseelement_set', )


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'title', 'subtopic_set')


class DynamicCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ()

    def to_representation(self, obj):
        if isinstance(obj, MoocCourse):
            return MoocCourseSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, SchoolCourse):
            return SchoolCourseSerializer(obj, context=self.context).to_representation(obj)


class DynamicInstructorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Instructor
        fields = ()

    def to_representation(self, obj):
        if isinstance(obj, NotSchool):
            return NotSchoolSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, School):
            return SchoolSerializer(obj, context=self.context).to_representation(obj)


class CourseSerializer(serializers.ModelSerializer):
    coursepart_set = CoursePartSerializer(many=True)
    topic_set = TopicSerializer(many=True)
    instructor_set = DynamicInstructorSerializer(many=True)
    resource_set = FileItemSerializer(many=True)

    class Meta:
        model = Course
        fields = ()


class InstructorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Instructor
        fields = ()


class SchoolSerializer(InstructorSerializer):
    class Meta(InstructorSerializer.Meta):
        model = School
        fields = ('id', 'name', 'link', 'colloquial_name', )


class NotSchoolSerializer(InstructorSerializer):
    class Meta(InstructorSerializer.Meta):
        model = NotSchool
        fields = ('id', 'name', 'link', )


class SchoolCourseSerializer(CourseSerializer):
    class Meta(CourseSerializer.Meta):
        model = SchoolCourse
        fields = ('id', 'title', 'topic_set', 'coursepart_set', 'year', 'semester', 'instructor_set', 'resource_set', )


class MoocCourseSerializer(CourseSerializer):
    class Meta(CourseSerializer.Meta):
        model = MoocCourse
        fields = ('id', 'title', 'topic_set', 'coursepart_set', 'instructor_set', 'resource_set')



