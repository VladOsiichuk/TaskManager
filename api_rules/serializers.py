from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PermissionRow

User = get_user_model()


class PermissionSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(help_text='email of the user', write_only=True)

    class Meta:
        model = PermissionRow
        fields = [
            'email',
            'user',
            'permission',
        ]
        read_only_fields = ['user']

    def validate_email(self, value, *args, **kwargs):

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

    def validate(self, attrs):
        request = self.context.get('request')
        dict = request.parser_context.get('kwargs')
        desk_id = dict['desk_id']
        user_id = attrs.pop('email')
        attrs.__setitem__('user', user_id)
        row = PermissionRow.objects.filter(user_id=user_id, related_desk_id=desk_id)
        if row.exists():
            raise serializers.ValidationError("This user is already participant of desk.")

        return attrs

    def create(self, validated_data):

        obj = PermissionRow.objects.create(user_id=validated_data['user'],
                                           permission=validated_data['permission'].upper(),
                                           related_desk_id=validated_data['related_desk_id'])
        obj.save()
        return obj


class UpdatePermissionRowSerializer(serializers.ModelSerializer):

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
