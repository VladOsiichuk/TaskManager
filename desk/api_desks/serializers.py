from rest_framework import serializers
from desk.model import Desk
from django.db import models
from desk.api_columns.serializers import ColumnSerializer


class DeskSerializer(serializers.ModelSerializer):
    columns =ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = Desk
        fields = [
            'id', 
            'author',
            'description',
            'name',
            'columns',
        ]
        read_only_fields = ['author']
