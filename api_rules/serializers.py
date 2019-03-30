from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import PermissionRow
from user_auth.models import CustomGroup
from desk.model import Desk
from user_auth.serializers import UserRegisterSerializer
from desk.api_desks.serializers import DeskSerializer
from user_auth.serializers import CustomGroupSerializer
User = get_user_model()


class UpdateUserPermissionsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(help_text='INT. ID of user for who to change permissions ')
    desk_id = serializers.IntegerField(help_text='INT. ID of Desk for who to change user\'s permissions')
    change_to_permission = serializers.CharField(help_text='STRING. Name of permission(EDITOR or STAFF)')
    change_from_permission = serializers.CharField(default=None,
                                                   help_text='If user already have some rules in tnis Desk, '
                                                             'then provide his previous permission')


class AddUserToDeskSerializer(serializers.ModelSerializer):

    #user_id = serializers.IntegerField(help_text='INT. ID of user for who to change permissions ')
    #desk_id = serializers.IntegerField(help_text='INT. ID of Desk for who to change user\'s permissions')
    set_to_permission = serializers.CharField(help_text='Enter STAFF or EDITOR', write_only=True)#CustomGroupSerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(help_text='ID of the user', write_only=True)
    #set_permission = serializers.CharField(help_text='Name of the desk')
    #user = UserRegisterSerializer(many=True)
    #group_set = serializers.SerializerMethodField()
    #add_to = serializers.CharField(help_text='STAFF/EDITORS')
    #participants = UserRegisterSerializer(read_only=True)
    class Meta:
        model = Desk
        fields = [
            'id',
            #'permission',
            #'author',
            #'related_desk'
            #'related_desk'
            #'username',
            #'add_to'
            #'email',
            #'related_desk',
            #'participants',
            'user_id',
            #'desk_id',
            #'customgroup_set',
            #'group_set',
            #'add_to_permission',
            'set_to_permission',
        ]

    def validate_set_to_permission(self, value):

        if value.upper() != "STAFF" and value.upper() != "EDITOR":
            raise serializers.ValidationError("Permission should be STAFF or EDITOR")

    def validate_user_id(self, value):
        if not isinstance(int, value):
            raise serializers.ValidationError("user_id should be int")

    #     return value
    # def create(self, validated_data):
    #     pass
    # # def get_group_set(self, obj):
    #     request = self.context.get('request')
    #     #print(request)
    #     #srl = CustomGroupSerializer()
    #     #qs = obj.desk_set.all()
    #     groups = obj.customgroup_set.all()
    #     data = CustomGroupSerializer(groups, many=True, context={'request': request}).data
    #     return data
