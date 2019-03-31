from rest_framework import serializers
from desk.model import Column
from django.db import models


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'author', 'name', 'related_desk', 'created']

        read_only_fields = ['author', 'created', 'id', 'related_desk']
