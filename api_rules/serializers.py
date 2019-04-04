from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PermissionRow

User = get_user_model()


class PermissionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(help_text='email of the user', write_only=True)

    class Meta:
        model = PermissionRow
        fields = [
            'id',
            'email',
            'permission',
        ]

    @staticmethod
    def validate_email(value):
        print("FROM VALIDATE", value)
        user = User.objects.filter(email=value).first()
        if user is None:
            raise serializers.ValidationError("User with this email does not exist")

        # return user id in order to create a new PermissionRow
        return user.id

    @staticmethod
    def validate_permission(value):
        if value.upper() != "STAFF" and value.upper() != "EDITOR":
            raise serializers.ValidationError("Permission should be STAFF or EDITOR")
        return value

    def create(self, validated_data):

        obj = PermissionRow.objects.create(user_id=validated_data['email'],
                                           permission=validated_data['permission'],
                                           related_desk_id=validated_data['related_desk_id'])
        obj.save()
        return obj


class UpdatePermissionRowSerializer(serializers.ModelSerializer):

    #email = serializers.EmailField(help_text='email of the user', write_only=True)

    class Meta:
        model = PermissionRow
        fields = [
            'id',
            'user',
            'permission'
        ]

    @staticmethod
    def validate_permission(value):
        if value.upper() != "STAFF" and value.upper() != "EDITOR":
            raise serializers.ValidationError("Permission should be STAFF or EDITOR")
        return value

