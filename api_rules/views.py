from django.db import IntegrityError
from .permissions import IsAdminOfDesk, IsEditorOfDeskOrHigher
from .serializers import UpdatePermissionRowSerializer, PermissionSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework import generics
from .models import PermissionRow
from desk.model import Desk
from rest_framework import permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from user_auth.models import UsersDesks
from redis_manager.cache_manager import CacheManager

User = get_user_model()


class SetUsersPermissionsAPIView(generics.CreateAPIView,
                                 generics.ListAPIView
                                 ):

    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsEditorOfDeskOrHigher]
    serializer_class = PermissionSerializer
    queryset = PermissionRow.objects.select_related("related_desk").select_related("user").all()

    def get_queryset(self):
        qs = self.queryset.filter(related_desk_id=self.kwargs["desk_id"])

        # check if user has permissions to see these permission rows
        #perm = qs.filter(user_id=self.request.user).first()

        # if perm is None:
        #     return Response({"detail": "You do not have permission to perform this action"}, status=403)

        return qs

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        desk_id = self.kwargs['desk_id']
        return serializer.save(related_desk_id=desk_id)

    def post(self, request, *args, **kwargs):
        """
        Use this method in order to add a new user with some permission to Desk
        """

        # desk = Desk.objects.prefetch_related("permissionrow_set__user").filter(id=self.kwargs['desk_id']).first()

        # if desk is None:
        #     return Response({"error": f"desk with selected id does not exists"}, status=400)

        # # check if user has access to add new users to this desk
        # self.check_object_permissions(request, desk)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj = None
        try:
            obj = self.perform_create(serializer)

        except IntegrityError:
            return Response({"detail": "This user already has a "
                                      "permission in selected group. use PATCH"
                                      "method to change his permission"}, status=403)

        headers = self.get_success_headers(serializer.data)

        rel = UsersDesks.objects.create(user_id=obj.user_id, desks_id=self.kwargs['desk_id'])
        rel.save()

        # update cache
        CacheManager.update_cache_of_user(user_id=obj.user_id, permission=obj.permission, desk_id=self.kwargs['desk_id'])
        
        return Response(serializer.data, status=201, headers=headers)


class UpdateUsersPermissionsAPIView(generics.UpdateAPIView,
                                    generics.DestroyAPIView,
                                    ):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsEditorOfDeskOrHigher]
    serializer_class = UpdatePermissionRowSerializer
    queryset = PermissionRow.objects.prefetch_related("related_desk").select_related("user").all()

    def get_object(self):

        #obj = #PermissionRow.objects.prefetch_related("user").select_related("related_desk") \
        print(self.request.data)
        obj = self.queryset.filter(related_desk_id=self.kwargs['desk_id'], user_id=self.request.data['user']).first()

        return obj

    def put(self, request, *args, **kwargs):
        """Use PATCH method in order to update permissions"""
        return Response({"message": "Use PATCH method in order to update permissions"}, status=405)

    def patch(self, request, *args, **kwargs):
        """
        Changes permissions of user in selected group
        """

        # Get PermissionRow instance
        obj = self.get_object()

        if obj is None:
            return Response({"error": f"permission for this user does not exist"}, status=400)

        if obj.permission == "ADMIN":
            return Response({"detail": "You cannot change admin's role"}, status=403)
        
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # update permission in cache if user's data is in memory
        post_data = request.data
        user_id = post_data['user']
        
        CacheManager.update_cache_of_user(user_id=user_id, permission=post_data['permission'], desk_id=self.kwargs['desk_id'])
            
        if getattr(obj, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            obj._prefetched_objects_cache = {}

        return Response({"message": "successfully updated"}, status=200)

    def delete(self, request, *args, **kwargs):
        """
        Just provide user_id in json format in order to delete him from Desk
        """

        # Get PermissionRow instance
        obj = self.get_object()

        if obj is None:
            return Response({"detail": f"Permission for this user and desk does not exist"}, status=400)

        if obj.permission == "ADMIN":
            return Response({"detail": "You cannot delete admin user"}, status=403)

        # Remove record from UsersDesks table
        user_id = request.data.get('user')
        rel_to_desk = UsersDesks.objects.filter(user_id=user_id, desks_id=obj.related_desk.id).delete() 

        # update cache
        CacheManager.delete_user_cache_row(user_id=user_id, desk_id=obj.related_desk_id)

        # Delete permission and user from desk
        obj.delete()

        return Response({"message": "successfully deleted user from desk"}, status=204)
