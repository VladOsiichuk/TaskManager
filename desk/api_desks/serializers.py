from rest_framework import serializers
from desk.model import Desk
from django.db import models


class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ['author', 'description', 'name']

        read_only_fields = ['author']
