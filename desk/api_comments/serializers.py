from rest_framework import serializers
from desk.model import Comment
import datetime
import json


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


# class to create New tasks
class CommentSerializer(serializers.ModelSerializer):
    related_comment = RecursiveField(many=True)
    author = serializers.CharField(source="author.username")

    class Meta:
        model = Comment
        # list_serializer_class = FilteredListSerializer
        fields = [
            'id',
            'author',
            'related_task',
            'image',
            'comment_body',
            'is_child',
            'related_comment',

        ]

        read_only_fields = [
            'id',
            'related_task',
            'author',
        ]
        ordering = ['-id']


class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "related_task",
            "comment_body",
            "is_child",
            'image',
            "parent"
        ]

        read_only_fields = [
            "id",
            "related_task",
            "author"
        ]
        ordering = ['-id']
