from rest_framework.generics import get_object_or_404

from desk.model import Desk
from .serializers import DeskSerializer
from rest_framework import generics
from rest_framework import mixins, permissions
from rest_framework.authentication import SessionAuthentication
from api_rules.models import PermissionRow
from user_auth.models import UsersDesks
from rest_framework import status
from rest_framework.response import Response
from api_rules.permissions import IsAdminOfDesk, IsEditorOfDeskOrHigher, IsStaffOfDeskOrHigher
from redis_manager.permission_cache_manager import PermissionCacheManager
from desk.actions.actions_data import get_columns_and_users, get_comments


class DeskAPIView(generics.ListAPIView,
                  mixins.CreateModelMixin,
                  ):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = DeskSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'desk_id'
    queryset = Desk.objects.prefetch_related('columns__tasks').all()

    # disable pagination
    paginator = None

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    # def get(self, request, *args, **kwargs):
    #     return self.get_list(request, *args, **kwargs)

    # def get_queryset(self):
    #     request = self.request
    #
    #     # Show only Desks in which user is participant
    #     users_qs = Desk.objects.prefetch_related('columns__tasks')\
    #         .prefetch_related("permissionrow_set__user").filter(permissionrow__user=request.user)
    #
    #     return users_qs

    def list(self, request, *args, **kwargs):
        current_user = request.user

        # Show only Desks in which user is participant
        queryset = self.queryset.filter(permissionrow__user=current_user)
        serializer = self.get_serializer(queryset, many=True)

        # Add permissions of user for requested desks
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Create a new Desk. Everyone can create a desk. But user should be logged in.
        """

        # create Desk object
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        desk_object = self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        # create relation between user and desk
        rel = UsersDesks.objects.create(user=request.user, desks=desk_object)
        rel.save()

        p = PermissionRow.objects.create(related_desk=desk_object, user=request.user, permission="ADMIN")
        p.save()

        # UPDATE CACHE
        PermissionCacheManager.update_cache_of_user(user_id=request.user.id, permission="ADMIN", desk_id=desk_object.id)

        # return success response
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DeskDetailAPIView(mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.RetrieveAPIView,
                        ):

    authentication_classes = [SessionAuthentication]
    queryset = Desk.objects.prefetch_related("columns__tasks", "usersdesks_set__user").all()
    serializer_class = DeskSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'desk_id'

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        if self.request.method == "GET":
            permission_classes.append(IsStaffOfDeskOrHigher)
        else:
            permission_classes.append(IsEditorOfDeskOrHigher)
        return [permission() for permission in self.permission_classes]

    def retrieve(self, request, *args, **kwargs):
        instance = self.queryset.filter(id=self.kwargs[self.lookup_url_kwarg]).first()
        serializer = self.get_serializer(instance)
        new_data = get_user_perm_for_desk(request.user, serializer.data)
        new_data = get_additional_data(new_data, instance)
        return Response(new_data)

    def put(self, request, *args, **kwargs):
        """Update the Desk(Only Desk, not Comments or Columns or Tasks)"""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Update the Desk(Only Desk, not Comments or Columns or Tasks)"""
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete the board. Only ADMIN can delete board"""
        self.permission_classes = [IsAdminOfDesk]
        return self.destroy(request, *args, **kwargs)


def get_user_perm_for_desk(user, serializer_data):
    """
    :param user: Who requests information about desks
    :param serializer_data: serialized data about desks
    :param obj: Desk instance
    :return: updated serialized data which contains permissions of user to each desk
    """

    permissions_dict = {
        "ADMIN": {
            "ROLE": "ADMIN",
            "DO_ALL": True,
            "DELETE_COMMENTS": False
        },
        "EDITOR": {
            "ROLE": "EDITOR",
            "DO_ALL": False,
            "UPDATE_DESK": True,
            "DELETE_DESK": False,
            "UPDATE_COLUMN": True,
            "DELETE_COLUMN": True,
            "CREATE_COLUMN": True,
            "CREATE_TASK": True,
            "UPDATE_TASK": True,
            "DELETE_TASK": True,
            "ADD_COMMENT": True,
            "ADD_USER": True,
            "DELETE_USER": True,
            "UPDATE_PERMISSION": True,
            "DELETE_COMMENTS": False

        },
        "STAFF": {
            "ROLE": "STAFF",
            "DO_ALL": False,
            "UPDATE_DESK": True,
            "DELETE_DESK": False,
            "UPDATE_COLUMN": False,
            "DELETE_COLUMN": False,
            "CREATE_COLUMN": False,
            "CREATE_TASK": False,
            "UPDATE_TASK": None,
            "DELETE_TASK": False,
            "ADD_COMMENT": True,
            "ADD_USER": False,
            "DELETE_USER": False,
            "UPDATE_PERMISSION": False,
            "DELETE_COMMENTS": False
        }
    }

    users_dict = PermissionCacheManager.get_user_perms(user.id)
    perm = users_dict[serializer_data['id']]
    serializer_data['permissions_of_current_user_for_this_desk'] = permissions_dict[perm]
    return serializer_data


def get_additional_data(serialized_data, obj):
    """
    :param serialized_data: serialized_data
    :param obj: desk obj
    :return: attach additional data to tasks.
    """

    users = obj.usersdesks_set.all()
    columns = obj.columns.all()
    columns_data = [{"id": row.id, "name": row.name} for row in columns]
    data = []
    for row in users:
        data.append({"user_id": row.user.id,
                     "username": row.user.username,
                     "email": row.user.email})

    serialized_data['users'] = data
    for row in range(len(serialized_data['columns'])):
        for task in range(len(serialized_data['columns'][row]['tasks'])):
            # add users to tasks
            serialized_data['columns'][row]['tasks'][task]['users'] = data
            # add columns to tasks
            serialized_data['columns'][row]['tasks'][task]['columns'] = columns_data

    return serialized_data
