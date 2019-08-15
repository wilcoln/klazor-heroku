from rest_framework import serializers
from klazor.models import *


class FileItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileItem
        fields = ('id', 'title', 'file',)


class PropositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposition
        fields = ('id', 'statement', 'is_true')


class MultipleChoiceQuestionCellSerializer(serializers.ModelSerializer):
    proposition_set = PropositionSerializer(required=False, many=True)

    class Meta:
        model = MultipleChoiceQuestionCell
        fields = ('id', 'sequence', 'proposition_set')


class NumericalQuestionCellSerializer(serializers.ModelSerializer):
    class Meta:
        model = NumericalQuestionCell
        fields = ('id', 'sequence', 'answer')


class OpenEndedQuestionCellSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenEndedQuestionCell
        fields = ('id', 'sequence', 'answer')


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
        elif isinstance(obj, FileCell):
            return FileCellSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, MultipleChoiceQuestionCell):
            return MultipleChoiceQuestionCellSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, NumericalQuestionCell):
            return NumericalQuestionCellSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, OpenEndedQuestionCell):
            return OpenEndedQuestionCellSerializer(obj, context=self.context).to_representation(obj)


class SheetSerializer(serializers.HyperlinkedModelSerializer):
    cell_set = DynamicCellSerializer(required=False, many=True)  # May be an anonymous user.

    class Meta:
        model = Sheet
        fields = ('id', 'title', 'cell_set', 'updated_at')


class CellSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cell
        fields = ()


class MarkdownCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = MarkdownCell
        fields = ('id', 'sequence', 'text',)


class FileCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = FileCell
        fields = ('id', 'sequence', 'title', 'file',)


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
        fields = ('id', 'level', 'sequence', 'label', 'title', 'courseelement_set',)


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ('id', 'title', 'subtopic_set')


class DynamicInstructorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Instructor
        fields = ()

    def to_representation(self, obj):
        if isinstance(obj, School):
            return SchoolSerializer(obj, context=self.context).to_representation(obj)
        else:
            return InstructorSerializer(obj, context=self.context).to_representation(obj)


class CourseSerializer(serializers.ModelSerializer):
    coursepart_set = CoursePartSerializer(many=True)
    topic_set = TopicSerializer(many=True)
    instructor_set = DynamicInstructorSerializer(many=True)
    resource_set = FileItemSerializer(many=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'topic_set', 'coursepart_set', 'instructor_set', 'resource_set', 'year')


class InstructorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Instructor
        fields = ('id', 'name', 'link',)


class SchoolSerializer(InstructorSerializer):
    class Meta(InstructorSerializer.Meta):
        model = School
        fields = ('id', 'name', 'link', 'colloquial_name',)
