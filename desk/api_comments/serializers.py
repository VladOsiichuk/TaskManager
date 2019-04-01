from rest_framework import serializers
from desk.model import Comment
import datetime


# class to create New tasks
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = [
            'id',
            'author',
            'related_task',
            'comment_body'
        ]

        read_only_fields = [
            'id',
            'related_task',
            'author'
        ]
