from rest_framework import serializers
from django.contrib.auth import get_user_model
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
    #add_to_permission = serializers.CharField(help_text='Enter STAFF or EDITOR')#CustomGroupSerializer(many=True, read_only=True)
    desk_name = serializers.CharField(help_text='Name of the desk')
    #user = UserRegisterSerializer(many=True)
    #group_set = serializers.SerializerMethodField()
    #add_to = serializers.CharField(help_text='STAFF/EDITORS')

    class Meta:
        model = User
        fields = [
            'id',
            #'username',
            #'add_to'
            #'email',
            #'related_desk',
            #'user_id'
            #'desk_id',
            #'customgroup_set',
            #'group_set',
            #'add_to_permission',
            'desk_name'

        ]

    #def create(self, validated_data):
     #   pass
    # # def get_group_set(self, obj):
    #     request = self.context.get('request')
    #     #print(request)
    #     #srl = CustomGroupSerializer()
    #     #qs = obj.desk_set.all()
    #     groups = obj.customgroup_set.all()
    #     data = CustomGroupSerializer(groups, many=True, context={'request': request}).data
    #     return data
