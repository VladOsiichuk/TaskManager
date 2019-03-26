from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = get_user_model().objects.create(username=validated_data['username'],
                                               password=make_password(validated_data['password']),
                                               email=validated_data['email'],
                                               first_name=validated_data['first_name'],
                                               last_name=validated_data['last_name'])
        user.save()
        return user
