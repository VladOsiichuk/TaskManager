from rest_framework import serializers
from desk.model import Task, Desk
import datetime
from desk.api_comments.serializers import CommentSerializer
from desk.model import Comment


# class to create New tasks
class CreateTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'id',
            'related_column',
            'name',
            'description',
            'task_deadline',
            'current_executor',
            'priority',
            'image',
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
    comments_url = serializers.SerializerMethodField(read_only=True)
    # comments = serializers.HyperlinkedRelatedField(source=Comment.objects.filter(related_task=Task),
    #                                                read_only=True,
    #                                                many=True,
    #                                                #view_name='dd'
    #                                                #lookup_field='id'
    #                                                )
    #Task.objects.prefetch_related("comments")

    class Meta:
        model = Task
        fields = [
            'id',
            'related_column',
            'name',
            'description',
            'task_deadline',
            'current_executor',
            'priority',
            'image',
            'comments_url',
        ]

        read_only_fields = [
            'id',
        ]

    def get_comments_url(self, obj):
        request = self.context.get("request")
        return request.path + "comments/"

    # Check if deadline is later or equal to today's date
    def validate_task_deadline(self, value):
        today = datetime.date.today()
        print(value.year, value.month, value.day)
        print(today.year, today.month, today.day)
        if today.year > value.year:
            raise serializers.ValidationError("Deadline should be later or equal to today's date")
        elif today.year == value.year:
            if today.month > value.month:
                raise serializers.ValidationError("Deadline should be later or equal to today's date")
            elif today.month == value.month:
                if today.day > value.day:
                    raise serializers.ValidationError("Deadline should be later or equal to today's date")

        return value
