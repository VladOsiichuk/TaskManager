from rest_framework import serializers
from desk.model import Task, Desk
import datetime
from desk.api_comments.serializers import CommentSerializer


# class to create New tasks
class CreateTaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'related_column',
            'name',
            'description',
            'task_deadline',
            'current_executor',
            'comments'
        ]

        read_only_fields = [
            'id',
            'related_column'
        ]

    # Check if deadline is later or equal to today's date
    def validate_task_deadline(self, value):
        today = datetime.date.today()
        if today.year > value.year or today.month > value.month:
            raise serializers.ValidationError("Deadline should be later or equal to today's date")
        return value


# class to update tasks
class UpdateTaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'related_column',
            'name',
            'description',
            'task_deadline',
            'current_executor',
            'comments',
        ]

        read_only_fields = [
            'id',
        ]

    # Check if deadline is later or equal to today's date
    def validate_task_deadline(self, value):
        today = datetime.date.today()
        if today.year > value.year or today.month > value.month:
            raise serializers.ValidationError("Deadline should be later or equal to today's date")
        return value
