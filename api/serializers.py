from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from klazor.models import *


class FileItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileItem
        fields = ('id', 'title', 'file',)


class PropositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposition
        fields = ('id', 'statement', 'is_true')


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
        elif isinstance(obj, MultipleChoiceInputCell):
            return MultipleChoiceInputCellSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, NumericalInputCell):
            return NumericalInputCellSerializer(obj, context=self.context).to_representation(obj)
        elif isinstance(obj, OpenEndedInputCell):
            return OpenEndedInputCellSerializer(obj, context=self.context).to_representation(obj)


class SheetSerializer(serializers.HyperlinkedModelSerializer):
    cell_set = DynamicCellSerializer(required=False, many=True)  # May be an anonymous user.

    class Meta:
        model = Sheet
        fields = ('id', 'title', 'cell_set', 'updated_at')


class CellSerializer(serializers.HyperlinkedModelSerializer):
    type = ReadOnlyField()

    class Meta:
        model = Cell
        fields = ()


class MarkdownCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = MarkdownCell
        fields = ('id', 'sequence', 'type', 'text',)


class FileCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = FileCell
        fields = ('id', 'sequence', 'type', 'title', 'url',)


class VideoCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = VideoCell
        fields = ('id', 'sequence', 'type', 'title', 'url', 'scale')


class YoutubeCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = YoutubeCell
        fields = ('id', 'sequence', 'type', 'title', 'url', 'scale')


class ImageCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = ImageCell
        fields = ('id', 'sequence', 'type', 'title', 'url', 'scale')


class AudioCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = AudioCell
        fields = ('id', 'sequence', 'type', 'title', 'url')


class MultipleChoiceInputCellSerializer(CellSerializer):
    proposition_set = PropositionSerializer(required=False, many=True)

    class Meta(CellSerializer.Meta):
        model = MultipleChoiceInputCell
        fields = ('id', 'sequence', 'type', 'proposition_set')


class NumericalInputCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = NumericalInputCell
        fields = ('id', 'sequence', 'type', 'answer')


class OpenEndedInputCellSerializer(CellSerializer):
    class Meta(CellSerializer.Meta):
        model = OpenEndedInputCell
        fields = ('id', 'sequence', 'type', 'answer')


class CourseElementSerializer(SheetSerializer):
    class Meta(SheetSerializer.Meta):
        model = CourseElement
        fields = ('id', 'sequence', 'title', 'cell_set')


class CoursePartSerializer(serializers.ModelSerializer):
    courseelement_set = CourseElementSerializer(many=True)

    class Meta:
        model = CoursePart
        fields = ('id', 'level', 'sequence', 'label', 'title', 'courseelement_set',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


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
    tag_set = TagSerializer(many=True)
    instructor_set = DynamicInstructorSerializer(many=True)
    resource_set = FileItemSerializer(many=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'tag_set', 'coursepart_set', 'instructor_set', 'resource_set', 'release_date')


class InstructorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Instructor
        fields = ('id', 'name', 'link',)


class SchoolSerializer(InstructorSerializer):
    class Meta(InstructorSerializer.Meta):
        model = School
        fields = ('id', 'name', 'link', 'colloquial_name',)
