from rest_framework import serializers
from klazor import models


class SheetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Sheet
        fields = ('title', )