#from sqlite3 import IntegrityError
from django.db import IntegrityError
from .permissions import IsAdminOfDesk, IsEditorOfDeskOrHigher, IsStaffOfDeskOrHigher
from rest_framework.views import APIView
from .serializers import UpdateUserPermissionsSerializer, AddUserToDeskSerializer
from user_auth.models import CustomGroup
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics
from desk.model import Desk
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import mixins
from .models import PermissionRow

User = get_user_model()


class SetUsersPermissionsAPIView(#generics.CreateAPIView,
                                    #generics.ListAPIView,
                                    #generics.RetrieveAPIView,
                                    generics.UpdateAPIView,
                                    #generics.ListAPIView,
                                    generics.CreateAPIView,
                                    #APIView,
                                    generics.DestroyAPIView,
                                    generics.GenericAPIView
                                   ):

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsEditorOfDeskOrHigher]
    serializer_class = AddUserToDeskSerializer
    queryset = Desk.objects.all()
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        """
        Use this method in order to add a new user with some permission to Desk
        """

        obj = self.get_object()

        if obj is None:
            return Response({"error": f"desk with selected id does not exists"}, status=400)

        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)

        #self.check_object_permissions(request, obj)
        data = request.data
        set_permission = request.data.get('set_to_permission')
        user_id = request.data.get('user_id')

        try:
            obj.permissionrow_set.create(user_id=user_id, permission=set_permission.upper())

        except IntegrityError:
            return Response({"error": "This user already has a "
                                      "permission in selected group. use PATCH "
                                      "method to change his permission"}, status=403)

        return Response({"message": f"successfully set user's permission to {set_permission}"}, status=200)

    def patch(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        """
        Changes permissions of user in selected group
        """
        obj = self.get_object()

        if obj is None:
            return Response({"error": f"desk with selected id does not exists"}, status=400)

        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)

        # self.check_object_permissions(request, obj)
        data = request.data
        set_permission = request.data.get('set_to_permission')
        user_id = request.data.get('user_id')

        perm = obj.permissionrow_set.filter(user_id=user_id).update(permission=set_permission)

        return Response({"message": "successfully updated"}, status=200)

    def delete(self, request, *args, **kwargs):
        """
        Just provide user_id in json file in order to delete him from Desk
        """

        obj = self.get_object()
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)

        if obj is None:
            return Response({"error": f"desk with selected id does not exists"}, status=400)

        user_id = request.data.get('user_id')
        perm = obj.permissionrow_set.filter(user_id=user_id).delete()

        return Response({"message": "successfully deleted user from desk"})

    # def update(self, request, *args, **kwargs):
    #     #self.permission_classes = [IsEditorOfDesk]
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #
    #     return Response(serializer.data)
    # def get_object(self):
    #     id = self.request.GET.get('pk')
    #     print(id)
    #     #qs = Desk.objects.get(id=id).customgroup_set.all()
    #     return CustomGroup.objects.first()
    # def post(self, request, *args, **kwargs):
    #     data = request.data
    # def post(self, request, *args, **kwargs):
    #     """
    #     If you add user for the first time(It means user was not participant of this desk before)
    #     then use POST method
    #     """
    #     data = request.data
    #
    #     user_id = data.get("user_id")
    #     desk_id = data.get("desk_id")
    #     add_to = data.get("change_to_permission")
    #
    #     desk = Desk.objects.filter(id=desk_id).first()
    #
    #     if not desk:
    #         return Response({"error": "Desk with that name does not exists"}, status=400)
    #
    #     if desk.author_id == user_id:
    #         return Response({"error": "You cannot change admin user role"}, status=403)
    #
    #     user = User.objects.filter(id=user_id).first()
    #     part_group_name = desk.name + "_" + str(desk.id)
    #     print(add_to.upper() + "_" + part_group_name)
    #     participants_group = CustomGroup.objects.get(name="COMMON" + "_" + part_group_name)
    #     group_to_add = CustomGroup.objects.get(name=add_to.upper() + "_" + part_group_name)
    #
    #     participants_group.user_set.add(user)
    #     group_to_add.user_set.add(user)
    #
    #     return Response(status=200)
    # def put(self, request, *args, **kwargs):
    #     """
    #     If you want to change user's rules in the desk (It means user is already
    #     participant of this desk) then use PATCH method
    #     """
    #     data = request.data
    #
    #     user_id = data.get("user_id")
    #     desk_id = data.get("desk_id")
    #     change_from = data.get("change_from_permission")
    #     change_to = data.get("change_to_permission")
    #
    #     desk = Desk.objects.filter(id=desk_id).first()
    #
    #     if not desk:
    #         return Response({"error": "Desk with that id does not exists"}, status=400)
    #
    #     if desk.author_id == user_id:
    #         return Response({"error": "You cannot change admin user role"}, status=403)
    #
    #     user = User.objects.filter(id=user_id).first()
    #     part_group_name = desk.name + "_" + str(desk.id)
    #
    #     group_to_add = CustomGroup.objects.get(name=change_to.upper() + "_" + part_group_name)
    #
    #     delete_from_group = CustomGroup.objects.get(name=change_from.upper() + "_" + part_group_name)
    #     delete_from_group.user_set.remove(user)
    #
    #     group_to_add.user_set.add(user)
    #
    #     return Response(status=200)
    #
    # def delete(self, request, *args, **kwargs):
    #     """Just provide user_id and desk_id"""
    #     data = request.data
    #
    #     user_id = data.get("user_id")
    #     desk_id = data.get("desk_id")
