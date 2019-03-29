from rest_framework import serializers
from desk.model import Desk
from django.db import models


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ['id', 'author', 'name', 'related_desk', 'created']

        read_only_fields = ['author', 'created']
