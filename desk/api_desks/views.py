from desk.model import Desk
from .serializers import DeskSerializer
from rest_framework import generics
from rest_framework import mixins, permissions
from rest_framework.authentication import SessionAuthentication
from api_rules.models import PermissionRow
from user_auth.models import UsersDesks
from rest_framework import status
from rest_framework.response import Response
from api_rules.permissions import IsAdminOfDesk, IsEditorOfDeskOrHigher


class DeskAPIView(generics.ListAPIView,
                  mixins.CreateModelMixin,
                  ):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    serializer_class = DeskSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'desk_id'
    queryset = Desk.objects.prefetch_related('columns__tasks').all()
            #.all()

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
        print("GGGGGGG")
        current_user = request.user

        # Show only Desks in which user is participant
        queryset = self.queryset.filter(permissionrow__user=current_user)

        serializer = self.get_serializer(queryset, many=True)

        # Add permissions of user for requested desks
        new_data = get_user_perm_for_desk(current_user, serializer.data, queryset)

        return Response(new_data)

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

        # return success response
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DeskDetailAPIView(mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.RetrieveAPIView,
                        ):

    permission_classes = [permissions.IsAuthenticated, IsEditorOfDeskOrHigher]
    authentication_classes = [SessionAuthentication]
    queryset = Desk.objects.prefetch_related("columns__tasks").all()
    serializer_class = DeskSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'desk_id'

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


def get_user_perm_for_desk(user, serializer_data, qs):
    """
    :param user: Who requests information about desks
    :param serializer_data: serialized data about desks
    :param qs: queryset of desks
    :return: updated serialized data which contains permissions of user to each desk
    """

    permissions_dict = {
        "ADMIN": {
            "DO_ALL": True,
        },
        "EDITOR": {
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

        },
        "STAFF": {
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
        }
    }

    for row in range(len(qs)):
        perm = qs[row].permissionrow_set.filter(user=user).first().permission
        serializer_data[row]['permissions_of_current_user_for_this_desk'] = permissions_dict[perm]

    return serializer_data
