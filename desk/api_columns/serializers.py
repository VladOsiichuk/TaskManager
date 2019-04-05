from rest_framework import serializers
from desk.model import Column
from django.db import models
from desk.api_tasks.serializers import CreateTaskSerializer, UpdateTaskSerializer


class ColumnSerializer(serializers.ModelSerializer):
    tasks = UpdateTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Column
        fields = ['id', 'author', 'name', 'related_desk', 'created', 'tasks']
        ordering = ['-id']

        read_only_fields = ['author', 'created', 'id', 'related_desk']
