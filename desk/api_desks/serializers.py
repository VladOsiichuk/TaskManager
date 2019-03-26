from rest_framework import serializers
from desk.model import Desk
from django.db import models


class DeskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Desk
        fields = ('description', 'name')
