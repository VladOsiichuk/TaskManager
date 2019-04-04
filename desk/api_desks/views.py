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

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_queryset(self):
        request = self.request

        # Show only Desks in which user is participant
        users_qs = Desk.objects.prefetch_related('columns__tasks').filter(permissionrow__user=request.user)

        return users_qs

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

        # # create pool groups for permissions
        # staff_group = CustomGroup.objects.create(name="STAFF_" + desk_object.name + "_" + str(desk_object.id),
        #                                          related_desk=desk_object)
        #
        # editor_group = CustomGroup.objects.create(name="EDITOR_" + desk_object.name + "_" + str(desk_object.id),
        #                                           related_desk=desk_object)
        #
        # # add all participants of the desk here
        # common_group = CustomGroup.objects.create(name="COMMON_" + desk_object.name + "_" + str(desk_object.id),
        #                                           related_desk=desk_object)
        #
        # staff_group.save()
        # editor_group.save()
        # common_group.save()

        # return success response
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DeskDetailAPIView(mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.RetrieveAPIView,
                        ):
    permission_classes = [permissions.IsAuthenticated, IsEditorOfDeskOrHigher]
    authentication_classes = [SessionAuthentication]
    queryset = Desk.objects.prefetch_related("columns__tasks__comments").prefetch_related("permissionrow_set").all()
    serializer_class = DeskSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'desk_id'

    # def get_queryset(self):
    #     desk_id = self.kwargs["desk_id"]
    #     #print(desk_id)
    #     qs = Desk.objects.prefetch_related('columns__tasks__comments').filter(id=desk_id).first()
    #     return qs
    #
    # def get_object(self):
    #     DbQueries.show(l_dbg_sql=LOCAL_DEBUG_SQL, view=DeskDetailAPIView)
    #     request = self.request
    #     passed_id = self.kwargs["desk_id"]
    #     # print(passed_id)
    #     # query_set = self.get_queryset()
    #     #obj = self.queryset.filter(id=passed_id).first()
    #     obj = Desk.objects.prefetch_related("columns__tasks__comments").get(id=passed_id)
    #     #print(obj.permissionrow_set)#.objects.prefetch_related("permissionrow_set").get(id=passed_id)
    #     print(type(obj))
    #     #self.check_object_permissions(request, obj)
    #     #obj = Desk.objects.prefetch_related("columns__tasks__comments").get(id=passed_id)
    #     return obj

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
